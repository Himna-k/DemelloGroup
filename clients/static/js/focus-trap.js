/**
 * Focus Trap: Limit focus to focusable elements inside `element`
 * @param {HTMLElement} element - DOM element to focus trap inside
 * @return {Function} cleanup function
 */
function focusTrap(element) {
  const focusableElements = getFocusableElements(element);
  const firstFocusableEl = focusableElements[0];
  const lastFocusableEl = focusableElements[focusableElements.length - 1];

  // Check if focusable elements are detected properly
  console.log("Focusable Elements:", focusableElements);

  setTimeout(() => {
    console.log("First Focusable Element:", firstFocusableEl);
    firstFocusableEl.focus(); // Focus on the first focusable element
  }, 50);

  /**
   * Get all focusable elements inside `element`
   * @param {HTMLElement} element - DOM element to focus trap inside
   * @return {HTMLElement[]} List of focusable elements
   */
  function getFocusableElements(element = document) {
    return [
      ...element.querySelectorAll(
        'a, button, details, input, select, textarea, [tabindex]:not([tabindex="-1"])'
      ),
    ].filter((e) => !e.hasAttribute('disabled'));
  }

  function handleKeyDown(e) {
    const TAB = 9;
    const isTab = e.key.toLowerCase() === 'tab' || e.keyCode === TAB;

    if (!isTab) return;

    if (e.shiftKey) {
      if (document.activeElement === firstFocusableEl) {
        lastFocusableEl.focus(); // Loop focus back to the last element
        e.preventDefault(); // Prevent default tab action
      }
    } else {
      if (document.activeElement === lastFocusableEl) {
        firstFocusableEl.focus(); // Loop focus back to the first element
        e.preventDefault(); // Prevent default tab action
      }
    }
  }

  element.addEventListener('keydown', handleKeyDown);

  return function cleanup() {
    element.removeEventListener('keydown', handleKeyDown);
  }
}

/**
 * Toggle Theme - Save theme preference in localStorage
 */
function toggleTheme() {
  const dark = getThemeFromLocalStorage();
  setThemeToLocalStorage(!dark);
  console.log("Theme toggled");
}

function getThemeFromLocalStorage() {
  if (window.localStorage.getItem('dark')) {
    return JSON.parse(window.localStorage.getItem('dark'));
  }

  return !!window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
}

function setThemeToLocalStorage(value) {
  window.localStorage.setItem('dark', value);
}

/**
 * Modal Handling: Open and close modal while trapping focus inside
 */
let trapCleanup;

function openModal() {
  const modalElement = document.querySelector('#modal');
  this.isModalOpen = true;
  console.log('Modal opened');
  trapCleanup = focusTrap(modalElement); // Start focus trap on modal
}

function closeModal() {
  this.isModalOpen = false;
  trapCleanup(); // Clean up focus trap
  console.log('Modal closed');
}

/**
 * Prevent form reload behavior by preventing default form submission
 */
function preventFormReload() {
  const form = document.querySelector('form');
  form.addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the form from causing a page reload
    console.log("Form submission prevented");
    // Handle form logic here, like AJAX requests or validation
  });
}

/**
 * Example Button Event - Prevent page reload on click
 */
function preventButtonReload() {
  const button = document.querySelector('#myButton');
  button.addEventListener('click', function(e) {
    e.preventDefault(); // This prevents the default action that could cause a reload
    console.log("Button click prevented page reload");
    // Your custom logic goes here
  });
}

/**
 * Ensure no navigation occurs or unwanted page reloads
 * by overriding links or navigation actions
 */
function preventNavigation() {
  const links = document.querySelectorAll('a');
  links.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault(); // Prevent default link navigation
      console.log('Navigation prevented for:', link.href);
      // Custom navigation logic can go here (e.g., using client-side routing)
    });
  });
}

/**
 * Add all event listeners to prevent unwanted page reloads
 */
function setupEventListeners() {
  preventFormReload(); // Prevent form reloads
  preventButtonReload(); // Prevent button reloads
  preventNavigation(); // Prevent link navigation
  console.log("Event listeners set up to prevent page reloads");
}

// Initialize event listeners on page load
window.addEventListener('DOMContentLoaded', setupEventListeners);
// /**
//  * Limit focus to focusable elements inside `element`
//  * @param {HTMLElement} element - DOM element to focus trap inside
//  * @return {Function} cleanup function
//  */
// function focusTrap(element) {
//   const focusableElements = getFocusableElements(element)
//   const firstFocusableEl = focusableElements[0]
//   const lastFocusableEl = focusableElements[focusableElements.length - 1]

//   // Wait for the case the element was not yet rendered
//   setTimeout(() => {
//     console.log("First Focusable Element:", firstFocusableEl);
//     firstFocusableEl.focus();
//   }, 50);
//   /**
//    * Get all focusable elements inside `element`
//    * @param {HTMLElement} element - DOM element to focus trap inside
//    * @return {HTMLElement[]} List of focusable elements
//    */
//   function getFocusableElements(element = document) {
//     return [
//       ...element.querySelectorAll(
//         'a, button, details, input, select, textarea, [tabindex]:not([tabindex="-1"])'
//       ),
//     ].filter((e) => !e.hasAttribute('disabled'))
//   }

//   function handleKeyDown(e) {
//     const TAB = 9
//     const isTab = e.key.toLowerCase() === 'tab' || e.keyCode === TAB

//     if (!isTab) return

//     if (e.shiftKey) {
//       if (document.activeElement === firstFocusableEl) {
//         lastFocusableEl.focus()
//         e.preventDefault()
//       }
//     } else {
//       if (document.activeElement === lastFocusableEl) {
//         firstFocusableEl.focus()
//         e.preventDefault()
//       }
//     }
//   }

//   element.addEventListener('keydown', handleKeyDown)

//   return function cleanup() {
//     element.removeEventListener('keydown', handleKeyDown)
//   }
// }
