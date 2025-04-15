import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MyReviews = () => {
  const [reviewedUserId, setReviewedUserId] = useState('');
  const [rating, setRating] = useState(5);
  const [reviewText, setReviewText] = useState('');
  const [givenReviews, setGivenReviews] = useState([]);
  const [receivedReviews, setReceivedReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [myId, setMyId] = useState(null);
  const token = localStorage.getItem('token');

  // Decode JWT to get user ID
  const parseJwt = (token) => {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch (e) {
      console.error('JWT decode failed:', e);
      return null;
    }
  };

  // Fetch reviews on mount
  useEffect(() => {
    const fetchReviews = async () => {
      if (!token) return;

      const decoded = parseJwt(token);
      const userId = decoded?.user_id;

      if (!userId) {
        setError('Could not extract user ID from token.');
        return;
      }

      setMyId(userId);

      try {
        const res = await axios.get('http://127.0.0.1:5001/getMyReviews', {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (res.data.success && res.data.reviews) {
          const reviews = res.data.reviews;

          const given = reviews.filter(r => String(r.Reviewer_ID) === String(userId));
          const received = reviews.filter(r => String(r.Reviewed_User_ID) === String(userId));

          setGivenReviews(given);
          setReceivedReviews(received);
        } else {
          setError('No reviews found.');
        }
      } catch (err) {
        console.error('Error fetching reviews:', err);
        setError('Failed to load reviews.');
      } finally {
        setLoading(false);
      }
    };

    fetchReviews();
  }, [token]);

  // Handle review submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post(
        'http://127.0.0.1:5001/addReview',
        {
          Reviewed_User_ID: reviewedUserId,
          Rating: rating,
          Review_Text: reviewText,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (res.data.success) {
        alert('Review submitted!');
        setReviewedUserId('');
        setRating(5);
        setReviewText('');
        try {
          const res = await axios.get('http://127.0.0.1:5001/getMyReviews',
            // Payload is not needed here, fix this if there is a bug later

            // {
            //   Reviewed_User_ID: reviewedUserId,
            //   Rating: rating,
            //   Review_Text: reviewText,
            // },
            {
            headers: { Authorization: `Bearer ${token}` },
          });

          if (res.data.success && res.data.reviews) {
            const reviews = res.data.reviews;
            const given = reviews.filter(r => String(r.Reviewer_ID) === String(myId));
            setGivenReviews(given);
          } else {
            alert('Failed to fetch updated reviews.');
          }
        } catch (err) {
          console.error('Error fetching updated reviews:', err);
          alert('An error occurred while fetching updated reviews.');
        }
      } else {
        alert('Failed to submit review.');
      }
    } catch (err) {
      console.error('Error submitting review:', err);
      alert('An error occurred. Please try again.');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Submit a Review</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
        <div>
          <label>Reviewed User ID:</label>
          <input
            type="number"
            value={reviewedUserId}
            onChange={(e) => setReviewedUserId(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Rating (1-5):</label>
          <input
            type="number"
            min="1"
            max="5"
            value={rating}
            onChange={(e) => setRating(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Review Text:</label>
          <textarea
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            required
          />
        </div>
        <button type="submit">Submit Review</button>
      </form>

      <h2>Reviews You've Given</h2>
      {loading ? (
        <p>Loading...</p>
      ) : givenReviews.length === 0 ? (
        <p>No reviews written yet.</p>
      ) : (
        <ul>
          {givenReviews.map((r) => (
            <li key={r.Review_ID} style={{ marginBottom: '1rem' }}>
              <div><strong>To User ID:</strong> {r.Reviewed_User_ID}</div>
              <div><strong>Rating:</strong> {r.Rating}</div>
              <div><strong>Review:</strong> {r.Review_Text}</div>
              <div><strong>Date:</strong> {new Date(r.Timestamp).toLocaleString()}</div>
            </li>
          ))}
        </ul>
      )}

      <h2>Reviews You've Received</h2>
      {loading ? (
        <p>Loading...</p>
      ) : receivedReviews.length === 0 ? (
        <p>No reviews received yet.</p>
      ) : (
        <ul>
          {receivedReviews.map((r) => (
            <li key={r.Review_ID} style={{ marginBottom: '1rem' }}>
              <div><strong>From User ID:</strong> {r.Reviewer_ID}</div>
              <div><strong>Rating:</strong> {r.Rating}</div>
              <div><strong>Review:</strong> {r.Review_Text}</div>
              <div><strong>Date:</strong> {new Date(r.Timestamp).toLocaleString()}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MyReviews;
