<script setup>
// Import Dependencies
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

// Import Components

const notifications = ref([]);
const router = useRouter();

const getNotifications = async () => {
  try {
    const { data } = await axios.get("/api/notifications/");
    notifications.value = data;
  } catch (error) {
    console.log("error", error);
  }
};

const readNotification = async (notification) => {
  console.log("readNotification", notification.id);
  try {
    const { data } = await axios.post(
      `/api/notifications/read/${notification.id}/`
    );
    console.log("data", data);

    if (
      notification.type_of_notification == "post_like" ||
      notification.type_of_notification == "post_comment"
    ) {
      router.push({ name: "postview", params: { id: notification.post_id } });
    } else {
      router.push({
        name: "friends",
        params: { id: notification.created_for_id },
      });
    }
  } catch (error) {
    console.log("error", error);
  }
};

onMounted(getNotifications);
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="notification in notifications"
        v-bind:key="notification.id"
        v-if="notifications.length"
      >
        {{ notification.body }}

        <button
          class="underline cursor-pointer"
          @click="readNotification(notification)"
        >
          Read more
        </button>
      </div>

      <div class="p-4 bg-white border border-gray-200 rounded-lg" v-else>
        You don't have any unread notifications.
      </div>
    </div>
  </div>
</template>

<style scoped></style>
