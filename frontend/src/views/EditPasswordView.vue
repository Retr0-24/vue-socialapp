<script setup>
// Import Dependencies
import axios from "axios";
import { reactive, ref } from "vue";
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

const toastStore = useToastStore();
const userStore = useUserStore();
const errors = ref([]);
const router = useRouter();

const form = reactive({
  old_password: "",
  new_password: "",
  new_password_confirm: "",
});

const submitForm = async () => {
  errors.value = [];

  if (form.old_password === "") {
    errors.value.push("Password is required.");
  }
  if (form.new_password === "") {
    errors.value.push("New password is required.");
  }
  if (form.new_password_confirm === "") {
    errors.value.push("Please confirm your new password.");
  }
  if (form.new_password !== form.new_password_confirm) {
    errors.value.push("Passwords do not match.");
  }

  // If there are no validation errors, proceed with the API call.
  if (errors.value.length === 0) {
    const formData = new FormData();
    formData.append("old_password", form.old_password);
    formData.append("new_password1", form.new_password);
    formData.append("new_password2", form.new_password_confirm);

    try {
      // Send a POST request to the edit password endpoint.
      const { data } = await axios.post("/api/editpassword/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      // If editprofile is successful, show a success toast and clear the form.
      if (data.message === "Success") {
        toastStore.showToast(
          5000,
          "Your password was updated successfully.",
          "bg-emerald-500"
        );

        router.push(`/profile/${userStore.id}`);
      } else {
        try {
          const parsed =
            typeof data.message === "string"
              ? JSON.parse(data.message)
              : data.message;

          for (const key in parsed) {
            errors.value.push(parsed[key][0].message);
          }
        } catch (parseError) {
          toastStore.showToast(
            5000,
            "Unable to parse server response.",
            "bg-red-300"
          );
        }
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
        <h1 class="mb-6 text-2xl">Update Password</h1>
        <p class="mb-6 text-gray-500">
          Update your Password. At least 8 Characters Long. For Security Reasons
          you should have at least one Number, One Uppercase and one Lowercase
          letter and Special Characters like '$,/,#,\,^,{},(),[],*'.
        </p>
      </div>
    </div>

    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" @submit.prevent="submitForm">
          <!-- Old Password input field -->
          <div>
            <label>Old Password</label><br />
            <input
              type="password"
              v-model="form.old_password"
              placeholder="Your Current Password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>
          <!-- New Password input field -->
          <div>
            <label>New Password</label><br />
            <input
              type="password"
              v-model="form.new_password"
              placeholder="Your New Password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>
          <!-- Confirm Password input field -->
          <div>
            <label>Confirm Password</label><br />
            <input
              type="password"
              v-model="form.new_password_confirm"
              placeholder="Confirm New Password"
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
              Update Password
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
