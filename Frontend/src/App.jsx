import React from "react";
import Dashboard from "./pages/Dashboard";
import "./index.css";

const App = () => {
  return (
    <div className="app-container">
      {/* Navbar */}
      <div className="navbar">
        <h1>AI Answer Evaluation System</h1>
      </div>

      {/* Main Content */}
      <Dashboard />
    </div>
  );
};

export default App;