<script setup>
// This component does not have any script logic.
</script>

<template>
  <!-- This component displays a "People you may know" section. -->
  <div class="p-4 bg-white border border-gray-200 rounded-lg">
    <h3 class="mb-6 text-xl">People you may know</h3>

    <!-- The list of people is currently static with placeholder data. -->
    <div class="space-y-4">
      <!-- First person entry -->
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <!-- Placeholder image for the user's avatar. -->
          <img
            src="https://i.pravatar.cc/300?img=70"
            class="w-[40px] rounded-full"
          />
          <!-- Placeholder for the user's name. -->
          <p class="text-xs"><strong>Placeholder Name</strong></p>
        </div>
        <!-- A link to view the user's profile. -->
        <a
          href="#"
          class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg"
          >Show</a
        >
      </div>

      <!-- Second person entry -->
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <img
            src="https://i.pravatar.cc/300?img=70"
            class="w-[40px] rounded-full"
          />
          <p class="text-xs"><strong>Placeholder Name</strong></p>
        </div>
        <a
          href="#"
          class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg"
          >Show</a
        >
      </div>

      <!-- Third person entry -->
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <img
            src="https://i.pravatar.cc/300?img=70"
            class="w-[40px] rounded-full"
          />
          <p class="text-xs"><strong>Placeholder Name</strong></p>
        </div>
        <a
          href="#"
          class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg"
          >Show</a
        >
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Scoped styles for this component can be added here. */
</style>
