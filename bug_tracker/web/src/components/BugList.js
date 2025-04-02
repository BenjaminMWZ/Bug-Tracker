import React, { useEffect, useState } from "react";
import { fetchBugs } from "../api/bugApi";
import { Link } from "react-router-dom";

const BugList = () => {
    const [bugs, setBugs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadBugs = async () => {
            setLoading(true);
            const data = await fetchBugs();
            setBugs(data);
            setLoading(false);
        };
        loadBugs();
    }, []);

    if (loading) return <div>Loading bugs lists...</div>;

    return (
        <div>
            <h2>Bug List</h2>
            <table border="1">
                <thead>
                    <tr>
                        <th>Bug ID</th>
                        <th>Subject</th>
                        <th>Status</th>
                        <th>Priority</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {bugs.map(bug => (
                        <tr key={bug.bug_id}>
                            <td>{bug.bug_id}</td>
                            <td>{bug.subject}</td>
                            <td>{bug.status}</td>
                            <td>{bug.priority}</td>
                            <td>
                                <Link to={`/bug/${bug.bug_id}`}>View Details</Link>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default BugList;