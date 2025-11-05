// Import Dependencies
import { defineStore } from "pinia"; // Pinia's function to create a new store.
import axios from "axios"; // HTTP client for making API requests.

/**
 * `useUserStore` is a Pinia store for managing user-related state,
 * including authentication status, user information, and JWT tokens.
 */
export const useUserStore = defineStore("user", {
  // The state is a function that returns an object of reactive properties.
  state: () => ({
    isAuthenticated: false, // Tracks if the user is authenticated.
    id: null, // User's unique identifier.
    name: null, // User's name.
    email: null, // User's email address.
    access: null, // JWT access token.
    refresh: null, // JWT refresh token.
  }),

  // Actions are methods that can be called to modify the state.
  actions: {
    /**
     * Initializes the user store from data saved in local storage.
     * This is used to persist the user's session across page reloads.
     */
    initStore() {
      const access = localStorage.getItem("user.access");
      if (access) {
        this.access = access;
        this.refresh = localStorage.getItem("user.refresh");
        this.id = localStorage.getItem("user.id");
        this.name = localStorage.getItem("user.name");
        this.email = localStorage.getItem("user.email");
        this.isAuthenticated = true;

        // Set the Authorization header for all subsequent Axios requests.
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${this.access}`;

        // Attempt to refresh the access token to ensure it's not expired.
        this.refreshToken();

        console.log("Initialized User", {
          id: this.id,
          email: this.email,
        });
      }
    },

    /**
     * Sets the JWT access and refresh tokens, marks the user as authenticated,
     * and saves the tokens to local storage.
     * @param {object} data - An object containing the access and refresh tokens.
     */
    setToken(data) {
      console.log("setToken", data);

      this.access = data.access;
      this.refresh = data.refresh;
      this.isAuthenticated = true;

      // Set the Authorization header for future Axios requests.
      axios.defaults.headers.common["Authorization"] = `Bearer ${data.access}`;

      // Store tokens in local storage for persistence.
      localStorage.setItem("user.access", data.access);
      localStorage.setItem("user.refresh", data.refresh);
    },

    /**
     * Removes all user-related data from the store and local storage,
     * effectively logging the user out.
     */
    removeToken() {
      console.log("removeToken");

      // Clear all user state properties.
      this.refresh = null;
      this.access = null;
      this.isAuthenticated = false;
      this.id = null;
      this.name = null;
      this.email = null;

      // Remove the Authorization header from Axios.
      delete axios.defaults.headers.common["Authorization"];

      // Remove user data from local storage.
      localStorage.removeItem("user.access");
      localStorage.removeItem("user.refresh");
      localStorage.removeItem("user.id");
      localStorage.removeItem("user.name");
      localStorage.removeItem("user.email");
    },

    /**
     * Sets the user's information in the store and saves it to local storage.
     * @param {object} user - An object containing the user's ID, name, and email.
     */
    setUserInfo(user) {
      console.log("setUserInfo", user);

      this.id = user.id;
      this.name = user.name;
      this.email = user.email;

      // Store user information in local storage.
      localStorage.setItem("user.id", this.id ?? "");
      localStorage.setItem("user.name", this.name ?? "");
      localStorage.setItem("user.email", this.email ?? "");

      console.log("User", {
        id: this.id,
        name: this.name,
        email: this.email,
      });
    },

    /**
     * Refreshes the JWT access token using the refresh token.
     * If the refresh fails, the user is logged out.
     */
    refreshToken() {
      if (!this.refresh) {
        return; // Do nothing if there is no refresh token.
      }

      axios
        .post("/api/refresh/", {
          refresh: this.refresh,
        })
        .then((response) => {
          // Update the access token with the new one.
          this.access = response.data.access;

          // Save the new access token to local storage.
          localStorage.setItem("user.access", response.data.access);

          // Update the Authorization header for Axios.
          axios.defaults.headers.common["Authorization"] =
            "Bearer " + response.data.access;
        })
        .catch((error) => {
          console.log(error);
          // If refreshing the token fails, remove all tokens and log the user out.
          this.removeToken();
        });
    },
  },
});
