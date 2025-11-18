<script setup>
// Import Dependencies
import axios from "axios";

// Import components.
import PeopleYouKnow from "@/components/PeopleYouKnow.vue";
import Trends from "@/components/Trends.vue";
import { onMounted, ref } from "vue";
import FeedItem from "@/components/FeedItem.vue";
import FeedForm from "@/components/FeedForm.vue";

const posts = ref([]);
const body = ref("");
const user = ref(null);

const getFeed = async () => {
  try {
    const { data } = await axios.get("/api/posts/");
    console.log("data", data);

    posts.value = data;
  } catch (error) {
    console.log("error", error);
  }
};

onMounted(getFeed);

const handlePostCreated = (post) => {
  posts.value.unshift(post);
};

const handlePostDeleted = (postId) => {
  posts.value = posts.value.filter((p) => p.id !== postId);
};
</script>

<template>
  <!-- This view represents the main feed page with a three-column layout. -->
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <!-- Center column: Post creation and feed -->
    <div class="main-center col-span-3 space-y-4">
      <!-- Post creation form -->
      <div class="bg-white border border-gray-200 rounded-lg">
        <FeedForm
          v-bind:user="user"
          v-bind:posts="posts"
          @post-created="handlePostCreated"
        />
      </div>

      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts"
        v-bind:key="post.id"
      >
        <FeedItem v-bind:post="post" @delete-post="handlePostDeleted" />
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
