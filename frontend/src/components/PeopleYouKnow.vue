<script setup>
// Import Dependencies
import axios from "axios";
import { ref, onMounted } from "vue";

// Import Components

const users = ref([]);

const getFriendSuggestions = async () => {
  try {
    const { data } = await axios.get("/api/friends/suggested/");
    console.log("data", data);
    users.value = data;
  } catch (error) {
    console.log(error);
  }
};

onMounted(getFriendSuggestions);
</script>

<template>
  <!-- This component displays a "People you may know" section. -->
  <div class="p-4 bg-white border border-gray-200 rounded-lg">
    <h3 class="mb-6 text-xl">People you may know</h3>

    <div class="space-y-4" v-if="users.length">
      <div
        class="flex items-center justify-between"
        v-for="user in users"
        v-bind:key="user.id"
      >
        <div class="flex items-center space-x-2">
          <img :src="user.get_avatar" class="w-[40px] rounded-full" />
          <p class="text-xs"><strong>{{ user.name }}</strong></p>
        </div>
        <RouterLink
          :to="{ name: 'profile', params: { id: user.id } }"
          class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg"
        >
          Show
        </RouterLink>
      </div>
    </div>

    <p v-else class="text-sm text-gray-500">No suggestions at the moment.</p>
  </div>
</template>

<style scoped></style>
