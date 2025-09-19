import { useEffect, useMemo, useState } from "react";
import "../../styles/seller/listings.css";

/* ================= Helpers ================= */
const API_BASE = "http://127.0.0.1:5001";

const formatPrice = (v) =>
  new Intl.NumberFormat("es-MX", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(v || 0));

const getAuthToken = () => {
  try {
    return (
      localStorage.getItem("token") ||
      localStorage.getItem("authToken") ||
      null
    );
  } catch {
    return null;
  }
};

const getVendorIdFromLocalStorage = () => {
  try {
    const direct =
      localStorage.getItem("vendorId") || localStorage.getItem("vendor_id");
    if (direct) return Number(direct);

    const raw =
      localStorage.getItem("vendor") ||
      localStorage.getItem("user") ||
      localStorage.getItem("auth") ||
      localStorage.getItem("profile");
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    return (
      parsed?.vendorId ??
      parsed?.vendor_id ??
      parsed?.user?.vendorId ??
      parsed?.user?.vendor_id ??
      parsed?.vendor?.vendorId ??
      parsed?.vendor?.vendor_id ??
      null
    );
  } catch {
    return null;
  }
};

const formatFeature = (v, unit = "") =>
  v != null ? `${v}${unit}` : "N/A";

/* ========== Cargar fotos (Vite o CRA) ========== */
const loadHousePhotos = () => {
  try {
    if (
      typeof import.meta !== "undefined" &&
      import.meta &&
      typeof import.meta.glob === "function"
    ) {
      const mods = import.meta.glob(
        "../Assets/HouseFotos/*.{png,jpg,jpeg,webp,avif,gif}",
        { eager: true }
      );
      return Object.values(mods)
        .map((m) => m?.default || m)
        .filter(Boolean);
    }
  } catch {}

  try {
    const ctx = require.context(
      "../../Assets/HouseFotos",
      false,
      /\.(png|jpe?g|webp|avif|gif)$/i
    );
    return ctx
      .keys()
      .map((k) => ctx(k)?.default || ctx(k))
      .filter(Boolean);
  } catch (e) {
    console.error("No se pudo cargar imágenes de Assets/HouseFotos:", e);
    return [];
  }
};

const HOUSE_PHOTOS = loadHousePhotos();
const pickPhotoForHouse = (houseId) => {
  if (!HOUSE_PHOTOS.length) return null;
  const idNum = Number(houseId);
  const idx = Number.isFinite(idNum)
    ? idNum % HOUSE_PHOTOS.length
    : Math.floor(Math.random() * HOUSE_PHOTOS.length);
  return HOUSE_PHOTOS[idx];
};

/* ================= UI Atoms ================= */
function DetailRow({ label, value }) {
  if (value === null || value === undefined || value === "") return null;
  return (
    <div className="rec-detail">
      <span className="rec-detail-label">{label}</span>
      <span className="rec-detail-value">{value}</span>
    </div>
  );
}

