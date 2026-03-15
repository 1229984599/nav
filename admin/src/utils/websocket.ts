import { localStg } from '@/utils/storage';
import { getServiceBaseURL } from '@/utils/service';

/** WS 超时时间（毫秒），超过此时间未收到完成/失败消息则视为连接异常 */
const WS_TIMEOUT = 60_000;

/**
 * Create a WebSocket connection for monitoring a background task.
 *
 * @param taskId - The task ID returned by the API
 * @param onResult - Callback when task completes successfully
 * @param onError - Callback when task fails or connection errors
 * @param onProgress - Optional callback for progress updates
 * @returns WebSocket instance
 */
export function createTaskWebSocket(
  taskId: string,
  onResult: (data: any) => void,
  onError?: (err: string) => void,
  onProgress?: (data: any) => void
): WebSocket {
  const isHttpProxy = import.meta.env.DEV && import.meta.env.VITE_HTTP_PROXY === 'Y';
  const { baseURL } = getServiceBaseURL(import.meta.env, isHttpProxy);
  const token = localStg.get('token') || '';

  let wsBase: string;
  if (baseURL.startsWith('http://')) {
    wsBase = baseURL.replace('http://', 'ws://');
  } else if (baseURL.startsWith('https://')) {
    wsBase = baseURL.replace('https://', 'wss://');
  } else {
    // Relative URL like "/api" or "/proxy-default" — use current page host
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    wsBase = `${protocol}//${window.location.host}${baseURL}`;
  }

  const wsUrl = `${wsBase}/ws/tasks/${taskId}?token=${encodeURIComponent(token)}`;
  const ws = new WebSocket(wsUrl);

  let settled = false;

  function settle() {
    if (settled) return false;
    settled = true;
    if (timeoutTimer) clearTimeout(timeoutTimer);
    if (pingInterval) clearInterval(pingInterval);
    return true;
  }

  // Timeout fallback: if no result within WS_TIMEOUT, treat as error
  const timeoutTimer = setTimeout(() => {
    if (settled) return;
    settle();
    try { ws.close(); } catch { /* ignore */ }
    onError?.('任务超时未响应，请刷新页面查看结果');
  }, WS_TIMEOUT);

  ws.onmessage = event => {
    try {
      const msg = JSON.parse(event.data);
      if (msg.type === 'task_completed') {
        if (settle()) onResult(msg.data);
        ws.close();
      } else if (msg.type === 'task_failed') {
        if (settle()) onError?.(msg.data?.error || '任务执行失败');
        ws.close();
      } else if (msg.type === 'task_progress') {
        onProgress?.(msg.data);
      }
    } catch {
      // ignore parse errors
    }
  };

  ws.onerror = () => {
    if (settle()) onError?.('WebSocket连接失败');
  };

  // Keep-alive ping every 30s
  let pingInterval: ReturnType<typeof setInterval> | null = null;
  ws.onopen = () => {
    pingInterval = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send('ping');
      }
    }, 30000);
  };

  ws.onclose = event => {
    if (pingInterval) clearInterval(pingInterval);
    // Abnormal close without a result — treat as error
    if (settle()) {
      if (event.code === 4001) {
        onError?.('WebSocket认证失败，请重新登录');
      } else if (event.code === 4004) {
        onError?.('任务不存在');
      } else {
        onError?.('WebSocket连接已断开，请刷新页面查看结果');
      }
    }
  };

  return ws;
}
