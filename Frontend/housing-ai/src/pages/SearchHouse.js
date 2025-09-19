import { useEffect, useMemo, useState } from "react";
import "../styles/seller/recommendations.css";

// ----- helpers -----
const formatPrice = (v) =>
  new Intl.NumberFormat("es-MX", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Number(v || 0));

const getAuthToken = () => {
  try {
    return localStorage.getItem("token") || localStorage.getItem("authToken") || null;
  } catch {
    return null;
  }
};

const getClientIdFromLocalStorage = () => {
  try {
    // intentos directos
    const direct = localStorage.getItem("clientId") || localStorage.getItem("client_id");
    if (direct) return Number(direct);

    // estructuras comunes
    const raw =
      localStorage.getItem("client") ||
      localStorage.getItem("user") ||
      localStorage.getItem("auth") ||
      localStorage.getItem("profile");
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    return (
      parsed?.clientId ??
      parsed?.client_id ??
      parsed?.user?.clientId ??
      parsed?.user?.client_id ??
      parsed?.client?.clientId ??
      parsed?.client?.client_id ??
      null
    );
  } catch {
    return null;
  }
};

// ----- UI atoms -----
function DetailRow({ label, value }) {
  if (value === null || value === undefined || value === "") return null;
  return (
    <div className="rec-detail">
      <span className="rec-detail-label">{label}</span>
      <span className="rec-detail-value">{value}</span>
    </div>
  );
}

function HouseCard({ match, expanded, onToggle }) {
  const { house, vendor } = match || {};
  const title = house?.title || "Sin título";
  const price = house?.sale_price;

  const tags = useMemo(() => {
    const out = [];
    if (house?.neighborhood) out.push(house.neighborhood);
    if (house?.house_style) out.push(house.house_style);
    if (house?.bedroom_abv_gr != null) out.push(`${Number(house.bedroom_abv_gr)} hab.`);
    if (house?.full_bath != null) out.push(`${Number(house.full_bath)} baños`);
    if (house?.garage_cars != null) out.push(`${Number(house.garage_cars)} autos`);
    return out.slice(0, 4);
  }, [house]);

  return (
    <article
      className={`rec-card ${expanded ? "is-open" : ""}`}
      onClick={onToggle}
      role="button"
      tabIndex={0}
      aria-expanded={expanded}
      onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && onToggle()}
    >
      <div className="rec-head">
        <div className="rec-img" aria-hidden="true" />
        <div className="rec-main">
          <h4 className="rec-title">{title}</h4>
          <div className="rec-tags">
            {tags.map((t) => (
              <span className="rec-tag" key={t}>{t}</span>
            ))}
          </div>
        </div>
        <div className="rec-price">{price != null ? `$ ${formatPrice(price)}` : "S/D"}</div>
      </div>

      <div className="rec-divider" />

      <div className="rec-more">
        <span className="rec-more-text">{expanded ? "Ocultar detalles" : "Ver detalles"}</span>
        <span className={`rec-caret ${expanded ? "up" : ""}`} aria-hidden>▾</span>
      </div>

      {expanded && (
        <div className="rec-details">
          <DetailRow label="Vecindario" value={house?.neighborhood} />
          <DetailRow label="Estilo" value={house?.house_style} />
          <DetailRow label="Construida" value={house?.year_built ? Number(house.year_built) : null} />
          <DetailRow label="Superficie habitable (GrLivArea)" value={house?.gr_liv_area ? `${Number(house.gr_liv_area)} ft²` : null} />
          <DetailRow label="1er piso" value={house?.first_flr_sf != null ? `${Number(house.first_flr_sf)} ft²` : null} />
          <DetailRow label="2do piso" value={house?.second_flr_sf != null ? `${Number(house.second_flr_sf)} ft²` : null} />
          <DetailRow label="Dormitorios" value={house?.bedroom_abv_gr != null ? Number(house.bedroom_abv_gr) : null} />
          <DetailRow label="Baños" value={
            house?.total_bath != null
              ? Number(house.total_bath)
              : house?.full_bath != null || house?.half_bath != null
              ? `${house?.full_bath ?? 0} / ${house?.half_bath ?? 0} (completos / medios)`
              : null
          } />
          <DetailRow label="Chimeneas" value={house?.fireplaces != null ? Number(house.fireplaces) : null} />
          <DetailRow label="Cochera (autos)" value={house?.garage_cars != null ? Number(house.garage_cars) : null} />
          <DetailRow label="Cochera (área)" value={house?.garage_area != null ? `${Number(house.garage_area)} ft²` : null} />
          <DetailRow label="Porche abierto" value={house?.open_porch_sf != null ? `${Number(house.open_porch_sf)} ft²` : null} />
          <DetailRow label="Piscina (área)" value={house?.pool_area != null ? Number(house.pool_area) : null} />
          <DetailRow label="A/C central" value={house?.central_air != null ? (String(house.central_air) === "Y" ? "Sí" : "No") : null} />
          <DetailRow label="Condición de venta" value={house?.sale_condition} />
          <DetailRow label="Tipo de venta" value={house?.sale_type} />
          <DetailRow label="Descripción" value={house?.description} />

          <div className="rec-subtitle">Contacto</div>
          <DetailRow label="Teléfono" value={house?.contact_phone || vendor?.contact_phone} />
          <DetailRow label="Email" value={house?.contact_email || vendor?.contact_email} />
          <DetailRow label="Inmobiliaria" value={vendor?.username} />
        </div>
      )}
    </article>
  );
}

