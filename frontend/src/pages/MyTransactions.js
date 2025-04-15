import React, { useEffect, useState } from 'react';
import axios from 'axios';

const TransactionHistory = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:5001/getMyTransactions', {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (res.data.success && res.data.transactions) {
          setTransactions(res.data.transactions);
        } else {
          setError('No transactions found.');
        }
        setLoading(false);
      } catch (err) {
        console.error("Error fetching transactions:", err);
        setError('Failed to fetch transactions.');
        setLoading(false);
      }
    };

    fetchTransactions();
  }, [token]);

  return (
    <div style={{ padding: '2rem' }}>
      <h2>My Transactions</h2>
      {loading ? (
        <p>Loading transactions...</p>
      ) : error ? (
        <p>{error}</p>
      ) : transactions.length === 0 ? (
        <p>No transactions found.</p>
      ) : (
        <ul>
          {transactions.map((txn) => (
            <li key={txn.Transaction_ID} style={{ marginBottom: '1.5rem', borderBottom: '1px solid #ccc', paddingBottom: '1rem' }}>
              <div><strong>Transaction ID:</strong> {txn.Transaction_ID}</div>
              <div><strong>Title:</strong> {txn.Title}</div>
              <div><strong>Buyer ID:</strong> {txn.Buyer_ID}</div>
              <div><strong>Seller ID:</strong> {txn.Seller_ID}</div>
              <div><strong>Price:</strong> ${txn.Price}</div>
              <div><strong>Payment Method:</strong> {txn.Payment_Method}</div>
              <div><strong>Date:</strong> {new Date(txn.Transaction_Date).toLocaleString()}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TransactionHistory;
