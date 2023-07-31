import { nextTick, onMounted, ref, watch } from "vue";
import { useScroll, useWebSocket } from "@vueuse/core";
import { isMobile } from "@/utils/windows";

export function useWs(url: string) {
  const messageList = ref([]);
  const loading = ref(false);
  const isFinish = ref(false);
  const websocket = useWebSocket(url, {
    heartbeat: true,
    onMessage: (ws, event) => {
      messageList.value.push(event.data);
      // console.log(event.data);
      if (event.data === "stop") {
        isFinish.value = true;
      } else {
        loading.value = true;
      }
    },
    onError: ws => {
      messageList.value = [];
      // ws.close()
    }
  });
  return {
    messageList,
    loading,
    isFinish,
    websocket
  };
}

export function useLogs(url: string) {
  // `ws://127.0.0.1:8000/api/v1/safe/user/logs/${client_id}`

  const viewLoging = ref(false);
  const { messageList, loading, isFinish, websocket } = useWs(url);
  const el = ref<HTMLElement | null>(null);
  watch(messageList.value, () => {
    el.value.scrollTo(0, el.value.scrollHeight);
  });

  const logView = () => (
    <el-dialog
      v-model={viewLoging.value}
      fullscreen={isMobile.value}
      destroy-on-close
      align-center
      onClose={() => {
        if (isFinish.value) {
          messageList.value = [];
          loading.value = false;
          websocket.close();
        }
      }}
    >
      <ul ref={el} class="h-[280px] overflow-y-scroll">
        {messageList.value.map(message => (
          <li>{message}</li>
        ))}
      </ul>
    </el-dialog>
  );
  return { logView, viewLoging, isFinish, loading, websocket, messageList };
}
