<script setup>
// Import Dependencies
import { computed, ref, toRefs } from "vue";
import { RouterLink } from "vue-router";
import axios from "axios";

// Import Components
import { useUserStore } from "@/stores/user";
import { useToastStore } from "@/stores/toast";

// Accept a post to display.
const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
});

const { post } = toRefs(props);
const showExtraModal = ref(false);
const userStore = useUserStore();
const toastStore = useToastStore();
const emit = defineEmits(["delete-post"]);
const canManagePost = computed(() => {
  const currentUserId = userStore.id;
  const postOwnerId = post.value?.created_by?.id;

  if (!currentUserId || !postOwnerId) {
    return false;
  }

  return currentUserId === postOwnerId;
});

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

const toggleExtraModal = () => {
  showExtraModal.value = !showExtraModal.value;
};

const deletePost = async () => {
  try {
    const { data } = await axios.delete(`/api/posts/${post.value.id}/delete/`);
    console.log("data", data);
    emit("delete-post", post.value.id);

    const message = data?.message ?? "This post has been deleted.";
    toastStore.showToast(5000, message, "bg-emerald-500");
  } catch (error) {
    console.log("error", error);

    const message =
      error.response?.data?.message ?? "Unable to delete this post.";
    toastStore.showToast(5000, message, "bg-red-300");
  }
};

const reportPost = async () => {
  console.log("reportPost:", post.value.id);
  try {
    const { data } = await axios.post(`/api/posts/${post.value.id}/report/`);
    console.log("data", data);

    const message = data?.message ?? "This post has been reported.";
    toastStore.showToast(5000, message, "bg-emerald-500");
  } catch (error) {
    console.log("error", error);

    const message =
      error.response?.data?.message ?? "Unable to report this post.";
    toastStore.showToast(5000, message, "bg-red-300");
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
          class="w-6 h-6 hover:text-red-600 cursor-pointer"
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
          class="w-6 h-6 hover:text-purple-600 cursor-pointer"
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
    <!-- Modal button -->
    <div>
      <div @click="toggleExtraModal" class="cursor-pointer">
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
  </div>

  <div v-if="showExtraModal">
    <div class="flex space-x-6 items-center">
      <div
        class="flex items-center space-x-2 cursor-pointer"
        @click="deletePost"
        v-if="canManagePost"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="hover:text-orange-600 w-6 h-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
          />
        </svg>
        <span class="text-gray-500 text-xs">Delete Post</span>
      </div>

      <div
        class="flex items-center space-x-2 cursor-pointer"
        @click="reportPost"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="hover:text-red-600 w-6 h-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z"
          />
        </svg>
        <span class="text-gray-500 text-xs">Report Post</span>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
