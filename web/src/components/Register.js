import React, { useState, useContext } from 'react';
import { Form, Input, Button, Card, Alert, Typography } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons';
import { AuthContext } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

const { Title } = Typography;

/**
 * Registration component for new user account creation
 * 
 * Provides a form for users to create a new account with username, email,
 * and password validation. Uses the AuthContext to handle the registration
 * process and automatically logs in the user upon successful registration.
 * 
 * Features:
 * - Form validation for all fields including email format
 * - Password confirmation matching
 * - Error handling and display
 * - Loading state during submission
 * - Automatic redirection after successful registration
 * 
 * @returns {JSX.Element} Rendered registration form
 */
const Register = () => {
  // State for tracking and displaying registration errors
  const [error, setError] = useState('');
  // State for tracking form submission loading state
  const [loading, setLoading] = useState(false);
  // Access registration function from authentication context
  const { register } = useContext(AuthContext);
  // Hook for programmatic navigation after successful registration
  const navigate = useNavigate();

  /**
   * Form submission handler for user registration
   * 
   * Processes the form data, calls the registration API,
   * and handles success/failure states
   * 
   * @param {Object} values - Form values containing username, email, password, etc.
   */
  const onFinish = async (values) => {
    setError('');
    setLoading(true);
    
    try {
      // Call the register method from AuthContext
      const result = await register({
        username: values.username,
        email: values.email,
        password: values.password,
        password2: values.confirmPassword
      });
      
      if (result.success) {
        navigate('/');
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', marginTop: '50px' }}>
      <Card>
        <Title level={2} style={{ textAlign: 'center', marginBottom: '30px' }}>
          Create an Account
        </Title>
        
        {/* Display error messages if registration fails */}
        {error && <Alert message={error} type="error" showIcon style={{ marginBottom: '20px' }} />}
        
        {/* Registration form with validation */}
        <Form
          name="register"
          onFinish={onFinish}
          layout="vertical"
        >
          {/* Username field with validation */}
          <Form.Item
            name="username"
            rules={[{ required: true, message: 'Please enter a username!' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="Username" size="large" />
          </Form.Item>
          
          {/* Email field with format validation */}
          <Form.Item
            name="email"
            rules={[
              { required: true, message: 'Please enter your email!' },
              { type: 'email', message: 'Please enter a valid email address!' }
            ]}
          >
            <Input prefix={<MailOutlined />} placeholder="Email" size="large" />
          </Form.Item>
          
          {/* Password field with minimum length validation */}
          <Form.Item
            name="password"
            rules={[
              { required: true, message: 'Please enter a password!' },
              { min: 6, message: 'Password must be at least 6 characters!' }
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Password"
              size="large"
            />
          </Form.Item>
          
          {/* Password confirmation field with matching validation */}
          <Form.Item
            name="confirmPassword"
            dependencies={['password']}
            rules={[
              { required: true, message: 'Please confirm your password!' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('The two passwords do not match!'));
                },
              }),
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Confirm Password"
              size="large"
            />
          </Form.Item>
          
          {/* Submit button with loading state */}
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              size="large"
              block
              loading={loading}
            >
              Register
            </Button>
          </Form.Item>
          
          {/* Link to login page for existing users */}
          <div style={{ textAlign: 'center' }}>
            Already have an account? <Link to="/login">Login</Link>
          </div>
        </Form>
      </Card>
    </div>
  );
};

export default Register;