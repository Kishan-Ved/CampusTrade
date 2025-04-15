import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Delete_Members = () => {
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  const token = localStorage.getItem('token');

  // Fetch all members on mount
  const fetchMembers = async () => {
    setLoading(true);
    try {
      const res = await axios.get('http://localhost:5001/viewGroupMembers', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMembers(res.data.members || []);
    } catch (err) {
      setMessage({
        type: 'error',
        text: err.response?.data?.error || 'Error fetching members'
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMembers();
    // eslint-disable-next-line
  }, []);

  // Handle member deletion
  const handleDeleteMember = async (memberId, memberName) => {
    // Confirm before deleting
    if (!window.confirm(`Are you sure you want to delete member ${memberName}?`)) {
      return;
    }

    setDeleteLoading(true);
    try {
      const response = await axios.delete('http://localhost:5001/deleteMember', {
        headers: { Authorization: `Bearer ${token}` },
        data: { member_id: memberId } // Send data in request body for DELETE
      });

      // Show success message
      setMessage({
        type: 'success',
        text: response.data.message || 'Member deleted successfully'
      });

      // Refresh the members list
      fetchMembers();
    } catch (err) {
      setMessage({
        type: 'error',
        text: err.response?.data?.error || 'Failed to delete member'
      });
      console.error("Error deleting member:", err);
    } finally {
      setDeleteLoading(false);
      
      // Clear message after 3 seconds
      setTimeout(() => {
        setMessage({ type: '', text: '' });
      }, 3000);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: 900, margin: 'auto' }}>
      <h2>Delete Members</h2>
      
      {message.text && (
        <div 
          style={{ 
            padding: '10px', 
            marginBottom: '20px', 
            borderRadius: '5px',
            backgroundColor: message.type === 'success' ? '#d4edda' : '#f8d7da',
            color: message.type === 'success' ? '#155724' : '#721c24'
          }}
        >
          {message.text}
        </div>
      )}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <p>Loading...</p>
        </div>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#f0f0f0' }}>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Contact</th>
              <th>Role</th>
              <th>Registered On</th>
              <th>Delete</th>
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
                    onClick={() => handleDeleteMember(m.Member_ID, m.Name)}
                    disabled={deleteLoading}
                    style={{
                      background: '#dc3545',
                      color: '#fff',
                      border: 'none',
                      padding: '0.4rem 1rem',
                      borderRadius: 4,
                      cursor: 'pointer',
                      opacity: deleteLoading ? 0.7 : 1,
                    }}
                  >
                    {deleteLoading ? 'Deleting...' : 'Delete'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {members.length === 0 && !loading && (
        <p style={{ textAlign: 'center', padding: '20px' }}>No members found.</p>
      )}
    </div>
  );
};

export default Delete_Members;