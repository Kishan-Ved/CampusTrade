// src/pages/Home.js
import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div style={{ padding: '2rem' }}>
      <h1>Welcome to CampusTrade 🛍️</h1>
      <p>
        <Link to="/register">Register</Link> |{" "}
        <Link to="/login">Login</Link> |{" "}
        <Link to="/products">View Products</Link> |{" "}
        <Link to="/add-product">Add Product</Link> |{" "}
        <Link to="/wishlist">Wishlist</Link> |{" "}
        <Link to="/transactions">Transactions</Link> |{" "}
        <Link to="/reviews">Reviews</Link> |{" "}
        <Link to="/complaints">Complaints</Link> |{" "}
        <Link to="/report">Reports</Link> |{" "}
        <Link to="/profile">Profile</Link>
      </p>
    </div>
  );
};

export default Home;

