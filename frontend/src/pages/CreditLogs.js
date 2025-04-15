import React, { useEffect, useState } from 'react';
import axios from 'axios';

const CreditLogs = () => {
  const [creditLog, setCreditLog] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchCreditLog = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:5001/getMyCreditLogs', {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (res.data.success && Array.isArray(res.data.credit_logs) && res.data.credit_logs.length > 0) {
          setCreditLog(res.data.credit_logs[0]); // Grab the first (and only) one
        } else {
          setError('No credit log found.');
        }

        setLoading(false);
      } catch (err) {
        console.error('Error fetching credit log:', err);
        setError('Failed to fetch credit log.');
        setLoading(false);
      }
    };

    if (token) {
      fetchCreditLog();
    } else {
      setError('You must be logged in to view your credit log.');
      setLoading(false);
    }
  }, [token]);

  return (
    <div style={{ padding: '2rem' }}>
      <h2>My Credit Balance</h2>

      {loading ? (
        <p>Loading credit log...</p>
      ) : error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : creditLog ? (
        <div
          style={{
            border: '1px solid #ddd',
            borderRadius: '8px',
            padding: '1.5rem',
            maxWidth: '500px',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
            backgroundColor: '#f9f9f9',
          }}
        >
          <div style={{ marginBottom: '1rem' }}>
            <strong>Credit ID:</strong> {creditLog.credit_ID || 'N/A'}
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <strong>Member ID:</strong> {creditLog.member_ID || 'N/A'}
          </div>
          <div>
            <strong>Balance:</strong>{' '}
            <span style={{ color: Number(creditLog.balance) >= 0 ? 'green' : 'red' }}>
              {creditLog.balance !== undefined && creditLog.balance !== null
                ? `Rs. ${Number(creditLog.balance).toFixed(2)}`
                : 'N/A'}
            </span>
          </div>
        </div>
      ) : (
        <p>No credit log available.</p>
      )}
    </div>
  );
};

export default CreditLogs;