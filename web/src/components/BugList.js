import React, { useEffect, useState } from "react";
import { fetchBugs } from "../api/bugApi";
import { useNavigate } from "react-router-dom";
import { Table, Tag, Button, Typography, Spin } from "antd";
import { EyeOutlined, ReloadOutlined } from "@ant-design/icons";

const { Title } = Typography;

/**
 * Component for displaying a paginated, sortable, and filterable list of bugs.
 * 
 * Features:
 * - Shows bugs in a table with ID, subject, status, and priority
 * - Color-coded status and priority tags
 * - Pagination with configurable page size
 * - Filtering by status and priority
 * - Sorting by bug ID
 * - Navigation to bug details
 * 
 * @returns {JSX.Element} Rendered bug list component
 */
const BugList = () => {
  // State for storing list of bugs from API
  const [bugs, setBugs] = useState([]);
  // State for tracking loading status during API calls
  const [loading, setLoading] = useState(true);
  // State for pagination configuration and metadata
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0,
  });
  // Hook for programmatic navigation to detail view
  const navigate = useNavigate();

  /**
   * Fetches bugs from the API based on pagination parameters
   * 
   * @param {number} page - The page number to fetch
   * @param {number} pageSize - Number of bugs per page
   */
  const loadBugs = async (page = 1, pageSize = 10) => {
    setLoading(true);
    try {
      const response = await fetchBugs(page, pageSize);
      setBugs(response.results);
      setPagination({
        current: page,
        pageSize: pageSize,
        total: response.count,
      });
    } catch (error) {
      console.error("Failed to load bugs:", error);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Effect hook to load bugs when component mounts
   */
  useEffect(() => {
    loadBugs();
  }, []);

  /**
   * Maps priority level to appropriate color for visual indication
   * 
   * @param {string} priority - The priority level of the bug
   * @returns {string} Color code for the priority tag
   */
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

  /**
   * Maps status to appropriate color for visual indication
   * 
   * @param {string} status - The current status of the bug
   * @returns {string} Color code for the status tag
   */
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

  /**
   * Column configuration for the Ant Design Table component
   * Defines rendering, sorting, and filtering for each column
   */
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
      ellipsis: true, // Truncate long subjects with ellipsis
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

  /**
   * Handler for table pagination, sorting, and filtering changes
   * 
   * @param {Object} pagination - The new pagination state
   */
  const handleTableChange = (pagination) => {
    loadBugs(pagination.current, pagination.pageSize);
  };

  return (
    <div>
      {/* Header with title and refresh button */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Title level={2}>Bug List</Title>
        <Button 
          type="primary" 
          icon={<ReloadOutlined />} 
          onClick={() => loadBugs(pagination.current, pagination.pageSize)}
          loading={loading}
        >
          Refresh
        </Button>
      </div>
      
      {/* Show spinner during loading or the table when data is available */}
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
            current: pagination.current,
            pageSize: pagination.pageSize,
            total: pagination.total,
            showSizeChanger: true,
            pageSizeOptions: ['10', '20', '50'],
          }}
          onChange={handleTableChange}
        />
      )}
    </div>
  );
};

export default BugList;