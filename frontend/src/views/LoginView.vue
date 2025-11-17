<script setup>
// Import Dependencies
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

// Import Components
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "@/stores/user";

const router = useRouter();
const toastStore = useToastStore();
const userStore = useUserStore();

// Reactive form object to hold user's login credentials.
const form = reactive({
  email: "",
  password: "",
});

const errors = ref([]);

/**
 * Handles the form submission for user login.
 * It performs validation, sends a login request, and handles the response.
 */
const submitForm = async () => {
  // Clear previous errors.
  errors.value = [];

  // Basic frontend validation.
  if (form.email === "") {
    errors.value.push("Email is required.");
  }
  if (form.password === "") {
    errors.value.push("Password is required.");
  }

  // If there are no validation errors, proceed with the API call.
  if (errors.value.length === 0) {
    try {
      // Send a POST request to the login endpoint.
      const response = await axios.post("/api/login/", form);

      // If login is successful, store the token in the user store.
      userStore.setToken(response.data);

      // Fetch the user's information.
      const { data: user } = await axios.get("/api/me/");
      // Store the user's information in the user store.
      userStore.setUserInfo(user);

      // Show a success toast notification.
      toastStore.showToast(3000, "Logged in successfully.", "bg-emerald-500");

      // Redirect the user to the feed page.
      await router.push("/feed");
    } catch (error) {
      // If there's an error during login, log it and show an error message.
      console.log("login error", error);
      errors.value.push(
        "Invalid e-mail or password. Or the User is no Activated."
      );
      toastStore.showToast(
        3000,
        "Invalid e-mail or password. Or the User is no Activated.",
        "bg-red-300"
      );
    }
  }
};
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <!-- Left side: Informational text and link to signup -->
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Log in</h1>
        <p class="mb-6 text-gray-500">
          Welcome back! Please enter your credentials to log in.
        </p>
        <p class="font-bold">
          Don't have an account?
          <RouterLink to="/signup" class="underline">Click here</RouterLink> to
          create one!
        </p>
      </div>
    </div>

    <!-- Right side: Login form -->
    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" @submit.prevent="submitForm">
          <!-- Email input field -->
          <div>
            <label>E-mail</label><br />
            <input
              type="email"
              v-model="form.email"
              placeholder="Your E-Mail"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <!-- Password input field -->
          <div>
            <label>Password</label><br />
            <input
              type="password"
              v-model="form.password"
              placeholder="Your Password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <!-- Display error messages if any -->
          <template v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>
          </template>

          <!-- Submit button -->
          <div>
            <button
              class="py-4 px-6 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
            >
              Log in
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Scoped styles for this component can be added here. */
</style>
