<script setup>
// Import Dependencies
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

// Import components.
import PeopleYouKnow from "@/components/PeopleYouKnow.vue";
import Trends from "@/components/Trends.vue";
import { useUserStore } from "@/stores/user";

const user = ref(null);
const route = useRoute();
const friendshipRequest = [];
const friends = ref([]);

onMounted(getFriends);

const getFriends = async () => {
  try {
    const { data } = await axios.get(
      `/api/posts/profile/${route.params.id}/friends`
    );
    console.log("data", data);

    friendshipRequest = response.data.requests;
    friends.value = data.friends || [];
    user.value = data.user || null;
  } catch (error) {
    console.log("error", error);
  }
};

const sendFriendshipRequest = async () => {
  try {
    const { data } = await axios.post(
      `/api/friends/send-request/${route.params.id}/`
    );
    console.log("data", data);
  } catch (error) {
    console.log("error", error);
  }
};
</script>

<template>
  <!-- This view represents the main feed page with a three-column layout. -->
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <!-- Left column: User profile information -->
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
        <!-- User avatar -->
        <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full" />

        <!-- User name -->
        <p>
          <strong>{{ user?.name ?? "" }}</strong>
        </p>

        <!-- User stats: friends and posts count -->
        <div class="mt-6 flex space-x-8 justify-around">
          <p class="text-xs text-gray-500">182 friends</p>
          <p class="text-xs text-gray-500">120 posts</p>
        </div>
      </div>
    </div>

    <!-- Center column: Post creation and feed -->
    <div class="main-center col-span-2 space-y-4">Friends</div>

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
