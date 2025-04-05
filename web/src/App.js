import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import { Layout, Menu, Typography, theme } from "antd";
import { BugOutlined, DashboardOutlined, HomeOutlined } from "@ant-design/icons";
import BugList from "./components/BugList";
import BugDetail from "./components/BugDetail";
import Dashboard from "./components/Dashboard";
import "./App.css";

const { Header, Content, Footer } = Layout;
const { Title } = Typography;

function App() {
  const { token } = theme.useToken();

  return (
    <Router>
      <Layout className="layout" style={{ minHeight: '100vh' }}>
        <Header style={{ position: 'sticky', top: 0, zIndex: 1, width: '100%', display: 'flex', alignItems: 'center' }}>
          <div className="logo" style={{ marginRight: '24px' }}>
            <BugOutlined style={{ fontSize: '24px', color: 'white' }} />
          </div>
          <Title level={4} style={{ color: 'white', margin: 0, marginRight: '24px' }}>Bug Tracker</Title>
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['1']}
            items={[
              { key: '1', icon: <HomeOutlined />, label: <Link to="/">Home</Link> },
              { key: '2', icon: <DashboardOutlined />, label: <Link to="/dashboard">Dashboard</Link> }
            ]}
          />
        </Header>
        <Content style={{ padding: '0 50px', marginTop: 24 }}>
          <div className="site-layout-content" style={{ background: token.colorBgContainer, padding: 24, borderRadius: 8 }}>
            <Routes>
              <Route path="/" element={<BugList />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/bug/:bugId" element={<BugDetail />} />
            </Routes>
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          Bug Tracker ©{new Date().getFullYear()} Created with Weizhe Mao
        </Footer>
      </Layout>
    </Router>
  );
}

export default App;