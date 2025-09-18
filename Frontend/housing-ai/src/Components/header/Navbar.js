import { Link, Outlet, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import logo from "../../Assets/LogoHouseLink.png";
import { logout } from "../../services/auth"; // 👈 importa logout

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [isAuthed, setIsAuthed] = useState(!!localStorage.getItem("token"));
  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 0);
    window.addEventListener("scroll", handleScroll);

    // 👇 escucha cuando cambie el estado de auth
    const onAuthChange = () => setIsAuthed(!!localStorage.getItem("token"));
    window.addEventListener("auth-changed", onAuthChange);
    window.addEventListener("storage", onAuthChange);

    return () => {
      window.removeEventListener("scroll", handleScroll);
      window.removeEventListener("auth-changed", onAuthChange);
      window.removeEventListener("storage", onAuthChange);
    };
  }, []);

  const handleLogout = () => {
    logout();
    setIsAuthed(false);
    navigate("/login");
  };

  return (
    <>
      <nav className={`nav ${scrolled ? "scrolled" : ""}`}>
        <Link to="/" className="site-title">
          <img
            src={logo}
            alt="Logo"
            style={{ width: "80px", height: "80px", marginRight: "8px" }}
          />
          House Link
        </Link>

        <ul>
          <li>
            <Link to="/search">Search House</Link>
          </li>
          <li>
            <Link to="/sell">Sell</Link>
          </li>
          <li>
            <Link to="/how-it-works">How It Works</Link>
          </li>
          <li>
            {!isAuthed ? (
              <Link to="/login">Login</Link>
            ) : (
              <button
                onClick={handleLogout}
                style={{
                  background: "transparent",
                  border: "none",
                  color: "inherit",
                  cursor: "pointer",
                  font: "inherit"
                }}
              >
                Logout
              </button>
            )}
          </li>
        </ul>
      </nav>

      <Outlet />
    </>
  );
}