function HouseCard({ house, expanded, onToggle }) {
  const title = house?.title || "No title";
  const price = house?.sale_price;
  const imgUrl = useMemo(() => pickPhotoForHouse(house?.house_id), [
    house?.house_id,
  ]);

  // Bubble keys: must match JSON keys exactly!
  const bubbleKeys = ["total_bath", "lot_area", "garage_cars"];
  const mainFeatures = bubbleKeys.map((key) => ({
    key,
    label: key.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase()),
    value: house[key],
  }));

  // Exclude these from summary and details
  const excludeKeys = [
    ...bubbleKeys,
    "vendor_id",
    "sale_price",
    "house_id"
  ];

  // Summary: first 5 important non-null fields not in excludeKeys
  const summaryFields = Object.entries(house)
    .filter(([key, value]) =>
      !excludeKeys.includes(key) &&
      value !== null &&
      value !== undefined &&
      value !== ""
    )
    .slice(0, 5);

  const summary = summaryFields
    .map(([key, value]) => `${key.replace(/_/g, " ")}: ${value}`)
    .join(", ");

  // Details: all other non-null fields not in bubbles or summary
  const shownKeys = [...bubbleKeys, ...summaryFields.map(([k]) => k)];
  const detailFields = Object.entries(house)
    .filter(([key, value]) =>
      !shownKeys.includes(key) &&
      value !== null &&
      value !== undefined &&
      value !== ""
    );

  // Contact info (always shown in a separate section)
  const contactKeys = ["contact_email", "contact_phone", "contact_name"];
  const contactFields = contactKeys
    .map((key) => [key, house[key]])
    .filter(([, value]) => value !== null && value !== undefined && value !== "");

  return (
    <article
      className={`rec-card airbnb-card${expanded ? " is-open" : ""}`}
      onClick={onToggle}
      role="button"
      tabIndex={0}
      aria-expanded={expanded}
      onKeyDown={(e) => (e.key === "Enter" || e.key === " ") && onToggle()}
    >
      <div
        className="rec-img-top"
        style={imgUrl ? { backgroundImage: `url(${imgUrl})` } : undefined}
      />
      <div className="rec-main-airbnb">
        <h4 className="rec-title-airbnb">{title}</h4>
        <div className="rec-price-airbnb">
          {price != null ? `$ ${formatPrice(price)}` : "N/A"}
        </div>
        <div className="rec-features-airbnb">
          {mainFeatures.map((f, i) => (
            <span className="rec-feature-bubble" key={i}>
              <span className="rec-feature-value">{formatFeature(f.value)}</span>
              <span className="rec-feature-label">{f.label}</span>
            </span>
          ))}
        </div>
      </div>
      <div className="rec-more-airbnb">
        <span>{expanded ? "Hide details" : "See details"}</span>
        <span className={`rec-caret ${expanded ? "up" : ""}`} aria-hidden>
          ▾
        </span>
      </div>
      {expanded && (
        <div className="rec-details-airbnb">
          <div className="rec-summary">
            <strong>Summary:</strong> {summary || "No summary available"}
          </div>
          {detailFields.length > 0 && (
            <div className="rec-details-section">
              <div className="rec-details-title">Additional features:</div>
              <div className="rec-details-grid">
                {detailFields.map(([key, value]) => (
                  <DetailRow
                    key={key}
                    label={key.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase())}
                    value={value}
                  />
                ))}
              </div>
            </div>
          )}
          <div className="rec-contact-card">
            <strong className="rec-contact-title">Contact information:</strong>
            <div className="rec-contact-grid">
              {contactFields.length > 0 ? (
                contactFields.map(([key, value]) => (
                  <DetailRow
                    key={key}
                    label={key.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase())}
                    value={value}
                  />
                ))
              ) : (
                <div className="rec-detail">No contact information available</div>
              )}
            </div>
          </div>
        </div>
      )}
    </article>
  );
}

/* ===================== Main ===================== */
export default function Listings() {
  const [vendorId, setVendorId] = useState(null);
  const [houses, setHouses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");
  const [openId, setOpenId] = useState(null);

  useEffect(() => {
    setVendorId(getVendorIdFromLocalStorage());
  }, []);

  useEffect(() => {
    const fetchHouses = async () => {
      try {
        setLoading(true);
        setErr("");
        const token = getAuthToken();
        const res = await fetch(`${API_BASE}/api/houses/${vendorId}`, {
          headers: {
            "Content-Type": "application/json",
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
          },
        });
        const json = await res.json();
        if (!res.ok) throw new Error(json?.error || "Error obteniendo casas");
        // Limpiar los objetos eliminando claves con valor null
        const cleanedData = Array.isArray(json)
          ? json.map(item => {
              const filteredItem = {};
              for (const key in item) {
                if (item[key] !== null) {
                  filteredItem[key] = item[key];
                }
              }
              return filteredItem;
            })
          : [];
        setHouses(cleanedData);
      } catch (e) {
        console.error(e);
        setErr(e.message || "Error de red");
      } finally {
        setLoading(false);
      }
    };
    if (vendorId != null) fetchHouses();
  }, [vendorId]);

  return (
    <section className="rec-wrap rec-bg">
      <div className="rec-header">
        <h2 className="pref-title rec-title-page">My houses</h2>
        <p className="pref-subtitle rec-subtitle-page">
          {vendorId == null
            ? "Vendor ID not found"
            : `Published houses by vendor #${vendorId}`}
        </p>
      </div>

      {vendorId == null && (
        <div className="global-error">Login as vendor to see your listings.</div>
      )}

      {vendorId != null && (
        <>
          {loading && <div className="rec-state">Loading Houses...</div>}
          {err && !loading && <div className="global-error">{err}</div>}

          {!loading && !err && (
            <div className="rec-rail">
              {houses.length === 0 && (
                <div className="rec-empty">You don't have published houses yet</div>
              )}

              {houses.map((house, idx) => (
                <HouseCard
                  key={house?.house_id ?? idx}
                  house={house}
                  expanded={openId === (house?.house_id ?? idx)}
                  onToggle={() =>
                    setOpenId((cur) =>
                      cur === (house?.house_id ?? idx) ? null : (house?.house_id ?? idx)
                    )
                  }
                />
              ))}
            </div>
          )}
        </>
      )}
    </section>
  );
}