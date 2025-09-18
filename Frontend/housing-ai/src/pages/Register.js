import { useState } from "react";
import { Link } from "react-router-dom";
import { AiOutlineEye, AiOutlineEyeInvisible } from "react-icons/ai";
import animatedLogo from "../Assets/animatedlogo.mov"; // tu video en src/assets
import "../styles/Styles.css";

export default function Register() {
  const [formData, setFormData] = useState({
    name: "", email: "", password: "", confirmPassword: ""
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });
  const handleSubmit = (e) => { e.preventDefault(); if (formData.password !== formData.confirmPassword) return alert("Las contraseñas no coinciden!"); console.log("Register:", formData); };

  return (
    <div className="auth-layout single register-page">
      {/* 🎥 Fondo de pantalla completo */}
      <video className="bg-video bg-video--full" autoPlay loop muted playsInline>
        <source src={animatedLogo} type="video/mp4" />
        Tu navegador no soporta video.
      </video>

      {/* Formulario centrado */}
      <div className="form-container">
        <h2>Crear cuenta</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" name="name" placeholder="Nombre completo" value={formData.name} onChange={handleChange} required />
          <input type="email" name="email" placeholder="Correo electrónico" value={formData.email} onChange={handleChange} required />

          <div className="password-wrapper">
            <input type={showPassword ? "text" : "password"} name="password" placeholder="Contraseña" value={formData.password} onChange={handleChange} required />
            <button type="button" className="eye-btn" onClick={() => setShowPassword(!showPassword)}>
              {showPassword ? <AiOutlineEyeInvisible size={20}/> : <AiOutlineEye size={20}/>}
            </button>
          </div>

          <div className="password-wrapper">
            <input type={showConfirm ? "text" : "password"} name="confirmPassword" placeholder="Confirmar contraseña" value={formData.confirmPassword} onChange={handleChange} required />
            <button type="button" className="eye-btn" onClick={() => setShowConfirm(!showConfirm)}>
              {showConfirm ? <AiOutlineEyeInvisible size={20}/> : <AiOutlineEye size={20}/>}
            </button>
          </div>

          <button type="submit">Registrarse</button>
        </form>
        <p>¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link></p>
      </div>
    </div>
  );
}