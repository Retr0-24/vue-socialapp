<script setup>
import { useToastStore } from "@/stores/toast";

// Initialize Variable that is stored with isVisible, Classes and Message
const store = useToastStore();

return {
  store,
};
</script>

<template>
  <!-- Create if statement to store only in variable if store is Visible and Design Toast Message -->
  <div
    v-if="store.isVisible"
    class="transition ease-in-out delay-500 duration-500 px-6 py-6 fixed top-full right-8 rounded-xl shadow-xl"
    :class="store.classes"
  >
    <!-- Show stored message Success or Error -->
    {{ store.message }}
  </div>
</template>

<style scoped></style>
