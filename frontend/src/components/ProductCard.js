// src/components/ProductCard.js
import React from 'react';

const ProductCard = ({ product, onAddToWishlist, onBuyCredit, onBuyCash }) => {
  // Default image if none is provided
  const defaultImage = 'https://via.placeholder.com/300x200?text=No+Image';

  return (
    <div className="product-card">
      <div className="product-image-container">
        <img
          src={product.Image_URL || defaultImage}
          alt={product.Title || product.name}
          className="product-image"
        />
      </div>

      <div className="product-info">
        <h3 className="product-title">{product.Title || product.name}</h3>

        <div className="product-price">
          ₹{product.Price || product.price}
        </div>

        <div className="product-meta">
          <span className="product-condition">
            {product.Condition_ || product.condition}
          </span>
          {product.sellerUsername && (
            <span className="product-seller">
              Seller: {product.sellerUsername}
            </span>
          )}
        </div>

        <p className="product-description">
          {product.Description || product.description}
        </p>

        <div className="product-actions">
          {onAddToWishlist && (
            <button
              onClick={() => onAddToWishlist(product.Product_ID || product.id)}
              className="btn"
            >
              Add to Wishlist
            </button>
          )}

          {onBuyCredit && (
            <button
              onClick={() => onBuyCredit(product.Product_ID || product.id)}
              className="btn btn-secondary"
            >
              Buy with Credit
            </button>
          )}

          {onBuyCash && (
            <button
              onClick={() => onBuyCash(product.Product_ID || product.id)}
              className="btn btn-secondary"
            >
              Buy with Cash
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
