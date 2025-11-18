// Import Dependencies
import { createApp } from "vue"; // Vue's function to create a new application instance.
import { createPinia } from "pinia"; // Pinia's function to create a new store instance.
import axios from "axios"; // HTTP client for making API requests.
import App from "./App.vue"; // The root component of the application.
import router from "./router"; // The Vue Router instance.

// Import the main stylesheet for the application.
import "./assets/main.css";

// Create the Vue application instance.
const app = createApp(App);

// Create the Pinia store instance.
const pinia = createPinia();

// Set the base URL for all Axios requests.
axios.defaults.baseURL = import.meta.env.VITE_API_URL;

// Use the Pinia store and Vue Router with the application instance.
app.use(pinia);
app.use(router);

// Make Axios available globally throughout the application.
app.config.globalProperties.$axios = axios;

// Mount the application to the DOM element with the ID "app".
app.mount("#app");
