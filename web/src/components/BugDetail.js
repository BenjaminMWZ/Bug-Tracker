import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchBugDetails } from "../api/bugApi";

const BugDetail = () => {
    const { bugId } = useParams(); // Get bug ID from URL
    const [bug, setBug] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadBug = async () => {
            setLoading(true);
            const data = await fetchBugDetails(bugId);
            setBug(data);
            setLoading(false);
        };
        loadBug();
    }, [bugId]);

    if (loading) return <div>Loading bug details...</div>;
    if (!bug) return <div>Bug not found.</div>;

    return (
        <div>
            <h2>Bug Details</h2>
            <p><strong>Bug ID:</strong> {bug.bug_id}</p>
            <p><strong>Subject:</strong> {bug.subject}</p>
            <p><strong>Description:</strong> {bug.description}</p>
            <p><strong>Status:</strong> {bug.status}</p>
            <p><strong>Priority:</strong> {bug.priority}</p>
            <p><strong>Created At:</strong> {new Date(bug.created_at).toLocaleString()}</p>
            <p><strong>Updated At:</strong> {new Date(bug.updated_at).toLocaleString()}</p>
            <p><strong>Modified Count:</strong> {bug.modified_count}</p>
        </div>
    );
};

export default BugDetail;