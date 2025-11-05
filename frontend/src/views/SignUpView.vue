<script setup>
import axios from 'axios'
import { reactive, ref } from 'vue'
import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()

const form = reactive({
  name: '',
  email: '',
  password1: '',
  password2: ''
})

const errors = ref([])

const submitForm = async () => {
  errors.value = []

  if (form.name === '') {
    errors.value.push('Name is required.')
  }
  if (form.email === '') {
    errors.value.push('Email is required.')
  }
  if (form.password1 === '') {
    errors.value.push('Password is required.')
  }
  if (form.password1 !== form.password2) {
    errors.value.push('Passwords do not match.')
  }

  if (errors.value.length === 0) {
    try {
      const response = await axios.post('/api/signup/', form)

      if (response.data.message === 'success') {
        toastStore.showToast(5000, 'The user is registered successfully. Please log in.', 'bg-emerald-500')

        form.name = ''
        form.email = ''
        form.password1 = ''
        form.password2 = ''
      } else {
        toastStore.showToast(5000, 'There was an error during registration. Please try again later.', 'bg-red-300')
      }
    } catch (error) {
      console.log('error', error)
    }
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <!-- Sign up Text Fields -->
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Sign Up</h1>
        <p class="mb-6 text-gray-500">
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum
          dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
        </p>
        <p class="font-bold">
          Already have an account?
          <RouterLink to="/login" class="underline">Click here</RouterLink> to Log in!
        </p>
      </div>
    </div>
    <!-- Sign up Input Fields -->
    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" v-on:submit.prevent="submitForm">
            <div>
                <label>Name</label><br>
                <input type="text" v-model="form.name" placeholder="Your Full Name" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
            </div>
            <div>
                <label>E-mail</label><br>
                <input type="email" v-model="form.email" placeholder="Your E-Mail" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
            </div>
            <div>
                <label>Password</label><br>
                <input type="password" v-model="form.password1" placeholder="Your Password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
            </div>
            <div>
                <label>Confirm Password</label><br>
                <input type="password" v-model="form.password2" placeholder="Confirm Password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
            </div>
            <!-- Show Error Message -->
            <template v-if="errors.length > 0">
              <div class="bg-red-300 text-white rounded-lg p-6">
                <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
              </div>
            </template>

            <div>
                <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Sign Up</button>
            </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
