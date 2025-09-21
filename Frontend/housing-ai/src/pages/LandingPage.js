// @author Santiago Villazón Ponce de León | A01746396

// src/pages/LandingPage.js
import { useEffect } from "react";
import { Link } from "react-router-dom";

export default function LandingPage() {
  useEffect(() => {
    // Reveal-on-scroll for soft entrance animations
    const els = document.querySelectorAll(".reveal");
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add("reveal--visible")),
      { threshold: 0.12 }
    );
    els.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, []);

  return (
    <div className="landing">
      {/* HERO: background image */}
      <section className="hero">
        <div className="hero-content">
          <h1>Want to rent or sell your property fast?</h1>
          <p>Reach thousands of people in seconds with House Link.</p>
          <Link to="/login" className="cta">Sign Up</Link>
        </div>
      </section>

      {/* VALUE PROPS + bottom curve */}
      <section className="section reveal sep sep--bottom-blue">
        <div className="container feature-grid">
          <div className="feature-card">
            <div className="feature-icon">⚡️</div>
            <h3>Instant reach</h3>
            <p>Publish and get visibility in minutes with a clean, modern profile.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>AI price insights</h3>
            <p>Data-driven price suggestions to attract more qualified buyers.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Smart matching</h3>
            <p>We match listings with buyers based on preferences and budget.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🛡️</div>
            <h3>Trust & privacy</h3>
            <p>We respect data privacy and follow best security practices.</p>
          </div>
        </div>
      </section>

      <section className="section alt reveal sep sep--top-blue sep--bottom-blue">
        <div className="container">
          <h2 className="section-title">How it works</h2>
          <ol className="stepper">
            <li>
              <span className="step-num">1</span>
              <div>
                <h4>Create your profile</h4>
                <p>Add property details or buyer preferences in a few steps.</p>
              </div>
            </li>
            <li>
              <span className="step-num">2</span>
              <div>
                <h4>Get an AI price estimate</h4>
                <p>Preview a fair price range based on similar properties.</p>
              </div>
            </li>
            <li>
              <span className="step-num">3</span>
              <div>
                <h4>Connect instantly</h4>
                <p>Receive matches and start chatting to schedule visits.</p>
              </div>
            </li>
          </ol>
        </div>
      </section>

      {/* AI PRICE ESTIMATOR: top & bottom curves */}
      <section className="section reveal sep sep--top-blue sep--bottom-blue">
        <div className="container estimator">
          <div className="estimator-copy">
            <h2 className="section-title">Estimate your price with AI</h2>
            <p className="muted">Enter a few details and preview an estimated price range.</p>
          </div>

          <form
            className="estimator-form"
            onSubmit={(e) => {
              e.preventDefault();
              alert("Demo: price estimate coming soon 🚧");
            }}
          >
            {/* Minimal inputs; */}
            <input type="text" placeholder="Neighborhood / ZIP" required />
            <input type="number" placeholder="Bedrooms" min="0" required />
            <input type="number" placeholder="Bathrooms" min="0" required />
            <input type="number" placeholder="Area (m²)" min="10" required />
            <button type="submit" className="cta secondary">Estimate</button>
          </form>
        </div>
      </section>

      {/* TESTIMONIALS: alt background + top curve */}
      <section className="section alt reveal sep sep--top-blue">
        <div className="container testimonials">
          <article className="quote">
            <p>“We sold 15% above our initial expectation thanks to the AI insights.”</p>
            <span>— Andrea R.</span>
          </article>
          <article className="quote">
            <p>“Filtering by preferences saved me days of back-and-forth.”</p>
            <span>— Daniel M.</span>
          </article>
          <article className="quote">
            <p>“Super clean UX and the price range felt realistic.”</p>
            <span>— Sofía T.</span>
          </article>
        </div>
      </section>

      {/* FAQ: top & bottom curves */}
      <section className="section reveal sep sep--top-blue sep--bottom-blue">
        <div className="container faq">
          <h2 className="section-title">FAQ</h2>

          <details>
            <summary>How do you estimate prices?</summary>
            <p>
              We use machine learning models trained on historical listings and transactions,
              plus key features like location, area, and property attributes.
            </p>
          </details>

          <details>
            <summary>Is my data safe?</summary>
            <p>
              Yes. We only use the data needed for recommendations and follow privacy best practices.
            </p>
          </details>

          <details>
            <summary>Can I list multiple properties?</summary>
            <p>Absolutely. You can manage multiple listings from your dashboard.</p>
          </details>
        </div>
      </section>

      {/* FINAL CTA BAND: subtle reveal */}
      <section className="cta-band reveal">
        <div className="container cta-band__inner">
          <h3>Ready to find the right match?</h3>
          <div className="cta-actions">
            <Link to="/sell" className="cta">List a property</Link>
            <Link to="/search" className="cta ghost">Search homes</Link>
          </div>
        </div>
      </section>
    </div>
  );
}
