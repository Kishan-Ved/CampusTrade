import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ProductCard from '../components/ProductCard'; // Make sure this exists and accepts onDelete

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

  const handleDelete = async (productId) => {
    try {
      const res = await axios.delete('http://127.0.0.1:5001/deletefromwishlist', {
        headers: { Authorization: `Bearer ${token}` },
        data: { Product_ID: productId },
      });

      if (res.data.success) {
        // Remove the item from state
        setWishlist((prevWishlist) =>
          prevWishlist.filter((item) => item.Product_ID !== productId)
        );
      } else {
        alert(res.data.message || 'Failed to delete item from wishlist');
      }
    } catch (err) {
      console.error("Error deleting product from wishlist:", err);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Your Wishlist</h2>
      {wishlist.length === 0 ? (
        <p>Your wishlist is empty.</p>
      ) : (
        <div className="product-grid">
          {wishlist.map((item) => (
            <ProductCard
              key={item.Product_ID}
              product={item}
              onRemoveWishlist={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Wishlist;
