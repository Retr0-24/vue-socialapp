<script setup></script>


<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <!-- Login Text Fields -->
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Log in</h1>
        <p class="mb-6 text-gray-500">
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum
          dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
        </p>
        <p class="font-bold">
          Don't have an account?
          <RouterLink to="/signup" class="underline">Click here</RouterLink> to create an Account!
        </p>
      </div>
    </div>
    <!-- Login Input Fields -->
    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6">
            <div>
                <label>E-mail</label><br>
                <input type="email" placeholder="Your E-Mail" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
            </div>
            <div>
                <label>Password</label><br>
                <input type="password" placeholder="Your Password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"></input>
            </div>
            <div>
                <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Login</button>
            </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped></style>

