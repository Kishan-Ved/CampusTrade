// src/components/Header.js
import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  const isLoggedIn = !!localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  return (
    <header style={{ padding: '1rem', backgroundColor: '#f0f0f0', display: 'flex', justifyContent: 'space-between' }}>
      <div>
        <Link to="/" style={{ marginRight: '1rem' }}>CampusTrade</Link>
        {isLoggedIn && (
          <>
            <Link to="/products" style={{ marginRight: '1rem' }}>Products</Link>
            <Link to="/wishlist" style={{ marginRight: '1rem' }}>Wishlist</Link>
            <Link to="/add-product" style={{ marginRight: '1rem' }}>Add Product</Link>
          </>
        )}
      </div>
      <div>
        {isLoggedIn ? (
          <button onClick={handleLogout}>Logout</button>
        ) : (
          <>
            <Link to="/login" style={{ marginRight: '1rem' }}>Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </header>
  );
};

export default Header;
