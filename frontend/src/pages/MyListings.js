// src/pages/MyListings.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const MyListings = () => {
  const [listings, setListings] = useState([]);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchListings = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:5001/myListings', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setListings(res.data.listings);
      } catch (err) {
        console.error("Error fetching listings:", err);
      }
    };

    fetchListings();
  }, [token]);

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Your Listings</h2>
      {listings.length === 0 ? (
        <p>No listings found.</p>
      ) : (
        <ul>
          {listings.map((listing) => (
            <li key={listing.Product_ID}>
              <strong>{listing.Title}</strong> - {listing.Description}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MyListings;
