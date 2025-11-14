<script setup>
// Import Dependencies
import axios from "axios";
import { reactive, ref, watch } from "vue";
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

const toastStore = useToastStore();
const userStore = useUserStore();
const errors = ref([]);
const router = useRouter();

const fileInput = ref(null);

const form = reactive({
  name: userStore.name ?? "",
  email: userStore.email ?? "",
});

watch(
  () => [userStore.name, userStore.email],
  ([name, email]) => {
    form.name = name ?? "";
    form.email = email ?? "";
  },
  { immediate: true }
);

const handleFileChange = (event) => {
  const files = event?.target?.files || [];
  form.avatar = files[0] ?? null;
};

const submitForm = async () => {
  errors.value = [];

  if (form.name === "") {
    errors.value.push("Name is required.");
  }
  if (form.email === "") {
    errors.value.push("Email is required.");
  }

  // If there are no validation errors, proceed with the API call.
  if (errors.value.length === 0) {
    const formData = new FormData();
    if (form.avatar) {
      formData.append("avatar", form.avatar);
    }
    formData.append("name", form.name);
    formData.append("email", form.email);

    try {
      // Send a POST request to the editprofile endpoint.
      const { data } = await axios.post("/api/editprofile/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      // If editprofile is successful, show a success toast and clear the form.
      if (data.message === "Profile updated") {
        toastStore.showToast(
          5000,
          "Your Profile updated successfully.",
          "bg-emerald-500"
        );

        if (data.user) {
          userStore.setUserInfo(data.user);
        } else {
          userStore.setUserInfo({
            id: userStore.id,
            name: form.name,
            email: form.email,
            avatar: userStore.avatar,
          });
        }

        router.back();
      } else {
        toastStore.showToast(
          5000,
          "There was an error while trying to update your Profile. Please try with another email.",
          "bg-red-300"
        );
      }
    } catch (error) {
      console.log("error", error);

      const message =
        error.response?.data?.message ?? "Unable to save changes right now.";

      toastStore.showToast(5000, message, "bg-red-300");
    }
  }
};
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Edit Profile</h1>
        <p class="mb-6 text-gray-500">
          Edit your Profile like you want! Insert and Avatar, change your name
          or update your password and email. All in one place! :)
        </p>

        <RouterLink
          to="/profile/edit/password"
          class="inline-block py-1 px-3 bg-purple-600 text-xs text-white rounded-lg"
        >
          Change Password
        </RouterLink>
      </div>
    </div>

    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" @submit.prevent="submitForm">
          <!-- Avatar input field -->
          <div>
            <label>Avatar</label><br />
            <input
              type="file"
              ref="fileInput"
              @change="handleFileChange"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <!-- Name input field -->
          <div>
            <label>Name</label><br />
            <input
              type="text"
              v-model="form.name"
              placeholder="Your Full Name"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <!-- Email input field -->
          <div>
            <label>E-mail</label><br />
            <input
              type="email"
              v-model="form.email"
              placeholder="Your E-Mail"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <!-- Display error messages if any -->
          <template v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>
          </template>

          <!-- Submit button -->
          <div>
            <button
              class="py-4 px-6 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
            >
              Save changes
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
