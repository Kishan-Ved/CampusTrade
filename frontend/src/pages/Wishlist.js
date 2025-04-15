import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ProductCard from '../components/ProductCard'; // Assuming ProductCard is used for displaying individual product details

const Wishlist = () => {
  const [wishlist, setWishlist] = useState([]);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchWishlist = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:5001/getWishlist', {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.data.success) {
          setWishlist(res.data.wishlist);
        } else {
          alert(res.data.message || 'Error fetching wishlist');
        }
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
        <div className="product-grid">
          {wishlist.map((item) => (
            <ProductCard key={item.Product_ID} product={item} />
          ))}
        </div>
      )}
    </div>
  );
};

export default Wishlist;
