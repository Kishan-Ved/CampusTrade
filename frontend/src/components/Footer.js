// src/components/Footer.js
import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>CampusTrade</h3>
            <p>The secure platform for campus trading.</p>
          </div>
          <div className="footer-section">
            <h3>Quick Links</h3>
            <ul>
              <li><a href="/">Home</a></li>
              <li><a href="/products">Products</a></li>
              <li><a href="/add-product">Sell Item</a></li>
              <li><a href="/wishlist">Wishlist</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h3>Contact</h3>
            <p>Email: support@campustrade.edu</p>
            <p>Phone: (123) 456-7890</p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; {currentYear} CampusTrade. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
