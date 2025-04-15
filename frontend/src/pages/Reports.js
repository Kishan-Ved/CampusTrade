// // // src/pages/Reports.js
// // import React, { useState } from 'react';
// // import axios from 'axios';

// // const Reports = () => {
// //   const [reportType, setReportType] = useState('');
// //   const token = localStorage.getItem('token');

// //   const handleSubmit = async (e) => {
// //     e.preventDefault();

// //     try {
// //       const response = await axios.post('http://127.0.0.1:5001/reports', 
// //         { reportType },
// //         { headers: { Authorization: `Bearer ${token}` } }
// //       );
// //       alert('Report generated successfully!');
// //     } catch (err) {
// //       console.error("Error generating report:", err);
// //     }
// //   };

// //   return (
// //     <div style={{ padding: '2rem' }}>
// //       <h2>Generate Report</h2>
// //       <form onSubmit={handleSubmit}>
// //         <div>
// //           <label>Report Type:</label>
// //           <select onChange={(e) => setReportType(e.target.value)} required>
// //             <option value="sales">Sales Report</option>
// //             <option value="complaints">Complaints Report</option>
// //             <option value="reviews">Reviews Report</option>
// //           </select>
// //         </div>
// //         <button type="submit">Generate Report</button>
// //       </form>
// //     </div>
// //   );
// // };

// // export default Reports;



// import React, { useEffect, useState } from 'react';
// import axios from 'axios';

// const Reports = () => {
//   const [reports, setReports] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);
//   const token = localStorage.getItem('token');

//   useEffect(() => {
//     const fetchReports = async () => {
//       try {
//         const res = await axios.get('http://127.0.0.1:5001/getReportAnalytics', {
//           headers: { Authorization: `Bearer ${token}` },
//         });

//         if (res.data.success && Array.isArray(res.data.report_analytics)) {
//           setReports(res.data.report_analytics);
//         } else {
//           setError('No reports found.');
//         }
//         setLoading(false);
//       } catch (err) {
//         console.error('Error fetching reports:', err);
//         setError('Failed to fetch reports.');
//         setLoading(false);
//       }
//     };

//     if (token) {
//       fetchReports();
//     } else {
//       setError('You must be logged in to view reports.');
//       setLoading(false);
//     }
//   }, [token]);

//   return (
//     <div style={{ padding: '2rem' }}>
//       <h2>Report Analytics</h2>

//       {loading ? (
//         <p>Loading reports...</p>
//       ) : error ? (
//         <p style={{ color: 'red' }}>{error}</p>
//       ) : reports.length === 0 ? (
//         <p>No reports available.</p>
//       ) : (
//         <ul>
//           {reports.map((report) => (
//             <li
//               key={report.Report_ID}
//               style={{
//                 marginBottom: '1.5rem',
//                 borderBottom: '1px solid #ccc',
//                 paddingBottom: '1rem',
//                 maxWidth: '600px',
//               }}
//             >
//               <div><strong>Report ID:</strong> {report.Report_ID}</div>
//               <div><strong>Type:</strong> {report.Report_Type}</div>
//               <div><strong>Generated On:</strong> {new Date(report.Generated_On).toLocaleString()}</div>
//             </li>
//           ))}
//         </ul>
//       )}
//     </div>
//   );
// };

// export default Reports;


import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Reports = () => {
  const [reportTypes, setReportTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const res = await axios.post('http://127.0.0.1:5001/getReportAnalytics', {}, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (res.data.success && Array.isArray(res.data.report_analytics)) {
          const types = res.data.report_analytics.map(report => report.Report_Type);
          setReportTypes(types);
        } else {
          setError('No reports found.');
        }
        setLoading(false);
      } catch (err) {
        console.error('Error fetching reports:', err);
        setError('Failed to fetch reports.');
        setLoading(false);
      }
    };

    if (token) {
      fetchReports();
    } else {
      setError('You must be logged in to view reports.');
      setLoading(false);
    }
  }, [token]);

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h2 className="mb-4 text-primary">View the total sales of all members so far - where are you on the leaderboard?!</h2>

      {loading ? (
        <p>Loading reports...</p>
      ) : error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : reportTypes.length === 0 ? (
        <p>No report types available.</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {reportTypes.map((type, index) => (
            <li
              key={index}
              style={{
                background: '#f8f9fa',
                padding: '1rem',
                marginBottom: '1rem',
                borderRadius: '0.5rem',
                border: '1px solid #dee2e6',
                fontWeight: '500',
              }}
            >
              {index + 1}. {type}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Reports;