// Import Dependencies
import { createApp } from "vue";
import { createPinia } from "pinia";
import axios from "axios";
import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

const app = createApp(App);
const pinia = createPinia();

axios.defaults.baseURL = "http://127.0.0.1:8000";

app.use(pinia);
app.use(router);

app.config.globalProperties.$axios = axios;

app.mount("#app");
