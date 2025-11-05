import { createRouter, createWebHistory } from "vue-router";

// Define the application's routes.
const routes = [
  {
    path: "/", // The URL path for the route.
    name: "home", // The name of the route for programmatic navigation.
    // The component to render for this route, lazy-loaded for better performance.
    component: () => import("../views/HomeView.vue"),
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import("../views/SignUpView.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../views/LoginView.vue"),
  },
  {
    path: "/feed",
    name: "feed",
    component: () => import("../views/FeedView.vue"),
  },
  {
    path: "/messages",
    name: "messages",
    component: () => import("../views/MessagesView.vue"),
  },
  {
    path: "/search",
    name: "search",
    component: () => import("../views/SearchView.vue"),
  },
  {
    // This is a catch-all route for any paths that don't match the defined routes.
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("../views/NotFoundView.vue"),
  },
];

// Create the router instance.
const router = createRouter({
  // Use HTML5 history mode for clean URLs.
  history: createWebHistory(),
  // The defined routes for the application.
  routes,
});

// Export the router instance to be used in the main application file.
export default router;
