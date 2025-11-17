<script setup>
// Import Dependencies
import axios from "axios";
import { ref, onMounted } from "vue";

// Import Components

const notifications = ref([]);

const getNotifications = async () => {
  try {
    const { data } = await axios.get("/api/notifications/");
    console.log("data", data);
  } catch (error) {
    console.log("error", error);
  }
};
onMounted(getNotifications);
</script>

<template>
  <h1>Test</h1>
</template>

<style scoped></style>
