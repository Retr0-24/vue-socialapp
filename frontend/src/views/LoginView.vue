<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const toastStore = useToastStore()
const userStore = useUserStore()

const form = reactive({
  email: '',
  password: ''
})

const errors = ref([])

const submitForm = async () => {
  errors.value = []

  if (form.email === '') {
    errors.value.push('Email is required.')
  }
  if (form.password === '') {
    errors.value.push('Password is required.')
  }

  if (errors.value.length === 0) {
    try {
      const response = await axios.post('/api/login/', form)

      userStore.setToken(response.data)
      toastStore.showToast(3000, 'Logged in successfully.', 'bg-emerald-500')

      await router.push('/')
    } catch (error) {
      console.log('login error', error)
      errors.value.push('Invalid e-mail or password.')
      toastStore.showToast(3000, 'Invalid e-mail or password.', 'bg-red-300')
    }
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <!-- Login Text Fields -->
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Log in</h1>
        <p class="mb-6 text-gray-500">
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum
          dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
        </p>
        <p class="font-bold">
          Don't have an account?
          <RouterLink to="/signup" class="underline">Click here</RouterLink> to create an Account!
        </p>
      </div>
    </div>
    <!-- Login Input Fields -->
    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" v-on:submit.prevent="submitForm">
            <div>
                <label>E-mail</label><br>
                <input type="email" v-model="form.email" placeholder="Your E-Mail" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
            </div>
            <div>
                <label>Password</label><br>
                <input type="password" v-model="form.password" placeholder="Your Password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
            </div>
            <!-- Show Error Message -->
            <template v-if="errors.length > 0">
              <div class="bg-red-300 text-white rounded-lg p-6">
                <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
              </div>
            </template>
            <div>
                <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Login</button>
            </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
