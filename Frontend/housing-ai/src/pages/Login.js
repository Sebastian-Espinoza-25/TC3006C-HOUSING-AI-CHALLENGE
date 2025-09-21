// @author Santiago Villazón Ponce de León | A01746396

import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AiOutlineEye, AiOutlineEyeInvisible } from "react-icons/ai";
import houseImg from "../Assets/house.png";
import "../styles/Styles.css";
import { login } from "../services/auth";


function extractVendorId(data) {
  return (
    data?.vendor?.id ??
    data?.user?.vendorId ??
    data?.vendorId ??
    data?.user?.vendor?.id ??
    data?.profile?.vendor_id ??
    null
  );
}

/**
 * Extrae role de la respuesta.
 */
function extractRole(data) {
  return (
    data?.role ??
    data?.user?.role ??
    data?.profile?.role ??
    null
  );
}

/**
 * Extrae token
 */
function extractToken(data) {
  return (
    data?.token ??
    data?.access_token ??
    data?.accessToken ??
    null
  );
}

export default function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await login(formData.email, formData.password);
      console.log("Login OK:", data);

      const token = extractToken(data);
      if (token) {
        localStorage.setItem("token", token);
      }

      localStorage.setItem("user", JSON.stringify(data?.user ?? data));

      const role = extractRole(data);
      if (role) {
        localStorage.setItem("role", role);
      }

      const vendorId = extractVendorId(data);
      if (vendorId !== null && vendorId !== undefined) {
        localStorage.setItem("vendorId", String(vendorId));
      }

      if (role === "vendor") navigate("/sell");
      else navigate("/search");
    } catch (err) {
      alert("Login fallido: " + (err?.message || "Error desconocido"));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-layout">
      {/* Panel azul con contenido dividido en bloques */}
      <div className="auth-info">
        <div className="auth-texts">
          <h1>
            Bienvenido a <span>HouseLink</span>
          </h1>
          <p>Conéctate con miles de compradores y vendedores.</p>
        </div>

        <div className="auth-image">
          <img src={houseImg} alt="House" />
        </div>
      </div>

      {/* Formulario */}
      <div className="auth-form">
        <div className="form-container">
          <h2>Login</h2>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              name="email"
              placeholder="Email o usuario"
              value={formData.email}
              onChange={handleChange}
              required
            />
            <div className="password-wrapper">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                required
              />
              <button
                type="button"
                className="eye-btn"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <AiOutlineEyeInvisible size={20} />
                ) : (
                  <AiOutlineEye size={20} />
                )}
              </button>
            </div>
            <button type="submit" disabled={loading}>
              {loading ? "Entrando..." : "Login"}
            </button>
          </form>
          <p>
            ¿No tienes cuenta? <Link to="/register">Regístrate</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
