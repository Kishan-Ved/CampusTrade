import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AddProduct = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState('');
  const [condition, setCondition] = useState('new'); // Default condition is 'new'
  const [categoryId, setCategoryId] = useState('');
  const [categories, setCategories] = useState([]);
  const [image, setImage] = useState(null); // To hold the image file
  const token = localStorage.getItem('token');

  useEffect(() => {
    // Fetch categories on component mount
    const fetchCategories = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5001/getCategories', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
    
        console.log("Categories fetched:", response.data.categories); // Log the categories array
    
        const categoriesData = response.data.categories.map(category => ({
          id: category.Category_ID,
          name: category.Category_Name,
        }));
    
        setCategories(categoriesData);
      } catch (err) {
        console.error("Error fetching categories:", err);
      }
    };    
    fetchCategories();
  }, [token]);

  const handleImageChange = (e) => {
    setImage(e.target.files[0]); // Set the selected image file
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('price', price);
    formData.append('condition', condition);
    formData.append('categoryId', categoryId);
    formData.append('image', image);  // Add the image file here

    try {
      const response = await axios.post('http://127.0.0.1:5001/addProduct', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      alert('Product added successfully!');
    } catch (err) {
      console.error("Error adding product:", err);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Add New Product</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title:</label>
          <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div>
          <label>Description:</label>
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} required />
        </div>
        <div>
          <label>Price:</label>
          <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} required />
        </div>
        <div>
          <label>Condition:</label>
          <select value={condition} onChange={(e) => setCondition(e.target.value)} required>
            <option value="new">New</option>
            <option value="used">Used</option>
          </select>
        </div>
        <div>
          <label>Category:</label>
          <select value={categoryId} onChange={(e) => setCategoryId(e.target.value)} required>
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
        <div>
          <label>Product Image:</label>
          <input type="file" onChange={handleImageChange} required />
        </div>
        <button type="submit">Add Product</button>
      </form>
    </div>
  );
};

export default AddProduct;
