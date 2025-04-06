const API_BASE_URL = "/api";

export const fetchBugs = async (page = 1, pageSize = 10) => {
  try {
    const response = await fetch(`${API_BASE_URL}/bugs/?page=${page}&page_size=${pageSize}`);
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
        const response = await fetch(`${API_BASE_URL}/bugs/${bugId}/`);
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
        const response = await fetch(`${API_BASE_URL}/bug_modifications/`);
        if (!response.ok) {
            throw new Error("Failed to fetch bug modifications");
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching bug modifications:", error);
        throw error;
    }
};