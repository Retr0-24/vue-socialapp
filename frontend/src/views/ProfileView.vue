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

const posts = ref([]);
const user = ref(null);
const body = ref("");
const route = useRoute();
const router = useRouter();
const userStore = useUserStore();
const toastStore = useToastStore();
const fileInput = ref(null);
const url = ref(null);
const can_send_friendship_request = ref(null);
const is_private = ref(false);

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

const submitForm = async () => {
  console.log("submitForm", body.value);
  const formData = new FormData();
  formData.append("body", body.value);
  formData.append("is_private", is_private.value);

  const file = fileInput.value?.files?.[0];
  if (file) {
    formData.append("image", file);
  }

  try {
    const { data } = await axios.post("/api/posts/create/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    console.log("data", data);

    posts.value.unshift(data);
    body.value = "";
    is_private.value = false;
    url.value = null;
    if (fileInput.value) {
      fileInput.value.value = "";
    }

    if (user.value) {
      user.value.posts_count = (user.value.posts_count || 0) + 1;
    }
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

const onFileChange = async (e) => {
  const file = e.target.files?.[0];
  url.value = file ? URL.createObjectURL(file) : null;
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
        <form v-on:submit.prevent="submitForm" method="post">
          <div class="p-4">
            <div id="preview" v-if="url">
              <img :src="url" class="w-full mb-5 rounded-lg" />
            </div>

            <textarea
              v-model="body"
              class="p-4 w-full bg-gray-100 rounded-lg"
              placeholder="What do you want to post?"
            ></textarea>

            <label>
              <input type="checkbox" class="m-1" v-model="is_private">Private</input>
            </label>
          </div>

          <div class="p-4 border-t border-gray-100 flex justify-between">
            <label
              class="inline-block py-4 px-2 bg-gray-600 text-white rounded-lg text-center cursor-pointer hover:bg-purple-600"
            >
              <input type="file" ref="fileInput" @change="onFileChange" />
              Attach Image
            </label>

            <button
              href="#"
              class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg cursor-pointer"
            >
              Post
            </button>
          </div>
        </form>
      </div>

      <!-- Second post in the feed (static placeholder) -->
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
input[type="file"] {
  display: none;
}
</style>
