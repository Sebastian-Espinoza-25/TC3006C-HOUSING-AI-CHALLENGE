import { Link } from "react-router-dom";
import { useEffect, useRef, useState } from "react";

export default function Footer() {
  const ref = useRef(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    // Muestra el footer cuando al menos 10% entra a viewport
    const io = new IntersectionObserver(
      ([entry]) => setVisible(entry.isIntersecting),
      { root: null, threshold: 0.1 }
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <footer ref={ref} className={`footer ${visible ? "is-visible" : ""}`}>
      <div className="footer__inner">
        <span className="footer__brand">© {new Date().getFullYear()} HouseLink</span>
        <ul className="footer__nav">
          <li><Link to="/about">About</Link></li>
        </ul>
      </div>
    </footer>
  );
}
