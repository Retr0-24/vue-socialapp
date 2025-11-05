<script setup>
// This component does not have any script logic.
</script>

<template>
  <!-- This view represents the messages page with a two-column layout. -->
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <!-- Left column: List of message proposals (conversations) -->
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <div class="space-y-4">
          <!-- Each of these is a static placeholder for a conversation. -->
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <img
                src="https://i.pravatar.cc/300?img=70"
                class="w-[40px] rounded-full"
              />
              <p class="text-xs"><strong>Placeholder Name</strong></p>
            </div>
            <span class="text-xs text-gray-500">13 minutes ago</span>
          </div>
          <!-- More placeholder conversations... -->
        </div>
      </div>
    </div>

    <!-- Right column: Main message area -->
    <div class="main-center col-span-3 space-y-4">
      <!-- Message history -->
      <div class="bg-white border border-gray-200 rounded-lg">
        <div class="flex flex-col flex-grow p-4">
          <!-- Sent message (right side) -->
          <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
            <div>
              <div
                class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg"
              >
                <p class="text-sm">
                  This is a placeholder for a sent message.
                </p>
              </div>
              <span class="text-xs text-gray-500 leading-none">2 min ago</span>
            </div>
            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
              <img
                src="https://i.pravatar.cc/300?img=70"
                class="w-[40px] rounded-full"
              />
            </div>
          </div>

          <!-- Received message (left side) -->
          <div class="flex w-full mt-2 space-x-3 max-w-md">
            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
              <img
                src="https://i.pravatar.cc/300?img=70"
                class="w-[40px] rounded-full"
              />
            </div>
            <div>
              <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                <p class="text-sm">
                  This is a placeholder for a received message.
                </p>
              </div>
              <span class="text-xs text-gray-500 leading-none">1 min ago</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Message input form -->
      <div class="bg-white border border-gray-200 rounded-lg">
        <div class="p-4">
          <textarea
            class="p-4 w-full bg-gray-100 rounded-lg"
            placeholder="Insert Message"
          ></textarea>
        </div>
        <div class="p-4 border-t border-gray-100 flex justify-between">
          <a
            href="#"
            class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
            >Send</a
          >
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Scoped styles for this component can be added here. */
</style>
