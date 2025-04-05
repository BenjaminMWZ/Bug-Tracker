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

// Format the date to be more compact (MM/DD format)
const formatXAxis = (dateStr) => {
  const date = new Date(dateStr);
  return `${date.getMonth() + 1}/${date.getDate()}`;
};

const Dashboard = () => {
  const [modifications, setModifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [chartType, setChartType] = useState('line');

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
      case 'bar':
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
      case 'area':
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
            <Option value="bar"><AreaChartOutlined /> Area Chart</Option>
            <Option value="area"><BarChartOutlined /> Bar Chart</Option>
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