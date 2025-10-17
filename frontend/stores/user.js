// Import Dependencies
import { defineStore } from "pinia";
import axios from "axios";

// Import Components

export const useUserStore = defineStore({
  id: "user",

  state: () => ({
    isAuthenticated: false,
    id: null,
    name: null,
    email: null,
    access: null,
    refresh: null,
  }),

  // Initialize Store and load Item from Local Storage
  actions: {
    initStore() {
      if (localStorage.getItem("user.access")) {
        this.user.access = localStorage.getItem("user.access");
        this.user.refresh = localStorage.getItem("user.refresh");
        this.user.id = localStorage.getItem("user.id");
        this.user.name = localStorage.getItem("user.name");
        this.user.email = localStorage.getItem("user.email");
        this.user.isAuthenticated = true;

        this.refreshToken();

        console.log("Initialized User", this.user);
      }
    },

    // Set JWT Access Token that you are Authenticated and save it in Localstorage
    setToken(data) {
      console.log("setToken", data);

      this.user.access = data.access;
      this.user.refresh = data.refresh;
      this.user.isAuthenticated = true;

      localStorage.setItem("user.access", data.access);
      localStorage.setItem("user.refresh", data.refresh);
    },

    // Remove JWT Tokens and User Data from Store and Localstorage
    removeToken() {
      console.log("removeToken");

      this.user.refresh = null;
      this.user.access = null;
      this.user.isAuthenticated = false;
      this.user.id = false;
      this.user.name = false;
      this.user.email = false;

      localStorage.setItem("user.access", "");
      localStorage.setItem("user.refresh", "");
      localStorage.setItem("user.id", "");
      localStorage.setItem("user.name", "");
      localStorage.setItem("user.email", "");
    },

    // Get Token from backend for Login User and save in Localstorage
    setUserInfo(user) {
      console.log("setUserInfo", user);

      this.user.id = user.id;
      this.user.name = user.name;
      this.user.email = user.email;

      localStorage.setItem("user.id", this.user.id);
      localStorage.setItem("user.name", this.user.name);
      localStorage.setItem("user.email", this.user.email);

      console.log("User", this.user);
    },

    // Refresh JWT Access Token
    refreshToken() {
      axios
        .post("/api/account/refresh/", {
          refresh: this.user.refresh,
        })

        .then((response) => {
          this.user.access = response.data.access;

          localStorage.setItem("user.access", response.data.access);

          axios.defaults.headers.common["Authorization"] =
            "Bearer " + response.data.access;
        })
        .catch((error) => {
          console.log(error);

          this.removeToken();
        });
    },
  },
});
