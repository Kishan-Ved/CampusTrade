// src/pages/Complaints.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Complaints = () => {
  const [complaint, setComplaint] = useState('');
  const [complaints, setComplaints] = useState([]);
  const [viewMode, setViewMode] = useState('file'); // 'file' or 'view'
  const [loading, setLoading] = useState(false);
  const token = localStorage.getItem('token');

  // Fetch complaints when switching to view mode
  useEffect(() => {
    if (viewMode === 'view') {
      fetchComplaints();
    }
    // eslint-disable-next-line
  }, [viewMode]);

  const fetchComplaints = async () => {
    setLoading(true);
    try {
      const res = await axios.get('http://127.0.0.1:5001/viewComplaints', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setComplaints(res.data.complaints || []);
    } catch (err) {
      alert('Error fetching complaints');
      setComplaints([]);
    }
    setLoading(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!complaint.trim()) return;
    try {
      await axios.post(
        'http://127.0.0.1:5001/addComplaint',
        { description: complaint },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('Complaint submitted successfully!');
      setComplaint('');
      setViewMode('view');
    } catch (err) {
      alert('Error submitting complaint');
    }
  };

  const handleToggleStatus = async (complaintId) => {
    try {
      await axios.post(
        'http://127.0.0.1:5001/toggleComplaintStatus',
        { complaint_id: complaintId },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      // Refresh complaints list
      fetchComplaints();
    } catch (err) {
      alert('Error toggling complaint status');
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: 600, margin: 'auto' }}>
      <h2>Complaints Portal</h2>
      <div style={{ marginBottom: '1rem' }}>
        <button
          onClick={() => setViewMode('file')}
          style={{
            marginRight: '1rem',
            background: viewMode === 'file' ? '#1976d2' : '#eee',
            color: viewMode === 'file' ? '#fff' : '#000',
            border: 'none',
            padding: '0.5rem 1rem',
            borderRadius: 4,
            cursor: 'pointer',
          }}
        >
          File New Complaint
        </button>
        <button
          onClick={() => setViewMode('view')}
          style={{
            background: viewMode === 'view' ? '#1976d2' : '#eee',
            color: viewMode === 'view' ? '#fff' : '#000',
            border: 'none',
            padding: '0.5rem 1rem',
            borderRadius: 4,
            cursor: 'pointer',
          }}
        >
          View My Complaints
        </button>
      </div>

      {viewMode === 'file' && (
        <form onSubmit={handleSubmit}>
          <div>
            <label>Complaint:</label>
            <textarea
              value={complaint}
              onChange={(e) => setComplaint(e.target.value)}
              required
              rows={4}
              style={{ width: '100%', marginTop: 8, marginBottom: 16 }}
            />
          </div>
          <button type="submit" style={{ padding: '0.5rem 1.5rem' }}>
            Submit Complaint
          </button>
        </form>
      )}

      {viewMode === 'view' && (
        <div>
          <h3>My Complaints</h3>
          {loading ? (
            <p>Loading...</p>
          ) : complaints.length === 0 ? (
            <p>No complaints found.</p>
          ) : (
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {complaints.map((c) => (
                <li
                  key={c.complaint_id}
                  style={{
                    border: '1px solid #ccc',
                    borderRadius: 6,
                    padding: '1rem',
                    marginBottom: '1rem',
                    background: c.status === 'Resolved' ? '#e0ffe0' : '#fff',
                  }}
                >
                  <div>
                    <strong>ID:</strong> {c.complaint_id}
                  </div>
                  <div>
                    <strong>Description:</strong> {c.description}
                  </div>
                  <div>
                    <strong>Status:</strong>{' '}
                    <span
                      style={{
                        color: c.status === 'Resolved' ? 'green' : 'orange',
                        fontWeight: 'bold',
                      }}
                    >
                      {c.status}
                    </span>
                  </div>
                  <div>
                    <strong>Filed On:</strong> {c.filed_on}
                  </div>
                  <button
                    onClick={() => handleToggleStatus(c.complaint_id)}
                    style={{
                      marginTop: 8,
                      background: '#1976d2',
                      color: '#fff',
                      border: 'none',
                      padding: '0.4rem 1rem',
                      borderRadius: 4,
                      cursor: 'pointer',
                    }}
                  >
                    Toggle Status
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default Complaints;
