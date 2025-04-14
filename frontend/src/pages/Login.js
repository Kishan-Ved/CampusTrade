import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://127.0.0.1:5001/login', { username, password });
      if (res.data.token) {
        // Store token in localStorage or state
        localStorage.setItem('token', res.data.token);
        // Optionally, store user info
        localStorage.setItem('user', JSON.stringify(res.data.user));
        navigate('/');  // Redirect to home after successful login
      } else {
        alert('Invalid login credentials');
      }
    } catch (err) {
      console.error("Login error", err);
      alert('An error occurred. Please try again.');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input 
          type="text" 
          placeholder="Username" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
