// @author Santiago Villazón Ponce de León | A01746396

import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer__inner">
        <span className="footer__brand">© {new Date().getFullYear()} HouseLink</span>
        <ul className="footer__nav">
          <li><Link to="/about">About</Link></li>
        </ul>
      </div>
    </footer>
  );
}


