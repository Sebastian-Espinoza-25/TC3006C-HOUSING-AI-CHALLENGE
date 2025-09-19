import "../styles/Styles.css";
import "../styles/howItWorks.css";
import { Link } from "react-router-dom";

export default function HowItWorks() {
  return (
    <section className="hiw">
      {/* decor */}
      <div className="hiw-bg hiw-bg--one" aria-hidden="true" />
      <div className="hiw-bg hiw-bg--two" aria-hidden="true" />

      <div className="hiw-container">
        <header className="hiw-hero">
          <h1 className="hiw-title">
            How does <span>House&nbsp;Link</span> work?
          </h1>
          <p className="hiw-sub">
            Publish or search properties, let AI assist you, and connect with the
          </p>

          <div className="hiw-actions">
            <Link to="/register" className="hiw-cta">Get Started</Link>
            <Link to="/login" className="hiw-cta hiw-cta--ghost">I already have an account</Link>
          </div>
        </header>

        <div className="hiw-steps">
          <article className="hiw-step">
            <div className="hiw-step__badge">1</div>
            <div className="hiw-step__icon" role="img" aria-label="Sign up">📝</div>
            <h3 className="hiw-step__title">Sign Up</h3>
            <p className="hiw-step__text">
              Create your account as a client or vendor and access your personalized dashboard.
            </p>
          </article>

          <article className="hiw-step">
            <div className="hiw-step__badge">2</div>
            <div className="hiw-step__icon" role="img" aria-label="Publish or Search">🏠</div>
            <h3 className="hiw-step__title">Publish or Search Houses</h3>
            <p className="hiw-step__text">
              Sellers publish properties with photos and details. Buyers search and filter by preferences.
            </p>
          </article>

          <article className="hiw-step">
            <div className="hiw-step__badge">3</div>
            <div className="hiw-step__icon" role="img" aria-label="AI">🤖</div>
            <h3 className="hiw-step__title">Get Smart Recommendations</h3>
            <p className="hiw-step__text">
              Our AI suggests prices and ideal houses using data and your personalized preferences.
            </p>
          </article>

          <article className="hiw-step">
            <div className="hiw-step__badge">4</div>
            <div className="hiw-step__icon" role="img" aria-label="Connect">💬</div>
            <h3 className="hiw-step__title">Connect & Negotiate</h3>
            <p className="hiw-step__text">
              Contact sellers or buyers, schedule visits, and negotiate directly from the platform.
            </p>
          </article>
        </div>

        <footer className="hiw-foot">
          <Link to="/register" className="hiw-cta hiw-cta--lg">Start free today</Link>
        </footer>
      </div>
    </section>
  );
}
