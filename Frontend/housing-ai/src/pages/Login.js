import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AiOutlineEye, AiOutlineEyeInvisible } from "react-icons/ai";
import houseImg from "../Assets/house.png";
import "../styles/Styles.css";
import { login } from "../services/auth";

/**
 * Intenta extraer vendorId de varias estructuras típicas de respuesta.
 * Ajusta si tu backend usa otra forma.
 */
function extractVendorId(data) {
  // Casos frecuentes:
  // data.vendor.id          -> { vendor: { id: 3, ... } }
  // data.user.vendorId      -> { user: { vendorId: 3, ... } }
  // data.vendorId           -> { vendorId: 3 }
  // data.user.vendor.id     -> { user: { vendor: { id: 3 } } }
  // data.profile.vendor_id  -> { profile: { vendor_id: 3 } }
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
 * Extrae role de la respuesta (ajusta las rutas según tu backend).
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
 * Extrae token si tu backend lo regresa (Bearer/JWT).
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
      // Llama a tu servicio de autenticación
      const data = await login(formData.email, formData.password);
      console.log("Login OK:", data);

      // 1) Token (si lo tienes)
      const token = extractToken(data);
      if (token) {
        localStorage.setItem("token", token);
      }

      // 2) Guardar user completo (si te sirve después)
      //    Evita guardar datos sensibles.
      localStorage.setItem("user", JSON.stringify(data?.user ?? data));

      // 3) Role (para routing)
      const role = extractRole(data);
      if (role) {
        localStorage.setItem("role", role);
      }

      // 4) VendorId (lo que necesitas para /vendors/{id}/houses)
      const vendorId = extractVendorId(data);
      if (vendorId !== null && vendorId !== undefined) {
        localStorage.setItem("vendorId", String(vendorId));
      }

      // 5) Redirige según role (o como prefieras)
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
      <div className="auth-info">
        <h1>
          Bienvenido a <span>HouseLink</span>
        </h1>
        <p>Conéctate con miles de compradores y vendedores.</p>
        <img src={houseImg} alt="House" />
      </div>

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
