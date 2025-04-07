/**
 * API Interceptor utility to automatically add authentication tokens to API requests
 * 
 * This module monkey-patches the global fetch function to intercept all outgoing
 * API requests and augment them with authorization headers when needed.
 */

/**
 * Sets up a global fetch interceptor for API authentication
 * 
 * When called, this function:
 * 1. Stores a reference to the original fetch implementation
 * 2. Replaces the global fetch with a wrapped version that:
 *    - Automatically adds auth token to API requests
 *    - Logs request details for debugging
 *    - Provides centralized error handling
 * 
 * The interceptor only adds auth headers to URLs containing '/api/'
 * to avoid affecting requests to third-party services.
 * 
 * @returns {void}
 */
const setupApiInterceptor = () => {
    // Store reference to original fetch implementation
    const originalFetch = window.fetch;
    
    // Replace global fetch with our interceptor
    window.fetch = function(url, options = {}) {
      // Get the current token from localStorage
      const token = localStorage.getItem('auth_token');
      
      // Only add auth header for our API requests
      if (url.includes('/api/') && token) {
        options = {
          ...options,
          headers: {
            ...options.headers,
            'Authorization': `Token ${token}`
          }
        };
      }
      
      // Log request details for debugging
      console.log(`Fetch request to ${url}`, { 
        headers: options.headers,
        method: options.method || 'GET'
      });
      
      // Call the original fetch with our modified options
      return originalFetch(url, options)
        .then(response => {
          // You can add global response handling here
          return response;
        })
        .catch(error => {
          // Centralized error logging for API requests
          console.error('API Request failed:', error);
          throw error; // Re-throw to allow component-level handling
        });
    };
  };
  
  export default setupApiInterceptor;