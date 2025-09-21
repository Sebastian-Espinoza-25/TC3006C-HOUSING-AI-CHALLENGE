// @author Santiago Villazón Ponce de León | A01746396

// src/Components/header/Navbar.jsx
import { NavLink, Link, Outlet, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import logo from "../../Assets/LogoHouseLink.png";
import { getRole, isAuthed as checkAuthed, logout } from "../../services/session";

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [authed, setAuthed] = useState(checkAuthed());
  const [role, setRole] = useState(getRole()); // "client" | "vendor" | null
  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 0);
    window.addEventListener("scroll", handleScroll);

    // sincroniza con cambios de sesión desde login/logout o en otra pestaña
    const syncAuth = () => {
      setAuthed(checkAuthed());
      setRole(getRole());
    };
    window.addEventListener("auth-changed", syncAuth);
    window.addEventListener("storage", syncAuth);

    // primera sincronización
    syncAuth();

    return () => {
      window.removeEventListener("scroll", handleScroll);
      window.removeEventListener("auth-changed", syncAuth);
      window.removeEventListener("storage", syncAuth);
    };
  }, []);

  const handleLogout = () => {
    logout();
    setAuthed(false);
    setRole(null);
    navigate("/login");
  };

  const navLinkClass = ({ isActive }) => (isActive ? "active" : undefined);

  return (
    <>
      <nav className={`nav ${scrolled ? "scrolled" : ""}`}>
        <Link to="/" className="site-title" style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <img src={logo} alt="Logo" style={{ width: 48, height: 48 }} />
          House Link
        </Link>

        <ul>
          {!authed && (
            <>
              <li><NavLink to="/search" className={navLinkClass}>Search House</NavLink></li>
              <li><NavLink to="/how-it-works" className={navLinkClass}>How It Works</NavLink></li>
              <li><NavLink to="/login" className={navLinkClass}>Login</NavLink></li>
              <li><NavLink to="/register" className={navLinkClass}>Register</NavLink></li>
            </>
          )}

          {authed && role === "client" && (
            <>
              <li><NavLink to="/search" className={navLinkClass}>Search House</NavLink></li>
              <li><NavLink to="/preferences" className={navLinkClass}>Preferences</NavLink></li>
              <li>
                <button onClick={handleLogout} className="nav-logout">Logout</button>
              </li>
            </>
          )}

          {authed && role === "vendor" && (
            <>
              <li><NavLink to="/sell" className={navLinkClass}>Sell</NavLink></li>
              <li><NavLink to="/publish" className={navLinkClass}>Publish</NavLink></li>
              <li><NavLink to="/listings" className={navLinkClass}>Listings</NavLink></li>
              <li>
                <button onClick={handleLogout} className="nav-logout">Logout</button>
              </li>
            </>
          )}
        </ul>
      </nav>

      <Outlet />
    </>
  );
}
