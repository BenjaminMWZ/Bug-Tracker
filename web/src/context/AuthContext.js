import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('auth_token') || null);
  const [loading, setLoading] = useState(true);

 // Check if token exists on app load
 useEffect(() => {
  if (token) {
    fetchUserProfile();
  } else {
    setLoading(false);
  }
}, [token]);

const fetchUserProfile = async () => {
  setLoading(true);
  try {
    // Log the token to check what's being sent
    console.log('Using token for profile fetch:', token);
    
    const response = await fetch('http://127.0.0.1:8000/api/auth/profile/', {
      headers: {
        'Authorization': `Token ${token}`
      }
    });

    console.log('Profile response status:', response.status);
    
    if (response.ok) {
      const userData = await response.json();
      console.log('User data:', userData);
      setUser(userData);
    } else {
      // Log the error response
      const errorText = await response.text();
      console.error('Profile fetch failed:', response.status, errorText);
      logout();
    }
  } catch (error) {
    console.error('Error fetching user profile:', error);
    logout();
  } finally {
    setLoading(false);
  }
};

const login = async (username, password) => {
  setLoading(true);
  try {
    const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Login successful, received token:', data.token);
      
      // Set token first, as the useEffect will trigger profile fetch
      localStorage.setItem('auth_token', data.token);
      setToken(data.token);
      setUser(data.user);
      
      return { success: true };
    } else {
      const errorData = await response.json();
      return { 
        success: false, 
        error: errorData.error || 'Login failed. Please check your credentials.' 
      };
    }
  } catch (error) {
    console.error('Login error:', error);
    return { 
      success: false, 
      error: 'Network error. Please try again later.' 
    };
  } finally {
    setLoading(false);
  }
};


  const register = async (userData) => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();
      
      if (response.ok) {
        setUser(data.user);
        setToken(data.token);
        
        localStorage.setItem('auth_token', data.token);
        
        return { success: true };
      } else {
        return { 
          success: false, 
          error: data.error || data.username || data.email || 'Registration failed.'
        };
      }
    } catch (error) {
      console.error('Registration error:', error);
      return { 
        success: false, 
        error: 'Network error. Please try again later.' 
      };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('auth_token');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login,
        register,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};