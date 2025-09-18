// src/pages/Register.js
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AiOutlineEye, AiOutlineEyeInvisible } from "react-icons/ai";
import animatedLogo from "../Assets/animatedlogo.mov";
import "../styles/Styles.css";

const API = process.env.REACT_APP_API || "http://localhost:5000";

export default function Register() {
  const nav = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: ""
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");
  const [ok, setOk] = useState("");

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErr(""); setOk("");

    if (formData.password !== formData.confirmPassword) {
      setErr("Las contraseñas no coinciden");
      return;
    }

    setLoading(true);
    try {
      // Por ahora registramos como CLIENTE (endpoint /api/clients del backend)
      // Si quieres registrar vendedores, cambia a /api/vendors
      const res = await fetch(`${API}/api/clients`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: formData.name.trim(),
          email: formData.email.trim(),
          password: formData.password
        })
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || "No se pudo registrar");
      }

      setOk("Cuenta creada. Ahora inicia sesión.");
      setTimeout(() => nav("/login"), 900);
    } catch (e2) {
      setErr(e2.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-layout single register-page">
      {/* 🎥 Fondo animado a pantalla completa */}
      <video className="bg-video bg-video--full" autoPlay loop muted playsInline>
        <source src={animatedLogo} type="video/mp4" />
        <source src={animatedLogo} type="video/quicktime" />
        Tu navegador no soporta video.
      </video>

      {/* Formulario centrado */}
      <div className="form-container">
        <h2>Crear cuenta</h2>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="name"
            placeholder="Nombre completo"
            value={formData.name}
            onChange={handleChange}
            required
          />

          <input
            type="email"
            name="email"
            placeholder="Correo electrónico"
            value={formData.email}
            onChange={handleChange}
            required
          />

          <div className="password-wrapper">
            <input
              type={showPassword ? "text" : "password"}
              name="password"
              placeholder="Contraseña"
              value={formData.password}
              onChange={handleChange}
              required
            />
            <button
              type="button"
              className="eye-btn"
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
            >
              {showPassword ? <AiOutlineEyeInvisible size={20} /> : <AiOutlineEye size={20} />}
            </button>
          </div>

          <div className="password-wrapper">
            <input
              type={showConfirm ? "text" : "password"}
              name="confirmPassword"
              placeholder="Confirmar contraseña"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />
            <button
              type="button"
              className="eye-btn"
              onClick={() => setShowConfirm(!showConfirm)}
              aria-label={showConfirm ? "Ocultar confirmación" : "Mostrar confirmación"}
            >
              {showConfirm ? <AiOutlineEyeInvisible size={20} /> : <AiOutlineEye size={20} />}
            </button>
          </div>

          {err && <p style={{ color: "#b91c1c", marginTop: 6 }}>{err}</p>}
          {ok &&  <p style={{ color: "#065f46", marginTop: 6 }}>{ok}</p>}

          <button type="submit" disabled={loading}>
            {loading ? "Creando..." : "Registrarse"}
          </button>
        </form>

        <p>¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link></p>
      </div>
    </div>
  );
}
