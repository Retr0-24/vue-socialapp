<script setup>
// Import Dependencies
import axios from "axios";
import { useRoute } from "vue-router";
import { onMounted, ref, watch } from "vue";

// Import components.
import PeopleYouKnow from "@/components/PeopleYouKnow.vue";
import Trends from "@/components/Trends.vue";
import FeedItem from "@/components/FeedItem.vue";

const posts = ref([]);
const route = useRoute();

const getFeed = async () => {
  try {
    const { data } = await axios.get(`/api/posts/?trend=${route.params.id}`);
    console.log("data", data);

    posts.value = data;
  } catch (error) {
    console.log("error", error);
  }
};

onMounted(getFeed);

watch(
  () => route.params.id,
  () => getFeed(),
  { immediate: true }
);
</script>

<template>
  <!-- This view represents the main feed page with a three-column layout. -->
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <!-- Center column: Post creation and feed -->
    <div class="main-center col-span-3 space-y-4">
      <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <h2 class="text-xl capitalize"># {{ route.params.id }}</h2>
      </div>
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts"
        v-bind:key="post.id"
      >
        <FeedItem v-bind:post="post" />
      </div>
    </div>
    <!-- Right column: "People you may know" and "Trends" sections -->
    <div class="main-right col-span-1 space-y-4">
      <PeopleYouKnow />
      <Trends />
    </div>
  </div>
</template>

<style scoped>
/* Scoped styles for this component can be added here. */
</style>
