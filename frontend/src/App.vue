<script setup>
// This script setup block handles the component's logic.

// Import Dependencies
import { onBeforeMount } from "vue"; // Vue's lifecycle hook that runs before the component is mounted.
import { RouterView } from "vue-router"; // Used to display the component for the current route.
import axios from "axios"; // HTTP client for making API requests.
import { storeToRefs } from "pinia"; // Utility to create refs from store properties.

// Import Components
import ToastMessage from "./components/ToastMessage.vue"; // Component to display toast notifications.
import { useUserStore } from "./stores/user"; // Pinia store for user state management.

// Initialize the user store.
const userStore = useUserStore();

// Destructure reactive properties from the user store.
const { isAuthenticated } = storeToRefs(userStore);

// `onBeforeMount` lifecycle hook to initialize the user store and set up Axios headers.
onBeforeMount(() => {
  // Initialize the user store, which likely involves checking for existing user data in local storage.
  userStore.initStore();

  // If an access token is present in the user store, set it as the default Authorization header for all Axios requests.
  if (userStore.access) {
    axios.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${userStore.access}`;
  } else {
    // If no access token is found, remove the Authorization header from Axios defaults.
    delete axios.defaults.headers.common["Authorization"];
  }
});
</script>

<template>
  <!-- Main application navigation bar -->
  <nav class="py-10 px-8 border-b border-gray-200">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between">
        <!-- Logo and application title -->
        <div class="menu-left">
          <a href="#" class="text-xl">Social App</a>
        </div>

        <!-- Center menu with navigation links, shown only if the user is authenticated -->
        <div class="menu-center flex space-x-12" v-if="isAuthenticated">
          <!-- Home link with an SVG icon -->
          <a href="#" class="text-purple-700">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"
              />
            </svg>
          </a>

          <!-- Messages link with an SVG icon -->
          <a>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M8.625 9.75a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 01.778-.332 48.294 48.294 0 005.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z"
              />
            </svg>
          </a>

          <!-- Notifications link with an SVG icon -->
          <a>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"
              />
            </svg>
          </a>

          <!-- Search link with an SVG icon -->
          <a href="#">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
              />
            </svg>
          </a>
        </div>

        <!-- Right menu with user-specific actions -->
        <div class="menu-right">
          <!-- Display user avatar if authenticated -->
          <template v-if="isAuthenticated">
            <a href="#">
              <img src="https://i.pravatar.cc/40?img=70" class="rounded-full" />
            </a>
          </template>
          <!-- Display Login and Signup links if not authenticated -->
          <template v-else>
            <RouterLink
              to="/login"
              class="mr-4 py-4 px-6 bg-gray-600 text-white rounded-lg"
              >Login
            </RouterLink>
            <RouterLink
              to="/signup"
              class="py-4 px-6 bg-purple-600 text-white rounded-lg"
              >Signup
            </RouterLink>
          </template>
        </div>
      </div>
    </div>
  </nav>

  <!-- Main content area where routed components will be displayed -->
  <main class="px-8 py-6 bg-gray-100">
    <RouterView />
  </main>

  <!-- Toast message component to show notifications -->
  <ToastMessage />
</template>

<style scoped>
/* Scoped styles for this component. */
/* These styles will only apply to the elements in this component and not affect other components. */
</style>
