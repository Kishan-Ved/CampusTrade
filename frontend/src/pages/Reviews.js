// src/pages/Reviews.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Reviews = () => {
  const [reviews, setReviews] = useState([]);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:5001/reviews', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setReviews(res.data.reviews);
      } catch (err) {
        console.error("Error fetching reviews:", err);
      }
    };

    fetchReviews();
  }, [token]);

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Reviews</h2>
      {reviews.length === 0 ? (
        <p>No reviews available.</p>
      ) : (
        <ul>
          {reviews.map((review) => (
            <li key={review.Review_ID}>
              <strong>{review.Product_Title}</strong> - {review.Comment}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Reviews;
