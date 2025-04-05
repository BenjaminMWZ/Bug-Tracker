import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchBugDetails } from "../api/bugApi";
import { Card, Descriptions, Tag, Typography, Button, Spin, Divider } from "antd";
import { ArrowLeftOutlined, ClockCircleOutlined } from "@ant-design/icons";

const { Title } = Typography;

const BugDetail = () => {
  const { bugId } = useParams();
  const [bug, setBug] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

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

  // Priority colors for tags
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

  // Status colors for tags
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

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
      </div>
    );
  }

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

  return (
    <div>
      <Button 
        icon={<ArrowLeftOutlined />} 
        onClick={() => navigate('/')}
        style={{ marginBottom: 16 }}
      >
        Back to Bug List
      </Button>
      
      <Card title={<Title level={2}>Bug Details: {bug.bug_id}</Title>}>
        <Descriptions bordered column={1} size="large">
          <Descriptions.Item label="Subject">
            {bug.subject}
          </Descriptions.Item>
          
          <Descriptions.Item label="Status">
            <Tag color={getStatusColor(bug.status)} style={{ fontSize: '14px', padding: '2px 8px' }}>
              {bug.status?.toUpperCase()}
            </Tag>
          </Descriptions.Item>
          
          <Descriptions.Item label="Priority">
            <Tag color={getPriorityColor(bug.priority)} style={{ fontSize: '14px', padding: '2px 8px' }}>
              {bug.priority?.toUpperCase()}
            </Tag>
          </Descriptions.Item>
          
          <Descriptions.Item label="Description">
            <div style={{ whiteSpace: 'pre-wrap' }}>{bug.description}</div>
          </Descriptions.Item>
          
          <Descriptions.Item label="Modification Count">
            {bug.modified_count}
          </Descriptions.Item>
        </Descriptions>
        
        <Divider />
        
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