// @author Santiago Villazón Ponce de León | A01746396

import { Navigate } from "react-router-dom";

export default function RoleGate({ allow = [], children }) {
  const role = localStorage.getItem("role"); // "client" | "vendor"
  if (allow.length && !allow.includes(role)) return <Navigate to="/" replace />;
  return children;
}
