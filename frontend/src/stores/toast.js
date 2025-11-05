// Import Dependencies
import { defineStore } from "pinia";

// Import Components

export const useToastStore = defineStore("toast", {
  // Define what should be stored in useToastStore
  state: () => ({
    ms: 0,
    message: "",
    classes: "",
    isVisible: false,
  }),
  // Manipulate the state values
  actions: {
    showToast(ms, message, classes) {
      this.ms = parseInt(ms);
      this.message = message;
      this.classes = classes;
      this.isVisible = true;

      // After 10 ms this function is added and shown on the Screen
      setTimeout(() => {
        this.classes += " -translate-y-28";
      }, 10);

      // Of the available 3000ms - 500ms we remove the "-translate-y-28" and set it to be empty
      // so it will NOT be shown on the Screen
      setTimeout(() => {
        this.classes = this.classes.replace("-translate-y-28", "");
      }, this.ms - 500);

      // After e. g. 300ms it is no longer rendered in the dom element
      setTimeout(() => {
        this.isVisible = false;
      }, this.ms);
    },
  },
});
