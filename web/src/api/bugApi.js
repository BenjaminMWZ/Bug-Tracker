// import mockBugData from "./mock_data.json";
// import mockModifications from "./bug_modifications.json";

// // Simulate an API fetch with a delay
// const fakeFetch = (data, delay = 500) => 
//     new Promise(resolve => setTimeout(() => resolve(data), delay));

// export const fetchBugs = async () => {
//     return await fakeFetch(mockBugData);
// };

// export const fetchBugDetails = async (bugId) => {
//     const bug = mockBugData.find(b => b.bug_id === bugId.trim());
//     return await fakeFetch(bug);
// };

// export const fetchBugModifications = async () => {
//     return await fakeFetch(mockModifications);
// };

const API_BASE_URL = "http://127.0.0.1:8000"; // Adjust if backend is hosted elsewhere

export const fetchBugs = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/bugs/`);
        if (!response.ok) {
            throw new Error("Failed to fetch bugs");
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