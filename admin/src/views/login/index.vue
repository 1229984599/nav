<script setup lang="ts">
import { reactive, ref } from "vue";
import { loginRules } from "./rules.ts";
import type { FormInstance } from "element-plus";
import { useUserStore } from "@/store";
import router from "@/router";
import { ElMessage } from "element-plus";
import MIcon from "@/components/icon.vue";

const loginForm = reactive({
  username: "",
  password: "",
});
const userStore = useUserStore();
const loginFormRef = ref<FormInstance>();
const loading = ref(false);

function handleSubmit() {
  loginFormRef.value?.validate((valid: boolean, fields) => {
    if (valid) {
      loading.value = true;
      userStore
        .login(loginForm)
        .then(() => {
          ElMessage.success("登录成功");
          router.push({
            path: "/",
          });
        })
        .finally(() => {
          loading.value = false;
        });
    } else {
      new Error("表单校验失败");
    }
  });
}
</script>

<template>
  <div class="login-container">
    <el-form
      class="login-form"
      ref="loginFormRef"
      :model="loginForm"
      :rules="loginRules"
      @keyup.enter="handleSubmit"
    >
      <a class="title-container gap-x-2" href="/">
        <m-icon icon="ion:logo-edge" color="white" :size="50" />
        <h3 class="title">用户登录</h3>
      </a>

      <el-form-item prop="username">
        <el-input
          v-model.trim="loginForm.username"
          clearable
          prefix-icon="user"
          placeholder="请输入用户名"
          type="text"
        />
      </el-form-item>

      <el-form-item prop="password">
        <el-input
          v-model.trim="loginForm.password"
          prefix-icon="Lock"
          show-password
          clearable
          placeholder="请输入密码"
          type="password"
        />
      </el-form-item>
      <el-button type="primary" :loading="loading" @click.prevent="handleSubmit"
        >登录
      </el-button>
    </el-form>
  </div>
</template>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;
$cursor: #fff;

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 80%;
    margin: 0 auto;

    .el-button {
      width: 100%;
      height: 50px;
    }

    .el-form-item {
      padding: 0px 5px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      border-radius: 5px;
    }

    :deep(.el-input) {
      display: inline-block;
      height: 47px;
      //width: 100%;
      .el-input__wrapper {
        background-color: unset;
        box-shadow: unset;
        width: 100%;
      }

      input {
        width: 100%;
        border: 0px;
        border-radius: 0px;
        padding: 12px 5px 12px 15px;
        color: $light_gray;
        height: 47px;
        caret-color: $cursor;
      }
    }
  }

  .tips {
    font-size: 16px;
    line-height: 28px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    display: inline-block;
  }

  .title-container {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;

    .title {
      font-size: 26px;
      color: $light_gray;
      text-align: center;
      font-weight: bold;
    }
  }
}
</style>
