/**
 * @author Ulises Jaramillo Portilla | A01798380 | Ulises-JPx
 *
 * This file defines the Sell page component for the Housing AI Challenge frontend application.
 * The Sell page serves as the main dashboard for property sellers, providing them with access
 * to key actions such as publishing new property listings, viewing their existing listings,
 * and managing messages from interested clients.
 */

import { Link } from "react-router-dom";
import "../styles/seller.css";

export default function Sell() {
  return (
    <div className="sell-container">
      {/* Animated welcome text */}
      <div className="title-anim">
        <div>Welcome,</div>
        <div>
          <span> Seller!</span>
        </div>
      </div>

      {/* Subtitle */}
      <p className="subtitle">
        Manage your properties, publish listings, and stay in touch
        with interested clients.
      </p>

      {/* Button box */}
      <section className="button-bar">
        <Link to="/sell/publish" className="glass-btn">
          Publish Listing
        </Link>
        <Link to="/sell/listings" className="glass-btn">
          My Listings
        </Link>
        <Link to="/sell/messages" className="glass-btn">
          Messages
        </Link>
      </section>
    </div>
  );
}