// src/pages/MyListings.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ProductCard from '../components/ProductCard';
import { Link } from 'react-router-dom';

const MyListings = () => {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState(null);
  const token = localStorage.getItem('token');

  const fetchListings = async () => {
    try {
      setLoading(true);
      setError(null);

      const res = await axios.get('http://127.0.0.1:5001/myListings', {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.data.success) {
        setListings(res.data.listings || []);
      } else {
        setError(res.data.error || 'Failed to fetch your listings');
      }
    } catch (err) {
      console.error("Error fetching listings:", err);
      setError(err.response?.data?.error || 'An error occurred while fetching your listings');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchListings();
  }, [token]);

  const handleDeleteListing = async (productId) => {
    // Confirm before deleting
    if (!window.confirm('Are you sure you want to delete this product?')) {
      return;
    }

    try {
      setDeleteLoading(true);

      const res = await axios.delete(`http://127.0.0.1:5001/deleteProduct/${productId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.data.message) {
        // Remove the deleted product from the listings state
        setListings(listings.filter(listing => listing.Product_ID !== productId));
        setSuccessMessage('Product deleted successfully');

        // Clear success message after 3 seconds
        setTimeout(() => {
          setSuccessMessage(null);
        }, 3000);
      }
    } catch (err) {
      console.error("Error deleting product:", err);
      setError(err.response?.data?.error || 'Failed to delete product. Please try again.');

      // Clear error message after 3 seconds
      setTimeout(() => {
        setError(null);
      }, 3000);
    } finally {
      setDeleteLoading(false);
    }
  };

  const handleEditListing = (productId) => {
    // For now, just alert. In a real app, you might redirect to an edit page
    alert(`Edit functionality for product ${productId} will be implemented in the future.`);
  };

  return (
    <div className="my-listings-page">
      <div className="page-header">
        <h1>Your Listings</h1>
        <Link to="/add-product" className="btn btn-primary">Add New Product</Link>
      </div>

      {successMessage && (
        <div className="success-message">{successMessage}</div>
      )}

      {error && (
        <div className="error-message">{error}</div>
      )}

      {loading ? (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading your listings...</p>
        </div>
      ) : listings.length === 0 ? (
        <div className="no-listings-message">
          <p>You haven't listed any products yet.</p>
          <Link to="/add-product" className="btn btn-primary">Add Your First Product</Link>
        </div>
      ) : (
        <>
          <div className="listings-summary">
            <p>You have <strong>{listings.length}</strong> active listing{listings.length !== 1 ? 's' : ''}.</p>
          </div>

          <div className="product-grid">
            {listings.map((listing) => (
              <div key={listing.Product_ID} className="my-product-card-container">
                <ProductCard product={listing} />
                <div className="my-product-actions">
                  <button
                    onClick={() => handleEditListing(listing.Product_ID)}
                    className="btn btn-secondary"
                    disabled={deleteLoading}
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDeleteListing(listing.Product_ID)}
                    className="btn btn-danger"
                    disabled={deleteLoading}
                  >
                    {deleteLoading ? 'Deleting...' : 'Delete'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default MyListings;
