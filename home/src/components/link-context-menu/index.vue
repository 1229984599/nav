<script setup lang="ts">
import { computed, reactive, ref, nextTick } from "vue";
import MIcon from "@/components/MIcon.vue";
import IconSelect from "@/components/icon-select/index.vue";
import linksModel from "@/api/links";
import { isMobile, isUrl } from "@/utils/window";
import { ElMessage, ElMessageBox, type FormInstance, FormRules } from "element-plus";
import { useMenuStore } from "@/store/menu";
import { LinkSchemaList } from "@/api/links/types";

defineOptions({
  name: "MLinkContextMenu",
});

const menuStore = useMenuStore();

// 右键菜单状态
const menuVisible = ref(false);
const menuStyle = reactive({ left: "0px", top: "0px" });
const currentItem = ref<LinkSchemaList | null>(null);

// 编辑弹窗状态
const dialogVisible = ref(false);
const editLoading = ref(false);
const ruleFormRef = ref<FormInstance>();
const spiderLoading = ref(false);

const form = reactive({
  title: "",
  href: "",
  icon: "",
  color: "",
  menus: [] as number[],
  order: 0,
  is_self: false,
  is_vip: false,
  status: true,
  desc: "",
});

const rules: FormRules = reactive<FormRules>({
  title: [{ required: true, message: "请输入标题", trigger: "blur" }],
  icon: [{ required: true, message: "请输入图标", trigger: "blur" }],
  href: [{ required: true, message: "请输入链接", trigger: "blur" }],
  menus: [{ required: true, message: "分类必选", trigger: "blur" }],
});

const isSpiderInfo = computed(() => isUrl(form.href));

function show(event: MouseEvent, item: LinkSchemaList) {
  event.preventDefault();
  event.stopPropagation();
  currentItem.value = item;
  menuStyle.left = event.clientX + "px";
  menuStyle.top = event.clientY + "px";
  menuVisible.value = true;

  const hide = () => {
    menuVisible.value = false;
    document.removeEventListener("click", hide);
    document.removeEventListener("contextmenu", hide);
  };
  nextTick(() => {
    document.addEventListener("click", hide);
    document.addEventListener("contextmenu", hide);
  });
}

async function handleEdit() {
  menuVisible.value = false;
  if (!currentItem.value?.id) return;
  // 从 API 获取完整链接数据（包含 menus 关联）
  // 因为 menu/tree 接口返回的 link 不含 menus 字段
  editLoading.value = true;
  try {
    const item: LinkSchemaList = await linksModel.read(currentItem.value.id);
    form.title = item.title || "";
    form.href = item.href || "";
    form.icon = item.icon || "";
    form.color = item.color || "";
    form.menus = item.menus?.map((m) => m.id!).filter(Boolean) || [];
    form.order = item.order ?? 0;
    form.is_self = item.is_self || false;
    form.is_vip = item.is_vip || false;
    form.status = item.status ?? true;
    form.desc = item.desc || "";
    dialogVisible.value = true;
  } catch (e) {
    console.error("获取链接详情失败", e);
  } finally {
    editLoading.value = false;
  }
}

function handleDelete() {
  menuVisible.value = false;
  if (!currentItem.value?.id) return;
  const id = currentItem.value.id;
  ElMessageBox.confirm("确定删除该链接吗？", "删除确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await linksModel.delete(String(id));
      ElMessage.success("删除成功");
      await menuStore.getMenuTree();
    })
    .catch(() => {});
}

async function handleSiteInfo() {
  if (!form.href) {
    ElMessage.warning("请先输入链接地址");
    return;
  }
  spiderLoading.value = true;
  linksModel
    .getSiteInfo(form.href)
    .then((data) => {
      if (data.title) form.title = data.title;
      if (data.icon) form.icon = data.icon;
      if (data.desc) form.desc = data.desc;
      ElMessage.success("抓取成功");
    })
    .finally(() => (spiderLoading.value = false));
}

