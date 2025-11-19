<script setup>
// Import Dependencies
import axios from "axios";
import { onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

// Import components.
import PeopleYouKnow from "@/components/PeopleYouKnow.vue";
import Trends from "@/components/Trends.vue";
import { useUserStore } from "@/stores/user";
import { useToastStore } from "@/stores/toast";
import FeedItem from "@/components/FeedItem.vue";
import FeedForm from "@/components/FeedForm.vue";

const posts = ref([]);
const user = ref(null);
const route = useRoute();
const router = useRouter();
const userStore = useUserStore();
const toastStore = useToastStore();
const can_send_friendship_request = ref(null);

const getFeed = async () => {
  try {
    const { data } = await axios.get(`/api/posts/profile/${route.params.id}`);
    console.log("data", data);

    posts.value = data.posts || [];
    user.value = data.user || null;
    can_send_friendship_request.value = data.can_send_friendship_request;
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

const handlePostCreated = (post) => {
  posts.value.unshift(post);
  if (user.value) {
    user.value.posts_count = (user.value.posts_count || 0) + 1;
  }
};

const sendFriendshipRequest = async () => {
  try {
    const { data } = await axios.post(
      `/api/friends/send-request/${route.params.id}/`
    );
    console.log("data", data);

    const message = data?.message ?? "Friend request updated";
    const isAlreadySent = message.toLowerCase().includes("already");
    const bgClass = isAlreadySent ? "bg-yellow-300" : "bg-emerald-300";

    toastStore.showToast(5000, message, bgClass);
  } catch (error) {
    console.log("error", error);

    const message =
      error.response?.data?.message ?? "Unable to send friend request";

    toastStore.showToast(5000, message, "bg-red-300");
  }
};

const sendDirectMessage = async () => {
  try {
    console.log("sendDirectMessage");
    const { data } = await axios.get(
      `/api/chat/${route.params.id}/get-or-create/`
    );
    console.log("data", data);
    router.push("/chat");
  } catch (error) {
    console.log("error", error);
  }
};

const logout = async () => {
  try {
    console.log("Log out");

    userStore.removeToken();
    router.push("/login");
  } catch (error) {
    console.log("error", error);
  }
};

const deletePost = (id) => {
  posts.value = posts.value.filter((post) => post.id !== id);
  if (user.value && userStore.id === user.value.id) {
    user.value.posts_count = Math.max(0, (user.value.posts_count || 1) - 1);
  }
};

const reportPost = async (id) => {
  try {
  } catch (error) {
    console.log("error", error);
    toastStore.showToast(5000, "Unable to report post", "bg-red-300");
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
        <img
          :src="user?.get_avatar ?? 'https://i.pravatar.cc/300?img=70'"
          class="mb-6 rounded-full"
        />

        <!-- User name -->
        <p>
          <strong>{{ user?.name ?? "" }}</strong>
        </p>

        <!-- User stats: friends and posts count -->
        <div v-if="user" class="mt-6 flex space-x-8 justify-around">
          <RouterLink
            :to="{ name: 'friends', params: { id: user.id } }"
            class="text-xs text-gray-500"
            >{{ user?.friends_count ?? 0 }} friends</RouterLink
          >
          <p class="text-xs text-gray-500">
            {{ user?.posts_count ?? 0 }} posts
          </p>
        </div>

        <div class="mt-6">
          <button
            v-if="userStore.id && user && userStore.id !== user.id"
            class="inline-block py-1 px-3 bg-purple-600 text-xs text-white rounded-lg"
            @click="sendFriendshipRequest"
          >
            Send Friend Request
          </button>

          <button
            v-if="userStore.id && user && userStore.id !== user.id"
            class="inline-block py-1 px-3 bg-purple-600 text-xs text-white rounded-lg"
            @click="sendDirectMessage"
          >
            Send direct Message
          </button>

          <RouterLink
            to="/profile/edit"
            v-if="userStore.id && user && userStore.id === user.id"
            class="inline-block py-1 px-1 bg-gray-600 text-xs text-white rounded-lg mr-10"
          >
            Edit Profile
          </RouterLink>

          <button
            v-if="userStore.id && user && userStore.id === user.id"
            class="inline-block py-1 px-3 bg-red-600 text-xs text-white rounded-lg cursor-pointer"
            @click="logout"
          >
            Log out
          </button>
        </div>
      </div>
    </div>

    <!-- Center column: Post creation and feed -->
    <div class="main-center col-span-2 space-y-4">
      <!-- Post creation form -->
      <div
        class="bg-white border border-gray-200 rounded-lg"
        v-if="userStore.id && user && userStore.id === user.id"
      >
        <FeedForm
          v-bind:user="user"
          v-bind:posts="posts"
          @post-created="handlePostCreated"
        />
      </div>

      <!-- Second post in the feed (static placeholder) -->
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts"
        v-bind:key="post.id"
      >
        <FeedItem v-bind:post="post" @delete-post="deletePost" />
      </div>
    </div>

    <!-- Right column: "People you may know" and "Trends" sections -->
    <div class="main-right col-span-1 space-y-4">
      <PeopleYouKnow />
      <Trends />
    </div>
  </div>
</template>
