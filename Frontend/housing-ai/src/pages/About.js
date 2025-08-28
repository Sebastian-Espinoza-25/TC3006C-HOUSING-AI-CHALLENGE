import { useEffect, useRef, useState } from "react";
import Santiago from "../Assets/TeamFotos/Santiago.png";
import Jesus from "../Assets/TeamFotos/Jesus.png";
import Jose from "../Assets/TeamFotos/Jose.png";
import Luis from "../Assets/TeamFotos/Luis.png";
import Sebas from "../Assets/TeamFotos/Sebas.png";
import Ulises from "../Assets/TeamFotos/Ulises.png";


const TEAM = [
  { name: "Santiago Villazón", role: "Product Lead",     photo: Santiago },
  { name: "Jesús Ángel Guzmán Ortega",       role: "ML Engineer",      photo: Jesus },
  { name: "José Antonio Moreno Tahuilán",       role: "Frontend Engineer",photo: Jose },
  { name: "Luis Ubaldo Balderas Sánchez",        role: "Data Scientist",   photo: Luis },
  { name: "Sebastián Espinoza Farías",        role: "Data Scientist",   photo: Sebas },
  { name: "Ulises Jaramillo Portilla",        role: "Data Scientist",   photo: Ulises },
];

export default function About() {
  const [index, setIndex] = useState(0);
  const timer = useRef(null);

  const next = () => setIndex((i) => (i + 1) % TEAM.length);
  const prev = () => setIndex((i) => (i - 1 + TEAM.length) % TEAM.length);

  useEffect(() => {
    timer.current && clearTimeout(timer.current);
    timer.current = setTimeout(next, 5000); // autoplay
    return () => clearTimeout(timer.current);
  }, [index]);

  const cls = (i) => {
    if (i === index) return "active";
    if (i === (index - 1 + TEAM.length) % TEAM.length) return "prev";
    if (i === (index + 1) % TEAM.length) return "next";
    return "hidden";
  };

  return (
    <section
      className="aboutfx"
      onMouseEnter={() => timer.current && clearTimeout(timer.current)}
      onMouseLeave={() => (timer.current = setTimeout(next, 5000))}
    >
    <h1 className="aboutfx__title">Our Team</h1>
      <div className="aboutfx__wrap">
        <button className="arrow left" onClick={prev} aria-label="Previous">
          <svg viewBox="0 0 24 24" width="22" height="22"><path d="M15 18l-6-6 6-6" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
        </button>

        {TEAM.map((m, i) => (
          <div key={m.name} className={`slide ${cls(i)}`} aria-hidden={i !== index}>
            <article className="cardfx">
              <img className="cardfx__photo" src={m.photo} alt={`${m.name} headshot`} />
              <div className="cardfx__info">
                <h2>{m.name}</h2>
                <p>{m.role}</p>
              </div>
            </article>
          </div>
        ))}

        <button className="arrow right" onClick={next} aria-label="Next">
          <svg viewBox="0 0 24 24" width="22" height="22"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
        </button>
      </div>

      <div className="dotsfx">
        {TEAM.map((_, i) => (
          <button
            key={i}
            className={`dot ${i === index ? "active" : ""}`}
            onClick={() => setIndex(i)}
            aria-label={`Go to slide ${i + 1}`}
          />
        ))}
      </div>

    {/* === Text below carousel === */}
      <div className="aboutfx__text">
        <h2>About House Link</h2>
        <p>
          HouseLink is a platform created to <strong>connect home sellers with buyers</strong> quickly and transparently.
          We use <strong>Artificial Intelligence models</strong> to estimate a property's <strong>true value</strong> and suggest options based on <strong>buyer 
          preferences</strong> (location, budget, square footage, and amenities), helping them make better, data-driven decisions.
        </p>

        <h3>Academic Project</h3>
        <p>
          This project was born from the <em>Advanced Artificial Intelligence</em> program at <strong>Tecnológico de Monterrey</strong>.
          Our approach includes <strong>price prediction</strong>, model <strong>explainability</strong>, and best practices in <strong>data privacy and security</strong>.
        </p>

        <h3>Team — Tec de Monterrey</h3>
        <ul className="aboutfx__teamlist">
          {TEAM.map((m) => (
            <li key={m.name}><strong>{m.name}</strong> — {m.role}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}
