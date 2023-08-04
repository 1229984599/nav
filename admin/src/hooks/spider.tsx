import { ref } from "vue";

export function useSpiderButtons(model: any) {
  const spiderLoading = ref(false);
  return {
    spider: {
      text: "采集",
      type: "success",
      loading: spiderLoading,
      click: ({ form }) => {
        spiderLoading.value = true;
        model
          .getSiteInfo(form.href)
          .then(data => Object.assign(form, data))
          .finally(() => {
            spiderLoading.value = false;
          });
      }
    }
  };
}
