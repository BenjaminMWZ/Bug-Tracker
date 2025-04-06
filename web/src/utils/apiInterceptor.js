// API Interceptor to automatically add auth token to all requests
const setupApiInterceptor = () => {
    const originalFetch = window.fetch;
    
    window.fetch = function(url, options = {}) {
      // Get the current token
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
      
      console.log(`Fetch request to ${url}`, { 
        headers: options.headers,
        method: options.method || 'GET'
      });
      
      return originalFetch(url, options)
        .then(response => {
          // You can add global response handling here
          return response;
        })
        .catch(error => {
          console.error('API Request failed:', error);
          throw error;
        });
    };
  };
  
  export default setupApiInterceptor;