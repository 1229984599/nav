<script lang="ts" setup>
import { onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/store/user";
import { ElMessage, type FormInstance, FormRules } from "element-plus";
import { type LoginRequestData } from "@/api/login/types";
import MLogo from "@/components/MLogo.vue";
import { useSiteStore } from "@/store/site";

const router = useRouter();
const userStore = useUserStore();
const loginFormRef = ref<FormInstance | null>(null);
const loading = ref(false);
const loginFormData: LoginRequestData = reactive({
  username: "",
  password: "",
});
const loginFormRules: FormRules = {
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [
    { required: true, message: "请输入密码", trigger: "blur" },
    { min: 5, max: 16, message: "长度在 5 到 16 个字符", trigger: "blur" },
  ],
};
const handleLogin = () => {
  loginFormRef.value?.validate((valid: boolean) => {
    if (valid) {
      loading.value = true;
      userStore
        .login(loginFormData)
        .then(() => {
          ElMessage.success("登录成功");
          userStore.getUserinfo();
          router.go(-1);
        })
        .catch(() => {
          loginFormData.password = "";
        })
        .finally(() => {
          loading.value = false;
        });
    }
  });
};
const siteStore = useSiteStore();
onMounted(siteStore.getSiteInfo);
</script>

<template>
  <div class="login-container">
    <div class="login-bg"></div>
    <div class="login-card">
      <div class="card-header">
        <m-logo class="flex justify-center" font-size="24px" />
      </div>
      <div class="card-body">
        <el-form
          ref="loginFormRef"
          :model="loginFormData"
          :rules="loginFormRules"
          @keyup.enter="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model.trim="loginFormData.username"
              placeholder="请输入用户名"
              clearable
              autofocus
              type="text"
              tabindex="1"
              size="large"
              prefix-icon="User"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model.trim="loginFormData.password"
              placeholder="请输入密码"
              clearable
              type="password"
              tabindex="2"
              size="large"
              show-password
              prefix-icon="Lock"
            />
          </el-form-item>
          <el-button
            :loading="loading"
            type="primary"
            size="large"
            round
            @click.prevent="handleLogin"
          >登 录</el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.login-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  min-height: 100vh;
  overflow: hidden;
}

.login-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: 0;

  &::before,
  &::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    opacity: 0.12;
    background: #fff;
  }

  &::before {
    width: 600px;
    height: 600px;
    top: -200px;
    right: -100px;
    animation: float 8s ease-in-out infinite;
  }

  &::after {
    width: 400px;
    height: 400px;
    bottom: -150px;
    left: -100px;
    animation: float 6s ease-in-out infinite reverse;
  }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-30px); }
}

.login-card {
  position: relative;
  z-index: 1;
  width: 420px;
  max-width: 90%;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  overflow: hidden;

  .card-header {
    padding: 32px 32px 16px;
  }

  .card-body {
    padding: 8px 40px 40px;

    .el-button {
      width: 100%;
      margin-top: 8px;
      font-size: 16px;
      letter-spacing: 4px;
    }
  }
}
</style>
