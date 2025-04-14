// src/pages/Register.js
import React, { useState } from 'react';
import axios from 'axios';

function Register() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    dob: '',
    password: '',
    contact_no: '',
    age: '',
    role: 'Student'
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:5001/addMember', form);
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
        <input key={field} name={field} placeholder={field} onChange={handleChange} />
      ))}
      <select name="role" onChange={handleChange}>
        <option value="Student">Student</option>
        <option value="Faculty">Faculty</option>
        <option value="Staff">Staff</option>
      </select>
      <button onClick={handleRegister}>Register</button>
    </div>
  );
}

export default Register;
