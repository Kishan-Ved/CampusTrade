import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

// Create Context
const AuthContext = createContext();

// Provider component
export const AuthProvider = ({ children }) => {
  const [authState, setAuthState] = useState({
    isAuthenticated: false,
    token: null,
    user: null,
  });

  useEffect(() => {
    // Check if the token exists in local storage on app load
    const token = localStorage.getItem('token');
    if (token) {
      axios.get('http://127.0.0.1:5001/verifyToken', { headers: { Authorization: `Bearer ${token}` } })
        .then(res => {
          if (res.data.success) {
            setAuthState({
              isAuthenticated: true,
              token: token,
              user: res.data.user, // Assuming the API returns user info
            });
          } else {
            localStorage.removeItem('token');
          }
        })
        .catch(err => {
          console.error("Error verifying token", err);
          localStorage.removeItem('token');
        });
    }
  }, []);

  const login = (token, user) => {
    localStorage.setItem('token', token);
    setAuthState({
      isAuthenticated: true,
      token: token,
      user: user,
    });
  };

  const logout = () => {
    localStorage.removeItem('token');
    setAuthState({
      isAuthenticated: false,
      token: null,
      user: null,
    });
  };

  return (
    <AuthContext.Provider value={{ authState, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