async function handleSubmit() {
  ruleFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    if (!currentItem.value?.id) return;
    await linksModel.update(currentItem.value.id, { ...form });
    dialogVisible.value = false;
    ElMessage.success("修改成功");
    await menuStore.getMenuTree();
  });
}

function handleCancel() {
  dialogVisible.value = false;
}

defineExpose({ show });
</script>

<template>
  <!-- 右键菜单 -->
  <teleport to="body">
    <transition name="ctx-spring">
      <div
        v-show="menuVisible"
        class="context-menu"
        :style="menuStyle"
      >
        <div class="context-menu-item" @click="handleEdit">
          <m-icon icon="mdi:pencil-outline" :size="16" />
          <span>编辑</span>
        </div>
        <div class="context-menu-item context-menu-item--danger" @click="handleDelete">
          <m-icon icon="mdi:delete-outline" :size="16" />
          <span>删除</span>
        </div>
      </div>
    </transition>
  </teleport>

  <!-- 编辑弹窗 -->
  <el-dialog
    center
    append-to-body
    :close-on-click-modal="false"
    v-model="dialogVisible"
    :fullscreen="isMobile"
    title="编辑链接"
    width="650px"
  >
    <el-form v-loading="editLoading" :model="form" :rules="rules" ref="ruleFormRef" label-width="80px">
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title" placeholder="链接标题" />
      </el-form-item>
      <el-form-item label="链接" prop="href">
        <div class="flex gap-2 w-full">
          <el-input v-model="form.href" placeholder="https://" />
          <el-button
            type="success"
            :disabled="!isSpiderInfo"
            :loading="spiderLoading"
            @click="handleSiteInfo"
          >抓取</el-button>
        </div>
      </el-form-item>
      <el-form-item label="图标" prop="icon">
        <icon-select v-model="form.icon" :color="form.color" />
      </el-form-item>
      <el-form-item label="颜色" prop="color">
        <el-color-picker
          size="large"
          v-model="form.color"
          :predefine="[
            '#ff4500',
            '#ff8c00',
            '#ffd700',
            '#90ee90',
            '#00ced1',
            '#1e90ff',
            '#c71585',
            '#c7158577',
          ]"
        />
      </el-form-item>
      <el-form-item label="菜单" prop="menus">
        <el-tree-select
          v-model="form.menus"
          :data="menuStore.menuTree"
          multiple
          :render-after-expand="false"
          show-checkbox
          check-strictly
          highlight-current
          filterable
          clearable
          check-on-click-node
          placeholder="选择所属菜单"
          class="w-full"
          :props="{
            label: 'title',
            value: 'id',
          }"
          node-key="id"
          value-key="id"
        >
          <template #default="{ data }">
            <div class="flex gap-x-1">
              <m-icon :size="20" :color="data.color" :icon="data?.icon" />
              <span>{{ data.title }}</span>
            </div>
          </template>
        </el-tree-select>
      </el-form-item>
      <el-form-item label="排序" prop="order">
        <el-input-number v-model="form.order" :min="0" />
      </el-form-item>
      <el-form-item label="站内打开" prop="is_self">
        <el-switch v-model="form.is_self" />
      </el-form-item>
      <el-form-item label="VIP" prop="is_vip">
        <el-switch v-model="form.is_vip" />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-switch v-model="form.status" />
      </el-form-item>
      <el-form-item label="描述" prop="desc">
        <el-input type="textarea" v-model="form.desc" placeholder="链接描述" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="flex justify-center">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style lang="scss" scoped>
.context-menu {
  position: fixed;
  z-index: 9999;
  background: var(--nav-card-bg, #fff);
  border: 1px solid var(--nav-border, rgba(0, 0, 0, 0.06));
  border-radius: 6px;
  padding: 4px 0;
  min-width: 120px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.context-menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  color: var(--nav-text, #1f2937);
  transition: background-color 0.15s;

  &:hover {
    background-color: rgba(0, 0, 0, 0.04);
  }

  &--danger {
    color: #ef4444;

    &:hover {
      background-color: rgba(239, 68, 68, 0.08);
    }
  }
}
</style>
