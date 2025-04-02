import React, { useEffect, useState } from "react";
import { fetchBugModifications } from "../api/bugApi";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

const Dashboard = () => {
    const [modifications, setModifications] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            const data = await fetchBugModifications();
            setModifications(data);
            setLoading(false);
        };
        loadData();
    }, []);

    if (loading) return <div>Loading chart...</div>;

    return (
        <div>
            <h2>Bug Modifications Over Time</h2>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={modifications}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="count" stroke="#8884d8" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default Dashboard;