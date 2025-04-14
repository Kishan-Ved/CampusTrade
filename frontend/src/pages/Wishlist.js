// src/pages/Wishlist.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Wishlist = () => {
  const [wishlist, setWishlist] = useState([]);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchWishlist = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:5001/wishlist', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setWishlist(res.data.wishlist);
      } catch (err) {
        console.error("Error fetching wishlist:", err);
      }
    };

    fetchWishlist();
  }, [token]);

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Your Wishlist</h2>
      {wishlist.length === 0 ? (
        <p>Your wishlist is empty.</p>
      ) : (
        <ul>
          {wishlist.map((item) => (
            <li key={item.Product_ID}>
              <strong>{item.Title}</strong> - {item.Description}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Wishlist;
