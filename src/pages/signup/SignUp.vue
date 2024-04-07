<template>
  <!-- form wrapper -->
  <div class="container py-16">
    <div class="max-w-lg mx-auto shadow px-6 py-7 rounded overflow-hidden">
      <form @submit.prevent="handleSubmit">
        <!-- Sử dụng v-model để liên kết ref và input -->
        <input type="text" class="input-box w-full" placeholder="John Doe" required v-model="username" />
        <input type="email" class="input-box w-full" placeholder="example@mail.com" required v-model="email" />
        <input type="password" class="input-box w-full" placeholder="type password" required v-model="password" />
        <button
          type="submit"
          class="block w-full py-2 text-center text-white bg-primary border borderprimary rounded hover:bg-transparent hover:text-primary transition uppercase font-roboto font-medium"
        >
          create account
        </button>
      </form>
    </div>
  </div>
  <!-- form wrapper end -->
</template>

<script setup lang="ts">
import AuthAPI from '@/api/auth.api'
import router from '@/router'
import axios from 'axios'
import { ref } from 'vue'

// Nâng cao: xử lý validate form bằng VeeValidate ...
// https://vee-validate.logaretm.com/v3/
const username = ref('')
const email = ref('')
const password = ref('')

const handleSubmit = async (e: Event) => {
  // Gọi API thông qua Repository
  const res = await AuthAPI.logup({
    email: email.value,
    username: username.value,
    password: password.value
  })

  if ('id' in res) {
    // xử lý khi đăng ký thành công: hiển thị snackbar, alert, redirect,...
  } else {
    // xử lý khi đăng ký thất bại: hiển thị error
  }
}
</script>
