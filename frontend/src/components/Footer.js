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
            <p>
                Report an Issue:{" "}
                <a
                  href="https://github.com/Kishan-Ved/CampusTrade/issues"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Click here to report a bug on GitHub
                </a>
              </p>
          </div>
          <div className="footer-section">
            <h3>Quick Links</h3>
            <ul>
              <li><a href="/">Home</a></li>
              <li><a href="/products">Products</a></li>
              <li><a href="/add-product">Sell Item</a></li>
              <li><a href="/wishlist">Wishlist</a></li>
              <li><a href="/getMyTransactions">Transactions</a></li>
              <li><a href="/members">Members</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h3>Developers</h3>
            <p>
              Aditya Mehta: <a href="mailto:aditya.mehta@iitgn.ac.in">aditya.mehta@iitgn.ac.in</a>
            </p>
            <p>
              Jiya Desai: <a href="mailto:jiya.desai@iitgn.ac.in">jiya.desai@iitgn.ac.in</a>
            </p>
            <p>
              Kishan Ved: <a href="mailto:kishan.ved@iitgn.ac.in">kishan.ved@iitgn.ac.in</a>
            </p>
            <p>
              Nimitt: <a href="mailto:nimitt.nimitt@iitgn.ac.in">nimitt.nimitt@iitgn.ac.in</a>
            </p>
            <p>
              Pratham Shards: <a href="mailto:pratham.sharda@iitgn.ac.in">pratham.sharda@iitgn.ac.in</a>
            </p>
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
