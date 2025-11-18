<script setup>
    // Import Dependencies
import { ref } from "vue";
import axios from "axios";

    // Import Components

const is_private = ref(false);
const body = ref("");
const fileInput = ref(null);
const url = ref(null);

const props = defineProps({
    user: Object,
    // The parent owns the posts array; we emit new posts instead of mutating the prop.
    posts: Array,
});

const emit = defineEmits(["post-created"]);

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

    emit("post-created", data);
    body.value = "";
    is_private.value = false;
    url.value = null;
    if (fileInput.value) {
      fileInput.value.value = "";
    }

    // The parent can optionally update counts when it receives the post-created event.
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
</template>

<style scoped>
input[type="file"] {
  display: none;
}
</style>
