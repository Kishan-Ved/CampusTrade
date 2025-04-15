import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [credit, setCredit] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchProfileAndCredit = async () => {
      setLoading(true);
      try {
        // Fetch profile
        const resProfile = await axios.get('http://127.0.0.1:5001/profile', {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (resProfile.data.success) {
          setProfile(resProfile.data.profile);
        } else {
          setError('Failed to load profile data');
        }

        // Fetch credit logs
        const resCredit = await axios.get('http://127.0.0.1:5001/getMyCreditLogs', {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (resCredit.data.success && Array.isArray(resCredit.data.credit_logs) && resCredit.data.credit_logs.length > 0) {
          setCredit(resCredit.data.credit_logs[0].balance);
        } else {
          setCredit(0);
        }
      } catch (err) {
        console.error("Error fetching profile or credit:", err);
        setError('An error occurred while loading your profile');
      } finally {
        setLoading(false);
      }
    };

    fetchProfileAndCredit();
  }, [token]);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading profile...</p>
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="error-message">
        <p>{error || "Profile not found."}</p>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <h1>My Profile</h1>
      <div className="profile-card">
        <div className="profile-header">
          <div className="profile-avatar">
            <img
              src={
                profile.Profile_Image
                  ? `data:image/png;base64,${profile.Profile_Image}`
                  : "https://via.placeholder.com/150"
              }
              alt="Profile"
            />
          </div>
          <div className="profile-info">
            <h2>{profile.Name}</h2>
            <p>{profile.Role}</p>
            <p>{profile.Email}</p>
          </div>
        </div>

        <div className="profile-stats">
          <div className="stat-item">
            <span className="stat-value">{profile.productsSold || 0}</span>
            <span className="stat-label">Products Sold</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">{profile.productsBought || 0}</span>
            <span className="stat-label">Products Bought</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">{credit}</span>
            <span className="stat-label">Current Credit</span>
          </div>
        </div>

        {/* <div className="profile-actions">
          <button className="btn btn-primary">Edit Profile</button>
          <button className="btn">Change Password</button>
        </div> */}
      </div>

      <div className="profile-sections">
        <div className="section-card">
          <h3>Account Information</h3>
          <div className="info-item">
            <span className="info-label">Name:</span>
            <span className="info-value">{profile.Name}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Email:</span>
            <span className="info-value">{profile.Email}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Contact No:</span>
            <span className="info-value">{profile.Contact_No}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Role:</span>
            <span className="info-value">{profile.Role}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Age:</span>
            <span className="info-value">{profile.Age}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Member Since:</span>
            <span className="info-value">
              {new Date(profile.Registered_On).toLocaleDateString()}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
