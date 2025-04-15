// src/pages/Home.js
import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  const isLoggedIn = !!localStorage.getItem('token');

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1>Welcome to CampusTrade 🛍️</h1>
          <p className="hero-subtitle">The secure platform for buying and selling within your campus community</p>

          {!isLoggedIn && (
            <div className="hero-buttons">
              <Link to="/register" className="btn btn-primary">Register</Link>
              <Link to="/login" className="btn btn-secondary">Login</Link>
              {/* <Link to="/products" className="btn">View Products</Link> */}
            </div>
          )}

          {isLoggedIn && (
            <div className="hero-buttons">
              <Link to="/products" className="btn btn-primary">View Products</Link>
              <Link to="/add-product" className="btn btn-secondary">Add Product</Link>
              <Link to="/wishlist" className="btn">Wishlist</Link>
              <Link to="/getMyTransactions" className="btn">Transactions</Link>
            </div>
          )}

          {isLoggedIn && (
            <div className="hero-links">
              <Link to="/reviews">Reviews</Link> |
              <Link to="/complaints">Complaints</Link> |
              <Link to="/reports">Reports</Link> |
              <Link to="/profile">Profile</Link> |
              <Link to="/my-listings">My Listings</Link>
            </div>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <h2>Why Choose CampusTrade?</h2>

        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <h3>Secure Transactions</h3>
            <p>All transactions are secure and tracked within our platform.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">👥</div>
            <h3>Campus Community</h3>
            <p>Trade exclusively with verified members of your campus.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">💰</div>
            <h3>Save Money</h3>
            <p>Find great deals on textbooks, electronics, and more.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">♻️</div>
            <h3>Sustainability</h3>
            <p>Reduce waste by giving items a second life on campus.</p>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works-section">
        <h2>How It Works</h2>

        <div className="steps-container">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Create an Account</h3>
            <p>Sign up with your campus email to join the community.</p>
          </div>

          <div className="step">
            <div className="step-number">2</div>
            <h3>Browse or List Items</h3>
            <p>Find what you need or list items you want to sell.</p>
          </div>

          <div className="step">
            <div className="step-number">3</div>
            <h3>Connect & Trade</h3>
            <p>Arrange meetups on campus to complete transactions.</p>
          </div>

          <div className="step">
            <div className="step-number">4</div>
            <h3>Rate & Review</h3>
            <p>Build trust in the community by rating your experience.</p>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="cta-section">
        <h2>Ready to Start Trading?</h2>
        <p>Join hundreds of students already using CampusTrade</p>

        {!isLoggedIn ? (
          <Link to="/register" className="btn btn-accent">Create an Account</Link>
        ) : (
          <Link to="/products" className="btn btn-accent">Browse Products</Link>
        )}
      </section>
    </div>
  );
};

export default Home;