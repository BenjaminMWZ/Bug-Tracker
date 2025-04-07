import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchBugDetails } from "../api/bugApi";
import { Card, Descriptions, Tag, Typography, Button, Spin, Divider } from "antd";
import { ArrowLeftOutlined, ClockCircleOutlined } from "@ant-design/icons";

const { Title } = Typography;

/**
 * Component for displaying detailed information about a single bug.
 * 
 * Retrieves bug details using the bugId from URL parameters and displays
 * them in a formatted card with priority color-coding, timestamps, and navigation.
 * 
 * @returns {JSX.Element} Rendered bug detail view
 */
const BugDetail = () => {
  // Extract bugId from URL parameters
  const { bugId } = useParams();
  // State for storing the fetched bug data
  const [bug, setBug] = useState(null);
  // State for tracking loading status
  const [loading, setLoading] = useState(true);
  // Navigation hook for programmatic routing
  const navigate = useNavigate();

  /**
   * Effect hook to fetch bug details when component mounts or bugId changes
   */
  useEffect(() => {
    const loadBug = async () => {
      setLoading(true);
      try {
        const data = await fetchBugDetails(bugId);
        setBug(data);
      } catch (error) {
        console.error(`Failed to fetch bug details for ${bugId}:`, error);
      } finally {
        setLoading(false);
      }
    };
    loadBug();
  }, [bugId]);

  /**
   * Maps priority level to appropriate color for visual indication
   * 
   * @param {string} priority - The priority level of the bug
   * @returns {string} Color code for the priority tag
   */
  const getPriorityColor = (priority) => {
    if (!priority) return "default";
    
    switch (priority.toLowerCase()) {
      case 'high':
        return 'red';
      case 'medium':
        return 'orange';
      case 'low':
        return 'green';
      default:
        return 'blue';
    }
  };

  /**
   * Maps status to appropriate color for visual indication
   * 
   * @param {string} status - The current status of the bug
   * @returns {string} Color code for the status tag
   */
  const getStatusColor = (status) => {
    if (!status) return "default";
    
    switch (status.toLowerCase()) {
      case 'open':
        return 'blue';
      case 'in_progress':
        return 'orange';
      case 'resolved':
        return 'green';
      case 'closed':
        return 'gray';
      default:
        return 'default';
    }
  };

  // Show loading spinner while fetching data
  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
      </div>
    );
  }

  // Show error state if bug data couldn't be retrieved
  if (!bug) {
    return (
      <Card>
        <Title level={4}>Bug not found</Title>
        <Button type="primary" onClick={() => navigate('/')}>
          Back to Bug List
        </Button>
      </Card>
    );
  }

  // Main render with complete bug details
  return (
    <div>
      {/* Navigation button to return to bug list */}
      <Button 
        icon={<ArrowLeftOutlined />} 
        onClick={() => navigate('/')}
        style={{ marginBottom: 16 }}
      >
        Back to Bug List
      </Button>
      
      {/* Main card containing bug details */}
      <Card title={<Title level={2}>Bug Details: {bug.bug_id}</Title>}>
        <Descriptions bordered column={1} size="large">
          {/* Subject line of the bug */}
          <Descriptions.Item label="Subject">
            {bug.subject}
          </Descriptions.Item>
          
          {/* Current status with color-coded tag */}
          <Descriptions.Item label="Status">
            <Tag color={getStatusColor(bug.status)} style={{ fontSize: '14px', padding: '2px 8px' }}>
              {bug.status?.toUpperCase()}
            </Tag>
          </Descriptions.Item>
          
          {/* Priority level with color-coded tag */}
          <Descriptions.Item label="Priority">
            <Tag color={getPriorityColor(bug.priority)} style={{ fontSize: '14px', padding: '2px 8px' }}>
              {bug.priority?.toUpperCase()}
            </Tag>
          </Descriptions.Item>
          
          {/* Full description with preserved whitespace */}
          <Descriptions.Item label="Description">
            <div style={{ whiteSpace: 'pre-wrap' }}>{bug.description}</div>
          </Descriptions.Item>
          
          {/* Counter showing how many times this bug has been modified */}
          <Descriptions.Item label="Modification Count">
            {bug.modified_count}
          </Descriptions.Item>
        </Descriptions>
        
        <Divider />
        
        {/* Timestamps showing creation and last update times */}
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <div>
            <ClockCircleOutlined /> Created: {new Date(bug.created_at).toLocaleString()}
          </div>
          <div>
            <ClockCircleOutlined /> Last Updated: {new Date(bug.updated_at).toLocaleString()}
          </div>
        </div>
      </Card>
    </div>
  );
};

export default BugDetail;