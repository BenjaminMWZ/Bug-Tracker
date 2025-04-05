import React, { useEffect, useState } from "react";
import { fetchBugs } from "../api/bugApi";
import { useNavigate } from "react-router-dom";
import { Table, Tag, Button, Typography, Spin } from "antd";
import { EyeOutlined, ReloadOutlined } from "@ant-design/icons";

const { Title } = Typography;

const BugList = () => {
  const [bugs, setBugs] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const loadBugs = async () => {
    setLoading(true);
    try {
      const data = await fetchBugs();
      setBugs(data);
    } catch (error) {
      console.error("Failed to load bugs:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBugs();
  }, []);

  // Priority colors for tags
  const getPriorityColor = (priority) => {
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

  const columns = [
    {
      title: 'Bug ID',
      dataIndex: 'bug_id',
      key: 'bug_id',
      sorter: (a, b) => a.bug_id.localeCompare(b.bug_id),
    },
    {
      title: 'Subject',
      dataIndex: 'subject',
      key: 'subject',
      ellipsis: true,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={getStatusColor(status)}>
          {status.toUpperCase()}
        </Tag>
      ),
      filters: [
        { text: 'Open', value: 'open' },
        { text: 'In Progress', value: 'in_progress' },
        { text: 'Resolved', value: 'resolved' },
        { text: 'Closed', value: 'closed' },
      ],
      onFilter: (value, record) => record.status.toLowerCase() === value,
    },
    {
      title: 'Priority',
      dataIndex: 'priority',
      key: 'priority',
      render: (priority) => (
        <Tag color={getPriorityColor(priority)}>
          {priority.toUpperCase()}
        </Tag>
      ),
      filters: [
        { text: 'High', value: 'high' },
        { text: 'Medium', value: 'medium' },
        { text: 'Low', value: 'low' },
      ],
      onFilter: (value, record) => record.priority.toLowerCase() === value,
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Button 
          type="primary" 
          icon={<EyeOutlined />} 
          size="small"
          onClick={() => navigate(`/bug/${record.bug_id}`)}
        >
          Details
        </Button>
      ),
    },
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Title level={2}>Bug List</Title>
        <Button 
          type="primary" 
          icon={<ReloadOutlined />} 
          onClick={loadBugs}
          loading={loading}
        >
          Refresh
        </Button>
      </div>
      
      {loading ? (
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <Spin size="large" />
        </div>
      ) : (
        <Table 
          columns={columns} 
          dataSource={bugs} 
          rowKey="bug_id"
          pagination={{ 
            pageSize: 10,
            showSizeChanger: true, 
            pageSizeOptions: ['10', '20', '50'],
          }}
        />
      )}
    </div>
  );
};

export default BugList;