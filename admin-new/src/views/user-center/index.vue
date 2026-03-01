<script setup lang="ts">
import { reactive, ref } from 'vue';
import { NButton, NCard, NForm, NFormItem, NInput, NSpace, NTag } from 'naive-ui';
import { useAuthStore } from '@/store/modules/auth';
import { fetchUpdateProfile, fetchChangePassword, fetchGetUserInfo } from '@/service/api';

const authStore = useAuthStore();

const profileModel = reactive({
  nickname: authStore.userInfo.userName || ''
});

const passwordModel = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
});

const profileLoading = ref(false);
const passwordLoading = ref(false);

async function loadProfile() {
  const { data, error } = await fetchGetUserInfo();
  if (!error && data) {
    profileModel.nickname = data.nickName || data.userName;
  }
}

async function handleSaveProfile() {
  profileLoading.value = true;
  const { error } = await fetchUpdateProfile({ nickname: profileModel.nickname });
  if (!error) {
    window.$message?.success('资料更新成功');
    // refresh userInfo in auth store
    await authStore.initUserInfo();
  }
  profileLoading.value = false;
}

async function handleChangePassword() {
  if (!passwordModel.old_password || !passwordModel.new_password) {
    window.$message?.warning('请填写完整密码信息');
    return;
  }
  if (passwordModel.new_password !== passwordModel.confirm_password) {
    window.$message?.warning('两次输入的新密码不一致');
    return;
  }
  if (passwordModel.new_password.length < 4) {
    window.$message?.warning('新密码长度不能少于4位');
    return;
  }
  passwordLoading.value = true;
  const { error } = await fetchChangePassword({
    old_password: passwordModel.old_password,
    new_password: passwordModel.new_password
  });
  if (!error) {
    window.$message?.success('密码修改成功');
    passwordModel.old_password = '';
    passwordModel.new_password = '';
    passwordModel.confirm_password = '';
  }
  passwordLoading.value = false;
}

loadProfile();
</script>

<template>
  <div class="overflow-auto p-16px">
    <div class="max-w-800px mx-auto flex flex-col gap-16px">
      <!-- User Info Card -->
      <NCard title="基本信息">
        <div class="flex items-center gap-16px mb-20px">
          <div class="flex-center w-64px h-64px rounded-full bg-primary-100 dark:bg-primary-900">
            <SvgIcon icon="ph:user-circle" class="text-48px text-primary" />
          </div>
          <div>
            <div class="text-18px font-bold">{{ authStore.userInfo.userName }}</div>
            <NSpace class="mt-4px" size="small">
              <NTag v-for="role in authStore.userInfo.roles" :key="role" :type="role === 'super' ? 'warning' : 'info'" size="small">
                {{ role === 'super' ? '超级管理员' : '普通用户' }}
              </NTag>
            </NSpace>
          </div>
        </div>

        <NForm label-placement="left" label-width="80px" :model="profileModel">
          <NFormItem label="昵称">
            <NInput v-model:value="profileModel.nickname" placeholder="输入昵称" />
          </NFormItem>
          <NFormItem>
            <NButton type="primary" :loading="profileLoading" @click="handleSaveProfile">保存资料</NButton>
          </NFormItem>
        </NForm>
      </NCard>

      <!-- Change Password Card -->
      <NCard title="修改密码">
        <NForm label-placement="left" label-width="100px" :model="passwordModel">
          <NFormItem label="当前密码">
            <NInput
              v-model:value="passwordModel.old_password"
              type="password"
              show-password-on="click"
              placeholder="输入当前密码"
            />
          </NFormItem>
          <NFormItem label="新密码">
            <NInput
              v-model:value="passwordModel.new_password"
              type="password"
              show-password-on="click"
              placeholder="输入新密码"
            />
          </NFormItem>
          <NFormItem label="确认新密码">
            <NInput
              v-model:value="passwordModel.confirm_password"
              type="password"
              show-password-on="click"
              placeholder="再次输入新密码"
            />
          </NFormItem>
          <NFormItem>
            <NButton type="primary" :loading="passwordLoading" @click="handleChangePassword">修改密码</NButton>
          </NFormItem>
        </NForm>
      </NCard>
    </div>
  </div>
</template>
