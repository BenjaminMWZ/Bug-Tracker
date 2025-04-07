import React, { useEffect, useState } from "react";
import { fetchBugModifications } from "../api/bugApi";
import { 
  Bar, BarChart, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, 
  ResponsiveContainer, Label, AreaChart, Area 
} from "recharts";
import { Card, Typography, Spin, Select, Empty } from "antd";
import { BarChartOutlined, LineChartOutlined, AreaChartOutlined } from "@ant-design/icons";

const { Title } = Typography;
const { Option } = Select;

/**
 * Formats dates on the X-axis to a more compact MM/DD format
 * 
 * @param {string} dateStr - ISO date string to format
 * @returns {string} Formatted date string in MM/DD format
 */
const formatXAxis = (dateStr) => {
  const date = new Date(dateStr);
  return `${date.getMonth() + 1}/${date.getDate()}`;
};

/**
 * Dashboard component that displays bug modification statistics over time
 * 
 * Features:
 * - Fetches bug modification data from the API
 * - Visualizes data with different chart types (line, area, bar)
 * - Allows switching between chart types
 * - Displays custom tooltips with detailed information
 * - Handles loading and empty states
 * 
 * @returns {JSX.Element} Rendered dashboard component
 */
const Dashboard = () => {
  // State for storing modification data from API
  const [modifications, setModifications] = useState([]);
  // State for tracking loading status
  const [loading, setLoading] = useState(true);
  // State for current selected chart type
  const [chartType, setChartType] = useState('line');

  /**
   * Effect hook to fetch bug modification data when component mounts
   */
  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const data = await fetchBugModifications();
        setModifications(data);
      } catch (error) {
        console.error("Failed to fetch bug modifications:", error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  /**
   * Renders the appropriate chart based on selected chart type
   * Handles loading and empty states
   * 
   * @returns {JSX.Element} The chart component or loading/empty state
   */
  const renderChart = () => {
    if (loading) {
      return (
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <Spin size="large" />
        </div>
      );
    }

    if (!modifications || modifications.length === 0) {
      return <Empty description="No modification data available" />;
    }

    /**
     * Custom tooltip component for the charts
     * Shows formatted date and modification count
     * 
     * @param {Object} props - Props passed from Recharts
     * @param {boolean} props.active - Whether tooltip is active
     * @param {Array} props.payload - Data payload for tooltip
     * @param {string} props.label - X-axis label (date)
     * @returns {JSX.Element|null} Tooltip component or null if inactive
     */
    const CustomTooltip = ({ active, payload, label }) => {
      if (active && payload && payload.length) {
        // Show full date in tooltip
        const fullDate = new Date(label).toLocaleDateString();
        return (
          <div style={{ 
            backgroundColor: '#fff', 
            border: '1px solid #ccc',
            padding: '10px',
            borderRadius: '5px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)'
          }}>
            <p style={{ margin: 0, fontWeight: 'bold' }}>{`Date: ${fullDate}`}</p>
            <p style={{ margin: 0 }}>{`Modifications: ${payload[0].value}`}</p>
          </div>
        );
      }
      return null;
    };

    // Common X and Y axis configurations to maintain consistency across chart types
    const xAxisConfig = {
      dataKey: "date",
      tickFormatter: formatXAxis,
      angle: -45,  // Rotate labels
      textAnchor: "end",  // Align rotated text
      height: 60,  // Allow more space for rotated labels
      interval: 0,  // Show all ticks
      tick: { fontSize: 12 },  // Smaller font size
      padding: { bottom: 5 }
    };

    const yAxisConfig = {
      allowDecimals: false,  // Only show integers for counts
      children: [
        <Label 
          value="Modifications Count" 
          angle={-90} 
          position="insideLeft" 
          style={{ textAnchor: 'middle' }}
          offset={-5}
          dy={50}
        />
      ]
    };

    switch (chartType) {
      case 'area':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <AreaChart
              data={modifications}
              margin={{ top: 20, right: 30, left: 50, bottom: 70 }} // Extra bottom margin for rotated labels
            >
              <defs>
                <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#8884d8" stopOpacity={0.1}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis {...xAxisConfig}>
                <Label value="Date" position="insideBottom" offset={-10} />
              </XAxis>
              <YAxis {...yAxisConfig} />
              <Tooltip content={<CustomTooltip />} />
              <Area 
                type="monotone" 
                dataKey="count" 
                stroke="#8884d8" 
                fillOpacity={1} 
                fill="url(#colorCount)" 
              />
            </AreaChart>
          </ResponsiveContainer>
        );
      case 'bar':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart
              data={modifications}
              margin={{ top: 20, right: 30, left: 50, bottom: 70 }} // Extra bottom margin for rotated labels
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis {...xAxisConfig}>
                <Label value="Date" position="insideBottom" offset={-10} />
              </XAxis>
              <YAxis {...yAxisConfig} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        );
      default:
        return (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart
              data={modifications}
              margin={{ top: 20, right: 30, left: 50, bottom: 70 }} // Extra bottom margin for rotated labels
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis {...xAxisConfig}>
                <Label value="Date" position="insideBottom" offset={-10} />
              </XAxis>
              <YAxis {...yAxisConfig} />
              <Tooltip content={<CustomTooltip />} />
              <Line 
                type="monotone" 
                dataKey="count" 
                stroke="#8884d8" 
                activeDot={{ r: 8 }} 
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        );
    }
  };

  return (
    <Card 
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Title level={2}>Bug Modifications Over Time</Title>
          <Select 
            defaultValue="line" 
            style={{ width: 150 }} 
            onChange={setChartType}
          >
            <Option value="line"><LineChartOutlined /> Line Chart</Option>
            <Option value="area"><AreaChartOutlined /> Area Chart</Option>
            <Option value="bar"><BarChartOutlined /> Bar Chart</Option>
          </Select>
        </div>
      }
    >
      {renderChart()}
      <div style={{ marginTop: 16, textAlign: 'center', color: '#888' }}>
        Shows bug modifications over the past week
      </div>
    </Card>
  );
};

export default Dashboard;