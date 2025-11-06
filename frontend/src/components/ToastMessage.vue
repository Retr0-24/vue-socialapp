<script setup>
// Import the Pinia store for toast notifications.
import { useToastStore } from "@/stores/toast";

// Initialize the toast store to access its state.
const store = useToastStore();
</script>

<template>
  <!--
    This div represents the toast notification.
    It is only rendered if `store.isVisible` is true.
    The `v-if` directive handles the conditional rendering.
  -->
  <div
    v-if="store.isVisible"
    class="transition ease-in-out delay-500 duration-500 px-6 py-6 fixed top-full right-8 rounded-xl shadow-xl"
    :class="store.classes"
  >
    <!-- Display the message from the toast store. -->
    {{ store.message }}
  </div>
</template>

<style scoped>
/* Scoped styles for this component can be added here. */
</style>
