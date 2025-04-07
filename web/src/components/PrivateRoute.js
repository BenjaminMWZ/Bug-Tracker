import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { Spin } from 'antd';

/**
 * Component that protects routes requiring authentication
 * 
 * PrivateRoute acts as a wrapper around components that should only be
 * accessible to authenticated users. It:
 * 1. Checks if user authentication is being loaded
 * 2. Shows a loading spinner during authentication check
 * 3. Renders the protected route content if user is authenticated
 * 4. Redirects to login page if user is not authenticated
 * 
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child components to render if authenticated
 * @returns {JSX.Element} The protected component, loading spinner, or redirect
 */
const PrivateRoute = ({ children }) => {
  // Get authentication state from context
  const { user, loading } = useContext(AuthContext);

  // Show loading spinner while checking authentication
  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Spin size="large" tip="Loading..." />
      </div>
    );
  }

  // If user is authenticated, render children; otherwise redirect to login
  return user ? children : <Navigate to="/login" />;
};

export default PrivateRoute;