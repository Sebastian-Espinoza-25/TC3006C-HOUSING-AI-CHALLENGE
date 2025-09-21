// @author Santiago Villazón Ponce de León | A01746396

// src/guards/RequireAuth.jsx
import { Navigate } from "react-router-dom";

export default function RequireAuth({ children }) {
  const token = localStorage.getItem("token");
  if (!token) return <Navigate to="/login" replace />;
  return children;
}
