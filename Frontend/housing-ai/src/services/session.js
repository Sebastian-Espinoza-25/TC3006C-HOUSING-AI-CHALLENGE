// src/auth/session.js
export function getUser() {
  try { return JSON.parse(localStorage.getItem("user") || "null"); }
  catch { return null; }
}
export function getRole() {
  return localStorage.getItem("role") || null; // "client" | "vendor"
}
export function isAuthed() {
  return !!(localStorage.getItem("token") || getUser());
}
export function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  localStorage.removeItem("role");
  localStorage.removeItem("vendorId");
  window.location.assign("/login");
}
