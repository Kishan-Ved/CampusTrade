import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ProductCard from '../components/ProductCard';

const ProductListing = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
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

    const fetchCategories = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:5001/getCategories', {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.data.categories) {
          setCategories(res.data.categories);
        }
      } catch (err) {
        console.error("Error fetching categories:", err);
      }
    };

    fetchProducts();
    fetchCategories();
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

  const buyProductOnCredit = async (productId) => {
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
        const updatedProducts = await axios.get('http://127.0.0.1:5001/getProducts', {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (updatedProducts.data.products) {
          setProducts(updatedProducts.data.products);
        }
      } else {
        alert('Failed to purchase the product');
      }
    } catch (err) {
      console.error("Error in buying the product:", err);
      alert('An error occurred. Please try again.');
    }
  };

  const buyProductWithCash = async (productId) => {
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
        const updatedProducts = await axios.get('http://127.0.0.1:5001/getProducts', {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (updatedProducts.data.products) {
          setProducts(updatedProducts.data.products);
        }
      } else {
        alert('Failed to purchase the product');
      }
    } catch (err) {
      console.error("Error in buying the product:", err);
      alert('An error occurred. Please try again.');
    }
  };

  // Filter products based on category and search term
  const filteredProducts = products.filter(product => {
    const matchesCategory = selectedCategory ? product.Category_ID === parseInt(selectedCategory) : true;
    const matchesSearch = searchTerm.trim() === '' ? true :
      (product.Title && product.Title.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (product.Description && product.Description.toLowerCase().includes(searchTerm.toLowerCase()));

    return matchesCategory && matchesSearch;
  });

  return (
    <div className="products-page">
      <h1>Available Products</h1>

      <div className="filters-container">
        <div className="search-container">
          <input
            type="text"
            placeholder="Search products..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="category-filter">
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="category-select"
          >
            <option value="">All Categories</option>
            {categories.map(category => (
              <option key={category.Category_ID} value={category.Category_ID}>
                {category.Category_Name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading products...</p>
        </div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : filteredProducts.length === 0 ? (
        <div className="no-products-message">
          <p>No products available.</p>
          {searchTerm || selectedCategory ? (
            <button
              onClick={() => {
                setSearchTerm('');
                setSelectedCategory('');
              }}
              className="btn btn-secondary"
            >
              Clear Filters
            </button>
          ) : null}
        </div>
      ) : (
        <div className="product-grid">
          {filteredProducts.map((product) => (
            <ProductCard
              key={product.Product_ID}
              product={product}
              onAddToWishlist={handleAddToWishlist}
              onBuyCredit={buyProductOnCredit}
              onBuyCash={buyProductWithCash}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default ProductListing;
