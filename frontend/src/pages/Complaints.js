// src/pages/Complaints.js
import React, { useState } from 'react';
import axios from 'axios';

const Complaints = () => {
  const [complaint, setComplaint] = useState('');
  const token = localStorage.getItem('token');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await axios.post('http://127.0.0.1:5001/complaints', 
        { complaint },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      alert('Complaint submitted successfully!');
    } catch (err) {
      console.error("Error submitting complaint:", err);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Submit a Complaint</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Complaint:</label>
          <textarea 
            value={complaint} 
            onChange={(e) => setComplaint(e.target.value)} 
            required 
          />
        </div>
        <button type="submit">Submit Complaint</button>
      </form>
    </div>
  );
};

export default Complaints;
