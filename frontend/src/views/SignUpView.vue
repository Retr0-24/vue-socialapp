<script setup>
// Import Dependencies
import axios from 'axios' // HTTP client for API requests.
import { reactive, ref } from 'vue' // Vue's reactivity functions.
import { useToastStore } from '@/stores/toast' // Pinia store for toast notifications.

// Initialize the toast store.
const toastStore = useToastStore()

// Reactive form object to hold user's registration data.
const form = reactive({
  name: '',
  email: '',
  password: '',
  password_confirmation: ''
})

// A ref to hold any validation or API errors.
const errors = ref([])

/**
 * Handles the form submission for user registration.
 * It performs validation, sends a registration request, and handles the response.
 */
const submitForm = async () => {
  // Clear previous errors.
  errors.value = []

  // Basic frontend validation.
  if (form.name === '') {
    errors.value.push('Name is required.')
  }
  if (form.email === '') {
    errors.value.push('Email is required.')
  }
  if (form.password === '') {
    errors.value.push('Password is required.')
  }
  if (form.password !== form.password_confirmation) {
    errors.value.push('Passwords do not match.')
  }

  // If there are no validation errors, proceed with the API call.
  if (errors.value.length === 0) {
    try {
      // Send a POST request to the signup endpoint.
      const response = await axios.post('/api/signup/', form)

      // If registration is successful, show a success toast and clear the form.
      if (response.data.message === 'success') {
        toastStore.showToast(5000, 'The user is registered successfully. Please log in.', 'bg-emerald-500')

        // Clear the form fields.
        form.name = ''
        form.email = ''
        form.password = ''
        form.password_confirmation = ''
      } else {
        // If there was an error, show a generic error toast.
        toastStore.showToast(5000, 'There was an error during registration. Please try again later.', 'bg-red-300')
      }
    } catch (error) {
      // Log any errors to the console.
      console.log('error', error)
    }
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <!-- Left side: Informational text and link to login -->
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Sign Up</h1>
        <p class="mb-6 text-gray-500">
          Create an account to start sharing and connecting with your friends.
        </p>
        <p class="font-bold">
          Already have an account?
          <RouterLink to="/login" class="underline">Click here</RouterLink> to Log in!
        </p>
      </div>
    </div>

    <!-- Right side: Sign-up form -->
    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" @submit.prevent="submitForm">
          <!-- Name input field -->
          <div>
            <label>Name</label><br>
            <input type="text" v-model="form.name" placeholder="Your Full Name" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <!-- Email input field -->
          <div>
            <label>E-mail</label><br>
            <input type="email" v-model="form.email" placeholder="Your E-Mail" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <!-- Password input field -->
          <div>
            <label>Password</label><br>
            <input type="password" v-model="form.password" placeholder="Your Password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <!-- Confirm Password input field -->
          <div>
            <label>Confirm Password</label><br>
            <input type="password" v-model="form.password_confirmation" placeholder="Confirm Password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <!-- Display error messages if any -->
          <template v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>
          </template>

          <!-- Submit button -->
          <div>
            <button class="py-4 px-6 bg-purple-600 text-white rounded-lg hover:bg-purple-700">Sign Up</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Scoped styles for this component can be added here. */
</style>
