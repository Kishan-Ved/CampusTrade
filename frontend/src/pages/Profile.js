// src/pages/Profile.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        // This endpoint might need to be adjusted based on your actual API
        const res = await axios.get('http://127.0.0.1:5001/profile', {
          headers: { Authorization: `Bearer ${token}` },
        });
        
        if (res.data.success) {
          setProfile(res.data.profile);
        } else {
          setError('Failed to load profile data');
        }
      } catch (err) {
        console.error("Error fetching profile:", err);
        setError('An error occurred while loading your profile');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [token]);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading profile...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-message">
        <p>{error}</p>
        <p>This is a placeholder profile page. The actual profile endpoint may not be implemented in the backend yet.</p>
      </div>
    );
  }

  // If the profile endpoint is not implemented, show placeholder content
  if (!profile) {
    return (
      <div className="profile-page">
        <h1>My Profile</h1>
        
        <div className="profile-card">
          <div className="profile-header">
            <div className="profile-avatar">
              <img src="https://via.placeholder.com/150" alt="Profile" />
            </div>
            <div className="profile-info">
              <h2>Campus User</h2>
              <p>Student</p>
              <p>user@campus.edu</p>
            </div>
          </div>
          
          <div className="profile-stats">
            <div className="stat-item">
              <span className="stat-value">0</span>
              <span className="stat-label">Products Sold</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">0</span>
              <span className="stat-label">Products Bought</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">0</span>
              <span className="stat-label">Reviews</span>
            </div>
          </div>
          
          <div className="profile-actions">
            <button className="btn btn-primary">Edit Profile</button>
            <button className="btn">Change Password</button>
          </div>
        </div>
        
        <div className="profile-sections">
          <div className="section-card">
            <h3>Account Information</h3>
            <div className="info-item">
              <span className="info-label">Username:</span>
              <span className="info-value">campus_user</span>
            </div>
            <div className="info-item">
              <span className="info-label">Email:</span>
              <span className="info-value">user@campus.edu</span>
            </div>
            <div className="info-item">
              <span className="info-label">Role:</span>
              <span className="info-value">Student</span>
            </div>
            <div className="info-item">
              <span className="info-label">Member Since:</span>
              <span className="info-value">January 2023</span>
            </div>
          </div>
          
          <div className="section-card">
            <h3>Recent Activity</h3>
            <p>No recent activity to display.</p>
          </div>
        </div>
      </div>
    );
  }

  // If the profile endpoint is implemented, display the actual profile data
  return (
    <div className="profile-page">
      <h1>My Profile</h1>
      
      <div className="profile-card">
        <div className="profile-header">
          <div className="profile-avatar">
            <img src={profile.profileImage || "https://via.placeholder.com/150"} alt="Profile" />
          </div>
          <div className="profile-info">
            <h2>{profile.username}</h2>
            <p>{profile.role}</p>
            <p>{profile.email}</p>
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
            <span className="stat-value">{profile.reviewsCount || 0}</span>
            <span className="stat-label">Reviews</span>
          </div>
        </div>
        
        <div className="profile-actions">
          <button className="btn btn-primary">Edit Profile</button>
          <button className="btn">Change Password</button>
        </div>
      </div>
      
      <div className="profile-sections">
        <div className="section-card">
          <h3>Account Information</h3>
          <div className="info-item">
            <span className="info-label">Username:</span>
            <span className="info-value">{profile.username}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Email:</span>
            <span className="info-value">{profile.email}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Role:</span>
            <span className="info-value">{profile.role}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Member Since:</span>
            <span className="info-value">{profile.memberSince}</span>
          </div>
        </div>
        
        <div className="section-card">
          <h3>Recent Activity</h3>
          {profile.recentActivity && profile.recentActivity.length > 0 ? (
            <ul className="activity-list">
              {profile.recentActivity.map((activity, index) => (
                <li key={index} className="activity-item">
                  <span className="activity-date">{activity.date}</span>
                  <span className="activity-description">{activity.description}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p>No recent activity to display.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;