// ===================== Main =====================
export default function Recommendations() {
  const [clientId, setClientId] = useState(null);
  const [data, setData] = useState({ client: null, matches: [], preferences_applied: null });
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");
  const [openId, setOpenId] = useState(null);

  // Lee clientId del localStorage una sola vez
  useEffect(() => {
    setClientId(getClientIdFromLocalStorage());
  }, []);

  // Fetch cuando ya tenemos clientId
  useEffect(() => {
    const fetchRecs = async () => {
      try {
        setLoading(true);
        setErr("");
        const token = getAuthToken();
        const res = await fetch(`http://127.0.0.1:5001/api/clients/${clientId}/recommendations`, {
          headers: {
            "Content-Type": "application/json",
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
          },
        });
        const json = await res.json();
        if (!res.ok) throw new Error(json?.error || "Error obteniendo recomendaciones");
        setData({
          client: json.client,
          matches: json.matches || [],
          preferences_applied: json.preferences_applied || null,
        });
      } catch (e) {
        console.error(e);
        setErr(e.message || "Error de red");
      } finally {
        setLoading(false);
      }
    };
    if (clientId != null) fetchRecs();
  }, [clientId]);

  return (
    <section className="rec-wrap">
      <div className="rec-header">
        <h2 className="pref-title rec-title-page">Recomendaciones</h2>
        <p className="pref-subtitle rec-subtitle-page">
          {clientId == null
            ? "No se encontró clientId en el navegador."
            : `Casas que hacen match con las preferencias del cliente ${
                data?.client?.username ? `“${data.client.username}”` : `#${clientId}`
              }`}
        </p>
      </div>

      {clientId == null && <div className="global-error">Inicia sesión como cliente o guarda el clientId en localStorage.</div>}

      {clientId != null && (
        <>
          {loading && <div className="rec-state">Cargando recomendaciones…</div>}
          {err && !loading && <div className="global-error">{err}</div>}

          {!loading && !err && (
            <div className="rec-rail">
              {data.matches.length === 0 && <div className="rec-empty">No hay coincidencias por ahora.</div>}

              {data.matches.map(({ house, vendor }) => (
                <HouseCard
                  key={house?.house_id || `${vendor?.vendor_id}-${Math.random()}`}
                  match={{ house, vendor }}
                  expanded={openId === house?.house_id}
                  onToggle={() => setOpenId((cur) => (cur === house?.house_id ? null : house?.house_id))}
                />
              ))}
            </div>
          )}
        </>
      )}
    </section>
  );
}
