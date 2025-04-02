import mockBugData from "./mock_data.json";
import mockModifications from "./bug_modifications.json";

// Simulate an API fetch with a delay
const fakeFetch = (data, delay = 500) => 
    new Promise(resolve => setTimeout(() => resolve(data), delay));

export const fetchBugs = async () => {
    return await fakeFetch(mockBugData);
};

export const fetchBugDetails = async (bugId) => {
    const bug = mockBugData.find(b => b.bug_id === bugId.trim());
    return await fakeFetch(bug);
};

export const fetchBugModifications = async () => {
    return await fakeFetch(mockModifications);
};