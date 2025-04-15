// src/components/Header.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  const isLoggedIn = !!localStorage.getItem('token');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="logo">
            <Link to="/">CampusTrade</Link>
          </div>

          <div className="mobile-menu-toggle" onClick={toggleMobileMenu}>
            <span></span>
            <span></span>
            <span></span>
          </div>

          <nav className={`main-nav ${mobileMenuOpen ? 'active' : ''}`}>
            <ul className="nav-links">
              <li><Link to="/" className="nav-link">Home</Link></li>
              <li><Link to="/products" className="nav-link">View Products</Link></li>

              {isLoggedIn ? (
                <>
                  <li><Link to="/add-product" className="nav-link">Add Product</Link></li>
                  <li><Link to="/wishlist" className="nav-link">Wishlist</Link></li>
                  <li><Link to="/my-listings" className="nav-link">My Listings</Link></li>
                  <li><Link to="/getMyTransactions" className="nav-link">Transactions</Link></li>
                  <li><Link to="/reviews" className="nav-link">Reviews</Link></li>
                  <li><Link to="/complaints" className="nav-link">Complaints</Link></li>
                  <li><Link to="/reports" className="nav-link">Reports</Link></li>
                  <li><Link to="/profile" className="nav-link">Profile</Link></li>
                </>
              ) : (
                <>
                  
                  {/* <li><Link to="/register" className="nav-link">Register</Link></li>
                  <li><Link to="/login" className="nav-link">Login</Link></li> */}
                </>
              )}
            </ul>

            <div className="auth-buttons">
              {isLoggedIn ? (
                <button onClick={handleLogout} className="btn btn-logout">Logout</button>
              ) : (
                <>
                  <Link to="/login" className="btn btn-login">Login</Link>
                  <Link to="/register" className="btn btn-register">Register</Link>
                </>
              )}
            </div>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
