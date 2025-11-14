<script setup>
// Import Dependencies
import axios from "axios";
import { onMounted, ref } from "vue";

// Import Components

const trends = ref([]);

const getTrends = async () => {
  try {
    const { data } = await axios.get("/api/posts/trends/");
    console.log("data", data);
    trends.value = data;
  } catch (error) {
    console.log("error", error);
  }
};

onMounted(getTrends);
</script>

<template>
  <!-- This component displays a "Trends" section with a list of trending hashtags. -->
  <div class="p-4 bg-white border border-gray-200 rounded-lg">
    <h3 class="mb-6 text-xl">Trends</h3>

    <!-- The list of trends is currently static with placeholder data. -->
    <div class="space-y-4">
      <!-- First trend entry -->
      <div
        class="flex items-center justify-between"
        v-for="trend in trends"
        v-bind:key="trend.id"
      >
        <p class="text-xs">
          <!-- Placeholder for the trend hashtag. -->
          <strong>#{{ trend.hashtag }}</strong
          ><br />
          <!-- Placeholder for the number of posts related to the trend. -->
          <span class="text-gray-500">{{ trend.occurences }} posts</span>
        </p>

        <!-- A link to explore the trend. -->
        <RouterLink
          :to="{ name: 'trendsview', params: { id: trend.hashtag } }"
          class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg"
          >Explore</RouterLink
        >
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Scoped styles for this component can be added here. */
</style>
