// Import Dependencies
import { defineStore } from "pinia"; // Pinia's function to create a new store.

/**
 * `useToastStore` is a Pinia store for managing toast notifications.
 */
export const useToastStore = defineStore("toast", {
  // The state is a function that returns an object of reactive properties for the toast.
  state: () => ({
    ms: 0, // The duration of the toast in milliseconds.
    message: "", // The message to be displayed in the toast.
    classes: "", // CSS classes for styling the toast (e.g., background color).
    isVisible: false, // Controls the visibility of the toast.
  }),

  // Actions are methods that can be called to manipulate the state.
  actions: {
    /**
     * Displays a toast notification with a message and styles for a specific duration.
     * @param {number} ms - The duration in milliseconds for the toast to be visible.
     * @param {string} message - The message to display.
     * @param {string} classes - The CSS classes to apply for styling.
     */
    showToast(ms, message, classes) {
      this.ms = parseInt(ms);
      this.message = message;
      this.classes = classes;
      this.isVisible = true;

      // After a short delay, add a class to animate the toast into view.
      setTimeout(() => {
        this.classes += " -translate-y-28";
      }, 10);

      // Before the toast disappears, remove the animation class to slide it out.
      setTimeout(() => {
        this.classes = this.classes.replace("-translate-y-28", "");
      }, this.ms - 500);

      // After the full duration, hide the toast by setting isVisible to false.
      setTimeout(() => {
        this.isVisible = false;
      }, this.ms);
    },
  },
});
