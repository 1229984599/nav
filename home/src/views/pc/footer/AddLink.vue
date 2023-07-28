<script setup lang="ts">
import { reactive, ref } from "vue";
import MIcon from "@/components/MIcon.vue";
import nav from "@/api/nav";

const dialogFormVisible = ref(false);

const form = reactive({
  title: "",
  icon: "",
  href: "",
  desc: "",
  isSelf: false,
  category: 1,
});

const rules = {
  title: [
    { required: true, message: "请输入标题", trigger: "blur" },

    { min: 1, max: 20, message: "长度在 1 到 20 个字符", trigger: "blur" },
  ],
  icon: [
    { required: true, message: "请输入图标", trigger: "blur" },

    { min: 1, max: 20, message: "长度在 1 到 20 个字符", trigger: "blur" },
  ],
  href: [
    { required: true, message: "请输入链接", trigger: "blur" },

    { min: 1, max: 20, message: "长度在 1 到 20 个字符", trigger: "blur" },
  ],
  desc: [
    { required: true, message: "请输入描述", trigger: "blur" },

    { min: 1, max: 20, message: "长度在 1 到 20 个字符", trigger: "blur" },
  ],
};

async function handleSiteInfo() {
  const data = await nav.getSiteInfo(form.href);
  form.title = data?.title;
  form.icon = data?.icon;
  form.desc = data?.desc;
}
</script>

<template>
  <div>
    <m-icon
      @click="dialogFormVisible = true"
      class="hover:text-red-900"
      icon="gridicons:add-outline"
    />

    <el-dialog
      center
      :close-on-click-modal="false"
      v-model="dialogFormVisible"
      title="添加网站"
    >
      <el-form :model="form">
        <el-form-item label="链接">
          <el-input v-model="form.href" />
        </el-form-item>
        <el-form-item label="标题">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="图标">
          <el-input v-model="form.icon" />
        </el-form-item>

        <el-form-item label="描述">
          <el-input type="textarea" v-model="form.desc" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category" placeholder="请选择">
            <el-option label="常用工具" :value="1" />
            <el-option label="系统管理" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="站内打开">
          <el-switch
            v-model="form.isSelf"
            active-text="是"
            inactive-text="否"
            inline-prompt
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div>
          <el-button type="success" @click="handleSiteInfo">采集数据</el-button>
          <el-button type="primary">确定</el-button>
          <el-button type="danger" @click="dialogFormVisible = false"
            >取消
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped></style>
