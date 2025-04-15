import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const AddProduct = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState('');
  const [condition, setCondition] = useState('New'); // Default condition is 'New'
  const [categoryId, setCategoryId] = useState('');
  const [categories, setCategories] = useState([]);
  const [image, setImage] = useState(null); // For storing image as a file
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const token = localStorage.getItem('token');
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch categories on component mount
    const fetchCategories = async () => {
      try {
        setLoading(true);
        const response = await axios.get('http://127.0.0.1:5001/getCategories', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const categoriesData = response.data.categories.map(category => ({
          id: category.Category_ID,
          name: category.Category_Name,
        }));

        setCategories(categoriesData);
        setError(null);
      } catch (err) {
        console.error("Error fetching categories:", err);
        setError('Failed to load categories. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    fetchCategories();
  }, [token]);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result); // Set base64 encoded image
      };
      reader.readAsDataURL(file); // Read the file as base64 string
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // Prepare the data to send
      const productData = {
        title,
        description,
        price: parseFloat(price),
        condition,
        category_id: parseInt(categoryId),
        image: image // Send the image as a base64 string
      };

      // Send the data to the backend
      const response = await axios.post('http://127.0.0.1:5001/addProduct', productData, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.data.success) {
        setSuccess(true);
        // Reset form fields
        setTitle('');
        setDescription('');
        setPrice('');
        setCondition('New');
        setCategoryId('');
        setImage(null);

        // Show success message and redirect after a delay
        setTimeout(() => {
          navigate('/my-listings');
        }, 2000);
      } else {
        setError(response.data.error || 'Failed to add product');
      }
    } catch (err) {
      console.error("Error adding product:", err);
      setError(err.response?.data?.error || 'An error occurred while adding the product');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-product-page">
      <div className="form-container">
        <h1 className="form-title">Add New Product</h1>

        {error && (
          <div className="error-message">{error}</div>
        )}

        {success && (
          <div className="success-message">
            Product added successfully! Redirecting to your listings...
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              disabled={loading}
              placeholder="Enter product title"
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              disabled={loading}
              placeholder="Describe your product"
              rows="4"
            />
          </div>

          <div className="form-group">
            <label htmlFor="price">Price (₹)</label>
            <input
              type="number"
              id="price"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              required
              disabled={loading}
              min="0"
              step="0.01"
              placeholder="Enter price"
            />
          </div>

          <div className="form-group">
            <label htmlFor="condition">Condition</label>
            <select
              id="condition"
              value={condition}
              onChange={(e) => setCondition(e.target.value)}
              required
              disabled={loading}
            >
              <option value="New">New</option>
              <option value="Used">Used</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="category">Category</label>
            <select
              id="category"
              value={categoryId}
              onChange={(e) => setCategoryId(e.target.value)}
              required
              disabled={loading}
            >
              <option value="">Select Category</option>
              {Array.isArray(categories) && categories.length > 0 ? (
                categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))
              ) : (
                <option disabled>No categories available</option>
              )}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="image">Product Image (Optional)</label>
            <input
              type="file"
              id="image"
              accept="image/*"
              onChange={handleImageChange}
              disabled={loading}
            />
            <small>Upload an image of your product (.png)</small>
          </div>

          <div className="form-actions">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Adding Product...' : 'Add Product'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddProduct;
