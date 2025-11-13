<script setup>
// Import Dependencies
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

// Import components.
import PeopleYouKnow from "@/components/PeopleYouKnow.vue";
import Trends from "@/components/Trends.vue";
import FeedItem from "@/components/FeedItem.vue";
import CommentItem from "@/components/CommentItem.vue";

const post = ref({ comments: [] });
const route = useRoute();
const body = ref("");
const comments = ref([]);

const getPost = async () => {
  try {
    const { data } = await axios.get(`/api/posts/${route.params.id}/`);
    console.log("data", data);

    post.value = {
      comments: [],
      ...data.post,
      comments: data.post?.comments ?? [],
    };
  } catch (error) {
    console.log("error", error);
  }
};

onMounted(getPost);

const submitForm = async () => {
  console.log("submitForm", body.value);

  try {
    const { data } = await axios.post(
      `/api/posts/${route.params.id}/comment/`,
      {
        body: body.value,
      }
    );
    console.log("data", data);

    if (!Array.isArray(post.value.comments)) {
      post.value.comments = [];
    }

    post.value.comments.push(data);
    post.value.comments_count += 1;
    body.value = "";
  } catch (error) {
    console.log("error", error);
  }
};
</script>

<template>
  <!-- This view represents the main feed page with a three-column layout. -->
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <!-- Center column: Post creation and feed -->
    <div class="main-center col-span-3 space-y-4">
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-if="post.id"
      >
        <FeedItem v-bind:post="post" />
      </div>

      <div
        class="p-4 ml-6 bg-white border border-gray-200 rounded-lg"
        v-for="comment in post.comments"
        v-bind:key="comment.id"
      >
        <CommentItem v-bind:comment="comment" />
      </div>

      <div class="bg-white border border-gray-200 rounded-lg">
        <form v-on:submit.prevent="submitForm" method="post">
          <div class="p-4">
            <textarea
              v-model="body"
              class="p-4 w-full bg-gray-100 rounded-lg"
              placeholder="What do you think about this post?"
            ></textarea>
          </div>
          <div class="p-4 border-t border-gray-100">
            <button
              href="#"
              class="inline-block py-2 px-4 bg-purple-600 text-white rounded-lg hover:bg-black hover:text-white"
            >
              Comment
            </button>
          </div>
        </form>
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
