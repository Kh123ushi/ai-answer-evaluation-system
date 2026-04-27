import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
} from "recharts";

const Charts = ({ data }) => {
  // 🔹 Handle empty data
  if (!data || data.length === 0) {
    return (
      <div style={styles.container}>
        <h2 style={styles.title}> Performance Chart</h2>
        <p style={styles.noData}>No data available</p>
      </div>
    );
  }

  // 🔹 Format data for chart
  const chartData = data.map((item) => ({
    name:
      item.file.length > 12
        ? item.file.substring(0, 12) + "..."
        : item.file,
    marks: item.marks,
    similarity: item.similarity,
  }));

  return (
    <div style={styles.container}>
      <h2 style={styles.title}> Chart</h2>

      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={chartData}>
          {/* Grid */}
          <CartesianGrid strokeDasharray="3 3" />

          {/* Axes */}
          <XAxis dataKey="name" />
          <YAxis />

          {/* Tooltip + Legend */}
          <Tooltip />
          <Legend />

          {/* Bars */}
          <Bar dataKey="marks" name="Marks" />
          <Bar dataKey="similarity" name="Similarity" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

const styles = {
  container: {
    width: "80%",
    margin: "20px auto",
    backgroundColor: "#ffffff",
    padding: "20px",
    borderRadius: "10px",
    boxShadow: "0px 4px 10px rgba(0,0,0,0.1)",
  },
  title: {
    textAlign: "center",
    marginBottom: "15px",
    fontSize: "20px",
  },
  noData: {
    textAlign: "center",
    color: "#888",
  },
};

export default Charts;