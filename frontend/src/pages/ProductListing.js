import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ProductListing = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:5001/getProducts', {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.data.products) {
          setProducts(res.data.products);
        } else {
          console.error("No products found");
        }
        setLoading(false);
      } catch (err) {
        console.error("Error fetching products:", err);
        setError("Error fetching products.");
        setLoading(false);
      }
    };

    fetchProducts();
  }, [token]);

  const handleAddToWishlist = async (productId) => {
    try {
      const res = await axios.post(
        'http://127.0.0.1:5001/addToWishlist',
        { productId },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (res.data.success) {
        alert('Product added to wishlist!');
      } else {
        alert('Failed to add product to wishlist');
      }
    } catch (err) {
      console.error("Error adding product to wishlist:", err);
      alert('An error occurred. Please try again.');
    }
  };

  const BuyProductOnCredit = async (productId) => {
    try {
      const res = await axios.post(
        'http://127.0.0.1:5001/buyProduct',
        { "Product_ID" : productId, "payment_mode": "Credit" },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (res.data.success) {
        alert('Product purchased!');
      } else {
        alert('Failed to purchase the product');
      }
    } catch (err) {
      console.error("Error in buying the product:", err);
      alert('An error occurred. Please try again.');
    }
  };

  const BuyProductWithCash = async (productId) => {
    try {
      const res = await axios.post(
        'http://127.0.0.1:5001/buyProduct',
        { "Product_ID" : productId, "payment_mode": "Cash" },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (res.data.success) {
        alert('Product purchased!');
      } else {
        alert('Failed to purchase the product');
      }
    } catch (err) {
      console.error("Error in buying the product:", err);
      alert('An error occurred. Please try again.');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Available Products</h2>
      {loading ? (
        <p>Loading products...</p>
      ) : error ? (
        <p>{error}</p>
      ) : products.length === 0 ? (
        <p>No products available.</p>
      ) : (
        <ul>
          {products.map((product) => (
            <li key={product.Product_ID} style={{ marginBottom: '1rem' }}>
              <div>
                <strong>{product.Title}</strong>
              </div>
              <div>{product.Description}</div>
              <div>Price: ${product.Price}</div>
              <div>Condition: {product.Condition_}</div>
              <div>Category ID: {product.Category_ID}</div>
              <div>
                {product.Image_URL && <img src={product.Image_URL} alt={product.Title} style={{ width: '150px', height: 'auto' }} />}
              </div>
              <div>
                <button onClick={() => handleAddToWishlist(product.Product_ID)}>
                  Add to Wishlist
                </button>

                <button onClick={() => BuyProductOnCredit(product.Product_ID)}>
                  Buy on Credit
                </button>

                <button onClick={() => BuyProductWithCash(product.Product_ID)}>
                  Buy with Cash
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ProductListing;
