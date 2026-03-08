import { localStg } from '@/utils/storage';
import { getServiceBaseURL } from '@/utils/service';

/**
 * Create a WebSocket connection for monitoring a background task.
 *
 * @param taskId - The task ID returned by the API
 * @param onResult - Callback when task completes successfully
 * @param onError - Callback when task fails or connection errors
 * @returns WebSocket instance
 */
export function createTaskWebSocket(
  taskId: string,
  onResult: (data: any) => void,
  onError?: (err: string) => void
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
    // Relative URL like "/api" — use current page host
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    wsBase = `${protocol}//${window.location.host}${baseURL}`;
  }

  const wsUrl = `${wsBase}/ws/tasks/${taskId}?token=${encodeURIComponent(token)}`;
  const ws = new WebSocket(wsUrl);

  ws.onmessage = event => {
    try {
      const msg = JSON.parse(event.data);
      if (msg.type === 'task_completed') {
        onResult(msg.data);
        ws.close();
      } else if (msg.type === 'task_failed') {
        onError?.(msg.data?.error || '任务执行失败');
        ws.close();
      }
    } catch {
      // ignore parse errors
    }
  };

  ws.onerror = () => {
    onError?.('WebSocket连接失败');
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

  ws.onclose = () => {
    if (pingInterval) clearInterval(pingInterval);
  };

  return ws;
}
