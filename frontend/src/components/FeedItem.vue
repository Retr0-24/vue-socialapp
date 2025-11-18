<script setup>
// Import Dependencies
import { toRefs } from "vue";
import { RouterLink } from "vue-router";
import axios from "axios";

// Accept a post to display.
const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
});

const { post } = toRefs(props);

const likePost = async () => {
  if (!post.value) {
    return;
  }

  try {
    const { data } = await axios.post(`/api/posts/${post.value.id}/like/`);
    console.log("data", data);

    if (data?.message === "Liked") {
      post.value.likes_count = (post.value.likes_count || 0) + 1;
    }
  } catch (error) {
    console.log("error", error);
  }
};
</script>

<template>
  <div class="mb-6 flex items-center justify-between">
    <div class="flex items-center space-x-6">
      <img :src="post.created_by.get_avatar" class="w-[40px] rounded-full" />
      <p>
        <strong>
          <RouterLink
            :to="{ name: 'profile', params: { id: post.created_by.id } }"
          >
            {{ post.created_by.name }}
          </RouterLink>
        </strong>
      </p>
    </div>
    <p class="text-gray-600">{{ post.created_at_formatted }}</p>
  </div>

  <template v-if="post.attachments.length">
    <img
      v-for="image in post.attachments"
      v-bind:key="image.id"
      :src="image.get_image"
      class="rounded-xl mb-3 w-full"
    />
  </template>
  <!-- Post content with text -->
  <p>
    {{ post.body }}
  </p>

  <!-- Post actions: likes and comments -->
  <div class="my-6 flex justify-between">
    <div class="flex space-x-6">
      <div class="flex items-center space-x-2" @click="likePost">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-6 h-6 hover:text-red-600"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"
          />
        </svg>
        <span class="text-gray-500 text-xs">{{ post.likes_count }} likes</span>
      </div>
      <div class="flex items-center space-x-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-6 h-6 hover:text-purple-600"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z"
          />
        </svg>
        <RouterLink
          :to="{ name: 'postview', params: { id: post.id } }"
          class="text-gray-500 text-xs hover:text-purple-600"
          >{{ post.comments_count }} comments</RouterLink
        >
      </div>

      <div v-if="post.is_private" class="flex items-center space-x-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          stroke-width="1.5"
          stroke="currentColor"
          viewBox="0 0 24 24"
          class="hover:text-purple-600 w-6 h-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"
          />
        </svg>
        <span class="text-xs text-gray-500">Private</span>
      </div>
    </div>
    <!-- More options button -->
    <div>
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
          d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"
        />
      </svg>
    </div>
  </div>
</template>

<style scoped></style>
