import { Link, Outlet } from "react-router-dom";
import { useEffect, useState } from "react";
import logo from "../../Assets/LogoHouseLink.png";

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 0);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

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
        </ul>
      </nav>

      <Outlet />
    </>
  );
}
