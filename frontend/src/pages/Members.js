// src/pages/Members.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ProductCard from '../components/ProductCard'; 

const Members = () => {
  const [members, setMembers] = useState([]);
  const [selectedMember, setSelectedMember] = useState(null);
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(false);
  const token = localStorage.getItem('token');

  // Fetch all members on mount
  useEffect(() => {
    const fetchMembers = async () => {
      setLoading(true);
      try {
        const res = await axios.get('http://localhost:5001/viewGroupMembers', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setMembers(res.data.members || []);
      } catch (err) {
        alert('Error fetching members');
      }
      setLoading(false);
    };
    fetchMembers();
    // eslint-disable-next-line
  }, []);

  // Fetch listings for a member
  const handleViewListings = async (member) => {
    setLoading(true);
    setSelectedMember(member);
    try {
      const res = await axios.post(
        'http://localhost:5001/getMemberListing',
        { member_id: member.Member_ID },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setListings(res.data.listings || []);
    } catch (err) {
      alert('Error fetching listings');
      setListings([]);
    }
    setLoading(false);
  };

  // Go back to members list
  const handleBack = () => {
    setSelectedMember(null);
    setListings([]);
  };

  // Add these functions inside the Members component (before return statement):
  const handleAddToWishlist = async (productId) => {
    try {
      await axios.post(
        'http://127.0.0.1:5001/addToWishlist',
        { product_id: productId },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('Added to wishlist!');
    } catch (err) {
      alert(err.response?.data?.message || 'Error adding to wishlist');
    }
  };

  const handleBuy = async (productId, mode) => {
    try {
      await axios.post(
        'http://127.0.0.1:5001/buyProduct',
        { Product_ID: productId, payment_mode: mode },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('Purchase successful!');
      // Refresh listings
      handleViewListings(selectedMember);
    } catch (err) {
      alert(err.response?.data?.message || 'Purchase failed');
    }
  };

  
  return (
    <div style={{ padding: '2rem', maxWidth: 900, margin: 'auto' }}>
      <h2>Group Members</h2>
      {loading && <p>Loading...</p>}

      {/* Show members list */}
      {!selectedMember && !loading && (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#f0f0f0' }}>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Contact</th>
              <th>Role</th>
              <th>Registered On</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {members.map((m) => (
              <tr key={m.Member_ID} style={{ borderBottom: '1px solid #ddd' }}>
                <td>{m.Member_ID}</td>
                <td>{m.Name}</td>
                <td>{m.Email}</td>
                <td>{m.Contact_No}</td>
                <td>{m.Role}</td>
                <td>{new Date(m.Registered_On).toLocaleString()}</td>
                <td>
                  <button
                    onClick={() => handleViewListings(m)}
                    style={{
                      background: '#1976d2',
                      color: '#fff',
                      border: 'none',
                      padding: '0.4rem 1rem',
                      borderRadius: 4,
                      cursor: 'pointer',
                    }}
                  >
                    View Listings
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Show listings for selected member */}
      {selectedMember && (
        <div>
          <button
            onClick={handleBack}
            style={{
              marginBottom: '1rem',
              background: '#eee',
              color: '#1976d2',
              border: '1px solid #1976d2',
              padding: '0.4rem 1rem',
              borderRadius: 4,
              cursor: 'pointer',
            }}
          >
            &larr; Back to Members
          </button>
          <h3>
            Listings by {selectedMember.Name} (ID: {selectedMember.Member_ID})
          </h3>
          {loading ? (
            <p>Loading...</p>
          ) : listings.length === 0 ? (
            <p>No listings found for this member.</p>
          ) : (
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {listings.map((l) => (
                <li
                  key={l.Product_ID}
                  style={{
                    border: '1px solid #ccc',
                    borderRadius: 6,
                    padding: '1rem',
                    marginBottom: '1rem',
                    background: '#fafbff',
                  }}
                >
                  <div>
                    <strong>Title:</strong> {l.Title}
                  </div>
                  <div>
                    <strong>Description:</strong> {l.Description}
                  </div>
                  <div>
                    <strong>Price:</strong> ₹{l.Price}
                  </div>
                  <div>
                    <strong>Category ID:</strong> {l.Category_ID}
                  </div>
                  <div>
                    <strong>Condition:</strong> {l.Condition}
                  </div>
                  <div>
                    <strong>Listed On:</strong>{' '}
                    {new Date(l.Listed_On).toLocaleString()}
                  </div>
                  {l.Image_Data && (
                    <div>
                      <img
                        src={`data:image/jpeg;base64,${l.Image_Data}`}
                        alt="Product"
                        style={{ maxWidth: 200, marginTop: 8 }}
                      />
                    </div>
                  )}
                  {/* Add buttons here */}
                  <div style={{ marginTop: '10px', display: 'flex', gap: '8px' }}>
                    <button 
                      onClick={() => handleAddToWishlist(l.Product_ID)}
                      style={{
                        background: '#4CAF50',
                        color: 'white',
                        border: 'none',
                        padding: '6px 12px',
                        borderRadius: '4px',
                        cursor: 'pointer'
                      }}
                    >
                      Add to Wishlist
                    </button>
                    <button
                      onClick={() => handleBuy(l.Product_ID, 'Cash')}
                      style={{
                        background: '#2196F3',
                        color: 'white',
                        border: 'none',
                        padding: '6px 12px',
                        borderRadius: '4px',
                        cursor: 'pointer'
                      }}
                    >
                      Buy with Cash
                    </button>
                    <button
                      onClick={() => handleBuy(l.Product_ID, 'Credit')}
                      style={{
                        background: '#9C27B0',
                        color: 'white',
                        border: 'none',
                        padding: '6px 12px',
                        borderRadius: '4px',
                        cursor: 'pointer'
                      }}
                    >
                      Buy on Credit
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default Members;
