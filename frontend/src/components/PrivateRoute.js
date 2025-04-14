import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';

// This component will protect any route from being accessed if the user is not logged in
const PrivateRoute = ({ element }) => {
  const { authState } = useContext(AuthContext);

  if (!authState.isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return element;
};

export default PrivateRoute;
