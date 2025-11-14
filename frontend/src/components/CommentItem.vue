<script setup>
// Import Dependencies
import { toRefs } from "vue";
import { RouterLink } from "vue-router";

// Accept a post to display.
const props = defineProps({
  comment: {
    type: Object,
    required: true,
  },
});

const { post } = toRefs(props);
</script>

<template>
  <div class="mb-6 flex items-center justify-between">
    <div class="flex items-center space-x-6">
      <img :src="comment.created_by.get_avatar" class="w-[40px] rounded-full" />
      <p>
        <strong>
          <RouterLink
            :to="{ name: 'profile', params: { id: comment.created_by.id } }"
          >
            {{ comment.created_by.name }}
          </RouterLink>
        </strong>
      </p>
    </div>
    <p class="text-gray-600">{{ comment.created_at_formatted }}</p>
  </div>

  <!-- Post content with text -->
  <p>
    {{ comment.body }}
  </p>
</template>

<style scoped></style>
