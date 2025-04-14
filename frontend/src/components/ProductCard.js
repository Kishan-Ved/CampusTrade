// src/components/ProductCard.js
import React from 'react';

const ProductCard = ({ product }) => {
  return (
    <div style={{
      border: '1px solid #ccc',
      borderRadius: '10px',
      padding: '1rem',
      marginBottom: '1rem',
      maxWidth: '500px'
    }}>
      <h3>{product.name}</h3>
      <p><strong>Price:</strong> ₹{product.price}</p>
      <p><strong>Condition:</strong> {product.condition}</p>
      <p><strong>Seller:</strong> {product.sellerUsername}</p>
      <p>{product.description}</p>
    </div>
  );
};

export default ProductCard;
