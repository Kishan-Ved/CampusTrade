// src/pages/Register.js
import React, { useState } from 'react';
import axios from 'axios';

function Register() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    dob: 'yyyy-mm-dd',
    password: '',
    contact_no: '',
    age: '',
    role: 'Student'
  });

  // State for profile image
  const [profileImage, setProfileImage] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Handle image file input
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfileImage(reader.result); // base64 string
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRegister = async () => {
    try {
      // Send form data along with profile image
      const res = await axios.post('http://127.0.0.1:5001/addMember', {
        ...form,
        profile_image: profileImage
      });
      alert('Registration successful! Member ID: ' + res.data.member_id);
    } catch (err) {
      console.error('Registration failed:', err);
      if (err.response && err.response.data && err.response.data.error) {
        alert('Registration failed: ' + err.response.data.error);
      } else {
        alert('Registration failed: ' + err.message);
      }
    }
  };

  return (
    <div>
      <h2>Register</h2>
      {['username', 'email', 'dob', 'password', 'contact_no', 'age'].map((field) => (
        <input
          key={field}
          name={field}
          placeholder={field}
          onChange={handleChange}
        />
      ))}
      <select name="role" onChange={handleChange}>
        <option value="Student">Student</option>
        <option value="Faculty">Faculty</option>
        <option value="Staff">Staff</option>
      </select>
      {/* Profile image input */}
      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
      />
      <p>Upload a profile image (optional)</p>
      <br />
      <button onClick={handleRegister}>Register</button>
    </div>
  );
}

export default Register;
