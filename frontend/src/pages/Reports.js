// src/pages/Reports.js
import React, { useState } from 'react';
import axios from 'axios';

const Reports = () => {
  const [reportType, setReportType] = useState('');
  const token = localStorage.getItem('token');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:5001/reports', 
        { reportType },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('Report generated successfully!');
    } catch (err) {
      console.error("Error generating report:", err);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Generate Report</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Report Type:</label>
          <select onChange={(e) => setReportType(e.target.value)} required>
            <option value="sales">Sales Report</option>
            <option value="complaints">Complaints Report</option>
            <option value="reviews">Reviews Report</option>
          </select>
        </div>
        <button type="submit">Generate Report</button>
      </form>
    </div>
  );
};

export default Reports;
