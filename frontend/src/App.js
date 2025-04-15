import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Home from './pages/Home';
import Register from './pages/Register';
import Login from './pages/Login';
import ProductListing from './pages/ProductListing';
import AddProduct from './pages/AddProduct';
import Wishlist from './pages/Wishlist';
import MyListings from './pages/MyListings';
import Reviews from './pages/Reviews';
import Complaints from './pages/Complaints';
import Reports from './pages/Reports';
import TransactionHistory from './pages/MyTransactions';
import MyReviews from './pages/Reviews';
import PrivateRoute from './components/PrivateRoute';


function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/products" element={<PrivateRoute element={<ProductListing />} />} />
          <Route path="/add-product" element={<PrivateRoute element={<AddProduct />} />} />
          <Route path="/wishlist" element={<PrivateRoute element={<Wishlist />} />} />
          <Route path="/my-listings" element={<PrivateRoute element={<MyListings />} />} />
          <Route path="/reviews" element={<PrivateRoute element={<MyReviews />} />} />
          <Route path="/complaints" element={<PrivateRoute element={<Complaints />} />} />
          <Route path="/reports" element={<PrivateRoute element={<Reports />} />} />
          <Route path="/getMyTransactions" element={<PrivateRoute element={<TransactionHistory />} />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
