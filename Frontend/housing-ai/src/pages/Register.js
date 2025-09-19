// src/pages/Register.js
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AiOutlineEye, AiOutlineEyeInvisible } from "react-icons/ai";
import animatedLogo from "../Assets/animatedlogo.mov";
import "../styles/Styles.css";

const API = process.env.REACT_APP_API || "http://localhost:5001";

export default function Register() {
  const nav = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: ""
  });

  // NUEVO: rol seleccionado (buyer = client por defecto)
  const [role, setRole] = useState("client"); // "client" | "vendor"

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
      // Endpoint según el rol elegido
      // Buyer -> client, Vendor -> vendor
      const endpoint =
        role === "vendor" ? "/api/vendors" : "/api/clients";

      const res = await fetch(`${API}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: formData.name.trim(),
          email: formData.email.trim(),
          password: formData.password,
          // En muchos backends el endpoint ya fija el rol,
          // pero mandar el rol no estorba si lo ignoran:
          role
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

        {/* NUEVO: selector de rol tipo switch/segmentado */}
        <div className="role-toggle" role="tablist" aria-label="Tipo de usuario">
          <button
            type="button"
            role="tab"
            aria-selected={role === "client"}
            className={role === "client" ? "active" : ""}
            onClick={() => setRole("client")}
          >
            Buyer
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={role === "vendor"}
            className={role === "vendor" ? "active" : ""}
            onClick={() => setRole("vendor")}
          >
            Vendor
          </button>
        </div>

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

          {/* feedback */}
          {err && <p style={{ color: "#b91c1c", marginTop: 6 }}>{err}</p>}
          {ok &&  <p style={{ color: "#065f46", marginTop: 6 }}>{ok}</p>}

          <button type="submit" disabled={loading}>
            {loading ? "Creando..." : `Registrarse como ${role === "vendor" ? "Vendor" : "Buyer"}`}
          </button>
        </form>

        <p>¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link></p>
      </div>
    </div>
  );
}
