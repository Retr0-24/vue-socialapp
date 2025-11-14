<script setup>
// Import Dependencies
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

// Import components.
import PeopleYouKnow from "@/components/PeopleYouKnow.vue";
import Trends from "@/components/Trends.vue";

const user = ref(null);
const route = useRoute();
const friends = ref([]);
const friendshipRequest = ref([]);

const getFriends = async () => {
  try {
    const { data } = await axios.get(`/api/friends/${route.params.id}`);
    console.log("data", data);

    friendshipRequest.value = data.requests || [];
    friends.value = data.friends || [];
    user.value = data.user || null;
  } catch (error) {
    console.log("error", error);
  }
};

onMounted(getFriends);


const handleRequest = async (status, pk) => {
  console.log('handleRequest', status)
  try {
    const { data } = await axios.post(
      `/api/friends/${pk}/${status}/`,
    );
    console.log("data", data);

  } catch (error) {
    console.log("error", error);
  }
}
</script>

<template>
  <!-- This view represents the main feed page with a three-column layout. -->
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <!-- Left column: User profile information -->
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
        <!-- User avatar -->
        <img
          :src="user?.get_avatar ?? 'https://i.pravatar.cc/300?img=70'"
          class="mb-6 rounded-full"
        />

        <!-- User name -->
        <p>
          <strong>{{ user?.name ?? "" }}</strong>
        </p>

        <!-- User stats: friends and posts count -->
        <div class="mt-6 flex space-x-8 justify-around" v-if="user">
          <p class="text-xs text-gray-500">{{ user?.friends_count ?? 0 }} friends</p>
            <p class="text-xs text-gray-500">{{ user?.posts_count ?? 0 }} posts</p>
        </div>
      </div>
    </div>

    <!-- Center column: Post creation and feed -->
    <div class="main-center col-span-2 space-y-4">
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-if="friendshipRequest.length"
      >
        <h2 class="text-xl mb-6 font-bold">Friendship Requests</h2>
        <div
          class="p-4 text-center bg-gray-100 rounded-lg mx-auto"
          v-for="friendshipRequests in friendshipRequest"
          v-bind:key="friendshipRequests.id"
        >
          <img
            :src="friendshipRequests.created_by.get_avatar"
            class="mb-6 rounded-full"
          />
          <p>
            <strong>
              <RouterLink :to="{ name: 'profile', params: { id: friendshipRequests.created_by.id } }">
                {{ friendshipRequests.created_by.name }}
              </RouterLink>
            </strong>
          </p>
          <div class="mt-6 flex space-x-8 justify-around">
            <p class="text-xs text-gray-500">
              {{ friendshipRequests.created_by?.friends_count ?? 0 }} friends
            </p>
            <p class="text-xs text-gray-500">{{ user?.posts_count ?? 0 }} posts</p>
          </div>
          <div class="mt-6 space-x-4">
              <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg" @click="handleRequest('accepted', friendshipRequests.created_by.id)">Accept</button>
              <button class="inline-block py-4 px-6 bg-red-600 text-white rounded-lg" @click="handleRequest('rejected', friendshipRequests.created_by.id)">Deny</button>
            </div>
        </div>
        <hr>
        </hr>
      </div>


      <div
        class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-2 gap-4"
        v-if="friends.length"
      >
        <div
          class="p-4 text-center bg-gray-100 rounded-lg"
          v-for="friend in friends"
          v-bind:key="friend.id"
        >
          <img
            :src="friend?.get_avatar ?? 'https://i.pravatar.cc/300?img=70'"
            class="mb-6 rounded-full"
          />
          <p>
            <strong>
              <RouterLink :to="{ name: 'profile', params: { id: friend.id } }">
                {{ friend.name }}
              </RouterLink>
            </strong>
          </p>
          <div class="mt-6 flex space-x-8 justify-around">
            <p class="text-xs text-gray-500">{{ friend.friends_count }} friends</p>
            <p class="text-xs text-gray-500">120 posts</p>
          </div>
        </div>
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
