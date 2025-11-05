// Import Dependencies
import { defineStore } from "pinia";
import axios from "axios";

// Import Components

export const useUserStore = defineStore("user", {
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
      const access = localStorage.getItem("user.access");
      if (access) {
        this.access = access;
        this.refresh = localStorage.getItem("user.refresh");
        this.id = localStorage.getItem("user.id");
        this.name = localStorage.getItem("user.name");
        this.email = localStorage.getItem("user.email");
        this.isAuthenticated = true;

        axios.defaults.headers.common["Authorization"] = `Bearer ${this.access}`;

        this.refreshToken();

        console.log("Initialized User", {
          id: this.id,
          email: this.email,
        });
      }
    },

    // Set JWT Access Token that you are Authenticated and save it in Localstorage
    setToken(data) {
      console.log("setToken", data);

      this.access = data.access;
      this.refresh = data.refresh;
      this.isAuthenticated = true;

      axios.defaults.headers.common["Authorization"] = `Bearer ${data.access}`;

      localStorage.setItem("user.access", data.access);
      localStorage.setItem("user.refresh", data.refresh);
    },

    // Remove JWT Tokens and User Data from Store and Localstorage
    removeToken() {
      console.log("removeToken");

      this.refresh = null;
      this.access = null;
      this.isAuthenticated = false;
      this.id = null;
      this.name = null;
      this.email = null;

      delete axios.defaults.headers.common["Authorization"];

      localStorage.removeItem("user.access");
      localStorage.removeItem("user.refresh");
      localStorage.removeItem("user.id");
      localStorage.removeItem("user.name");
      localStorage.removeItem("user.email");
    },

    // Get Token from backend for Login User and save in Localstorage
    setUserInfo(user) {
      console.log("setUserInfo", user);

      this.id = user.id;
      this.name = user.name;
      this.email = user.email;

      localStorage.setItem("user.id", this.id ?? "");
      localStorage.setItem("user.name", this.name ?? "");
      localStorage.setItem("user.email", this.email ?? "");

      console.log("User", {
        id: this.id,
        name: this.name,
        email: this.email,
      });
    },

    // Refresh JWT Access Token
    refreshToken() {
      if (!this.refresh) {
        return;
      }

      axios
        .post("/api/account/refresh/", {
          refresh: this.refresh,
        })

        .then((response) => {
          this.access = response.data.access;

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
