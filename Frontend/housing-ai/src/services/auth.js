// src/services/auth.js
const API = process.env.REACT_APP_API || "http://localhost:5001"; // asegúrate del puerto correcto

export async function login(identifier, password, role = "auto") {
  const res = await fetch(`${API}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ identifier, password, role })
  });
  if (!res.ok) {
    const msg = await res.json().catch(() => ({}));
    throw new Error(msg.error || "Login failed");
  }
  const data = await res.json();
  localStorage.setItem("token", data.access_token);
  localStorage.setItem("role", data.user.role);
  window.dispatchEvent(new Event("auth-changed"));   // <— notifica a la UI
  return data;
}

export async function me() {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("No token");
  const res = await fetch(`${API}/api/auth/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error("Unauthorized");
  return res.json();
}

export function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  window.dispatchEvent(new Event("auth-changed"));   // <— notifica a la UI
}
