/**
 * Base URL for all API requests to the backend server
 * Points to the local development server running Django
 */
const API_BASE_URL = "http://127.0.0.1:8000/api";

/**
 * Helper function to get authentication headers for API requests
 * 
 * Retrieves the JWT token from local storage and formats it for the Authorization header.
 * Always includes the Content-Type header for JSON requests.
 * 
 * @returns {Object} Headers object with Content-Type and optional Authorization
 */
const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Token ${token}` : '',
  };
};

/**
 * Fetches a paginated list of bugs from the API
 * 
 * Makes an authenticated request to get bug data with pagination support.
 * Handles unauthorized responses by redirecting to login.
 * 
 * @param {number} page - The page number to fetch (default: 1)
 * @param {number} pageSize - Number of bugs per page (default: 10)
 * @returns {Promise<Object>} Promise resolving to JSON response with bugs data
 * @throws {Error} If the request fails or unauthorized
 */
export const fetchBugs = async (page = 1, pageSize = 10) => {
  try {
    const response = await fetch(`${API_BASE_URL}/bugs/?page=${page}&page_size=${pageSize}`, {
      headers: getAuthHeaders()
    });
    
    if (response.status === 401) {
      // Handle unauthorized
      alert('You need to log in again');
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
      throw new Error('Unauthorized - Please log in again');
    }
    
    if (!response.ok) {
      throw new Error(`Failed to fetch bugs: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error("Error fetching bugs:", error);
    throw error;
  }
};

/**
 * Fetches detailed information for a specific bug
 * 
 * Makes an authenticated request to get a single bug's complete data.
 * Handles unauthorized responses by redirecting to login.
 * 
 * @param {string} bugId - The unique identifier of the bug to fetch
 * @returns {Promise<Object>} Promise resolving to JSON response with bug details
 * @throws {Error} If the request fails or unauthorized
 */
export const fetchBugDetails = async (bugId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/bugs/${bugId}/`, {
      headers: getAuthHeaders()
    });
    
    if (response.status === 401) {
      // Handle unauthorized
      alert('You need to log in again');
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
      throw new Error('Unauthorized - Please log in again');
    }
    
    if (!response.ok) {
      throw new Error(`Failed to fetch bug details: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`Error fetching bug details for ${bugId}:`, error);
    throw error;
  }
};

/**
 * Fetches bug modification statistics data for the dashboard
 * 
 * Makes an authenticated request to get aggregated data about bug modifications
 * for charting purposes. This data powers the dashboard's visualization features.
 * 
 * @returns {Promise<Array>} Promise resolving to array of modification data points
 * @throws {Error} If the request fails or unauthorized
 */
export const fetchBugModifications = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/bug_modifications/`, {
      headers: getAuthHeaders()
    });
    
    if (response.status === 401) {
      throw new Error('Unauthorized - Please log in again');
    }
    
    if (!response.ok) {
      throw new Error("Failed to fetch bug modifications");
    }
    
    return await response.json();
  } catch (error) {
    console.error("Error fetching bug modifications:", error);
    throw error;
  }
};