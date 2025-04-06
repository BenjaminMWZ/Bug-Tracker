import React, { useContext, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from "react-router-dom";
import { Layout, Menu, Typography, theme, Button, Dropdown } from "antd";
import { 
  BugOutlined, DashboardOutlined, HomeOutlined, 
  UserOutlined, LogoutOutlined 
} from "@ant-design/icons";
import BugList from "./components/BugList";
import BugDetail from "./components/BugDetail";
import Dashboard from "./components/Dashboard";
import Login from "./components/Login";
import Register from "./components/Register";
import PrivateRoute from "./components/PrivateRoute";
import { AuthProvider, AuthContext } from "./context/AuthContext"; // Import from the proper file
import "./App.css";
import setupApiInterceptor from "./utils/apiInterceptor";

const { Header, Content, Footer } = Layout;
const { Title } = Typography;

// User dropdown menu
const UserMenu = () => {
  const { user, logout } = useContext(AuthContext);
  
  const items = [
    {
      key: '1',
      label: <span><UserOutlined /> Profile</span>,
    },
    {
      key: '2',
      label: <span onClick={logout}><LogoutOutlined /> Logout</span>,
    },
  ];

  return (
    <Dropdown menu={{ items }} placement="bottomRight">
      <Button type="text" style={{ color: 'white' }}>
        <UserOutlined /> {user?.username}
      </Button>
    </Dropdown>
  );
};

// Component for authorized API calls 
const AuthorizedComponent = ({ children }) => {
  const { token } = useContext(AuthContext);
  
  useEffect(() => {
    setupApiInterceptor();
    // Add auth token to all API calls
    const originalFetch = window.fetch;
    window.fetch = function(url, options = {}) {
      // Only add auth header for our API requests
      if (url.includes('/api/') && token) {
        options.headers = {
          ...options.headers,
          'Authorization': `Token ${token}` // Use Token format
        };
      }
      return originalFetch(url, options);
    };
    
    return () => {
      // Restore original fetch when component unmounts
      window.fetch = originalFetch;
    };
  }, [token]);
  
  return children;
};

// Main app content
const AppContent = () => {
  const { token } = theme.useToken();
  const { user } = useContext(AuthContext);

  return (
    <Router>
      <Layout className="layout" style={{ minHeight: '100vh' }}>
        <Header style={{ 
          position: 'sticky', 
          top: 0, 
          zIndex: 1, 
          width: '100%', 
          display: 'flex', 
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div className="logo" style={{ marginRight: '24px' }}>
              <BugOutlined style={{ fontSize: '24px', color: 'white' }} />
            </div>
            <Title level={4} style={{ color: 'white', margin: 0, marginRight: '24px' }}>Bug Tracker</Title>
            {user && (
              <Menu
                theme="dark"
                mode="horizontal"
                defaultSelectedKeys={['1']}
                items={[
                  { key: '1', icon: <HomeOutlined />, label: <Link to="/">Home</Link> },
                  { key: '2', icon: <DashboardOutlined />, label: <Link to="/dashboard">Dashboard</Link> }
                ]}
              />
            )}
          </div>
          
          {user && <UserMenu />}
        </Header>
        
        <Content style={{ padding: '0 50px', marginTop: 24 }}>
          <div className="site-layout-content" style={{ 
            background: token.colorBgContainer, 
            padding: 24, 
            borderRadius: 8,
            minHeight: 'calc(100vh - 200px)'
          }}>
            <Routes>
              <Route path="/login" element={
                user ? <Navigate to="/" /> : <Login />
              } />
              <Route path="/register" element={
                user ? <Navigate to="/" /> : <Register />
              } />
              
              <Route path="/" element={
                <PrivateRoute>
                  <BugList />
                </PrivateRoute>
              } />
              
              <Route path="/dashboard" element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              } />
              
              <Route path="/bug/:bugId" element={
                <PrivateRoute>
                  <BugDetail />
                </PrivateRoute>
              } />
              
              <Route path="*" element={<Navigate to={user ? "/" : "/login"} />} />
            </Routes>
          </div>
        </Content>
        
        <Footer style={{ textAlign: 'center' }}>
          Bug Tracker ©{new Date().getFullYear()} Created with Weizhe Mao
        </Footer>
      </Layout>
    </Router>
  );
};

// Main App component
function App() {
  return (
    <AuthProvider>
      <AuthorizedComponent>
        <AppContent />
      </AuthorizedComponent>
    </AuthProvider>
  );
}

export default App; // Add proper default export