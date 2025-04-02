import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import BugList from "./components/BugList";
import BugDetail from "./components/BugDetail";
import Dashboard from "./components/Dashboard";

function App() {
    return (
        <Router>
            <div>
                <h1>Bug Tracker</h1>
                <Routes>
                    <Route path="/" element={
                        <div>
                            <BugList />
                            <Dashboard />
                        </div>
                    } />
                    <Route path="/bug/:bugId" element={<BugDetail />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;