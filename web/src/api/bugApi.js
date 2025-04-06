const API_BASE_URL = "http://127.0.0.1:8000/api";

// Helper function to get auth headers
const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Token ${token}` : '',
  };
};

export const fetchBugs = async (page = 1, pageSize = 10) => {
  try {
    const response = await fetch(`${API_BASE_URL}/bugs/?page=${page}&page_size=${pageSize}`, {
      headers: getAuthHeaders()
    });
    
    if (response.status === 401) {
      // Handle unauthorized (could trigger token refresh or logout)
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

export const fetchBugDetails = async (bugId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/bugs/${bugId}/`, {
      headers: getAuthHeaders()
    });
    
    if (response.status === 401) {
      throw new Error('Unauthorized - Please log in again');
    }
    
    if (!response.ok) {
      throw new Error("Failed to fetch bug details");
    }
    
    return await response.json();
  } catch (error) {
    console.error(`Error fetching bug details for ${bugId}:`, error);
    throw error;
  }
};

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