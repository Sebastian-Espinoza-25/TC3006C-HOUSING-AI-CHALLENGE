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
    // intentos directos
    const direct =
      localStorage.getItem("vendorId") || localStorage.getItem("vendor_id");
    if (direct) return Number(direct);

    // estructuras comunes
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

/* ========== Cargar fotos (Vite o CRA) ========== */
const loadHousePhotos = () => {
  // 1) Vite
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

  // 2) CRA/Webpack
  try {
    const ctx = require.context("../../Assets/HouseFotos", false, /\.(png|jpe?g|webp|avif|gif)$/i);
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
  const title = house?.title || "Sin título";
  const price = house?.sale_price;

  const imgUrl = useMemo(
    () => pickPhotoForHouse(house?.house_id),
    [house?.house_id]
  );

  // Etiquetas rápidas (máx 4)
  const tags = useMemo(() => {
    const out = [];
    if (house?.neighborhood) out.push(house.neighborhood);
    if (house?.house_style) out.push(house.house_style);
    if (house?.bedroom_abv_gr != null)
      out.push(`${Number(house.bedroom_abv_gr)} hab.`);
    if (house?.full_bath != null) out.push(`${Number(house.full_bath)} baños`);
    if (house?.garage_cars != null)
      out.push(`${Number(house.garage_cars)} autos`);
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
        <div
          className="rec-img"
          aria-hidden="true"
          style={imgUrl ? { backgroundImage: `url(${imgUrl})` } : undefined}
        />
        <div className="rec-main">
          <h4 className="rec-title">{title}</h4>
          <div className="rec-tags">
            {tags.map((t) => (
              <span className="rec-tag" key={t}>
                {t}
              </span>
            ))}
          </div>
        </div>
        <div className="rec-price">
          {price != null ? `$ ${formatPrice(price)}` : "S/D"}
        </div>
      </div>

      <div className="rec-divider" />

      <div className="rec-more">
        <span className="rec-more-text">
          {expanded ? "Hide details" : "See details"}
        </span>
        <span className={`rec-caret ${expanded ? "up" : ""}`} aria-hidden>
          ▾
        </span>
      </div>

      {expanded && (
        <div className="rec-details">
          <DetailRow label="Vecindario" value={house?.neighborhood} />
          <DetailRow label="Estilo" value={house?.house_style} />
          <DetailRow
            label="Construida"
            value={house?.year_built ? Number(house.year_built) : null}
          />
          <DetailRow
            label="Superficie habitable (GrLivArea)"
            value={
              house?.gr_liv_area ? `${Number(house.gr_liv_area)} ft²` : null
            }
          />
          <DetailRow
            label="1er piso"
            value={
              house?.first_flr_sf != null
                ? `${Number(house.first_flr_sf)} ft²`
                : null
            }
          />
          <DetailRow
            label="2do piso"
            value={
              house?.second_flr_sf != null
                ? `${Number(house.second_flr_sf)} ft²`
                : null
            }
          />
          <DetailRow
            label="Dormitorios"
            value={
              house?.bedroom_abv_gr != null ? Number(house.bedroom_abv_gr) : null
            }
          />
          <DetailRow
            label="Baños"
            value={
              house?.total_bath != null
                ? Number(house.total_bath)
                : house?.full_bath != null || house?.half_bath != null
                ? `${house?.full_bath ?? 0} / ${house?.half_bath ?? 0} (completos / medios)`
                : null
            }
          />
          <DetailRow
            label="Chimeneas"
            value={house?.fireplaces != null ? Number(house.fireplaces) : null}
          />
          <DetailRow
            label="Cochera (autos)"
            value={house?.garage_cars != null ? Number(house.garage_cars) : null}
          />
          <DetailRow
            label="Cochera (área)"
            value={
              house?.garage_area != null
                ? `${Number(house.garage_area)} ft²`
                : null
            }
          />
          <DetailRow
            label="Porche abierto"
            value={
              house?.open_porch_sf != null
                ? `${Number(house.open_porch_sf)} ft²`
                : null
            }
          />
          <DetailRow
            label="Piscina (área)"
            value={house?.pool_area != null ? Number(house.pool_area) : null}
          />
          <DetailRow
            label="A/C central"
            value={
              house?.central_air != null
                ? String(house.central_air) === "Y"
                  ? "Sí"
                  : "No"
                : null
            }
          />
          <DetailRow label="Condición de venta" value={house?.sale_condition} />
          <DetailRow label="Tipo de venta" value={house?.sale_type} />
          <DetailRow label="Descripción" value={house?.description} />

          <div className="rec-subtitle">Contact</div>
          <DetailRow label="Teléfono" value={house?.contact_phone} />
          <DetailRow label="Email" value={house?.contact_email} />
          <DetailRow label="Vendor ID" value={house?.vendor_id} />
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

  // Lee vendorId una sola vez
  useEffect(() => {
    setVendorId(getVendorIdFromLocalStorage());
  }, []);

  // Fetch cuando ya tenemos vendorId
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
        setHouses(Array.isArray(json) ? json : []);
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
    <section className="rec-wrap">
      <div className="rec-header">
        <h2 className="pref-title rec-title-page">My houses</h2>
        <p className="pref-subtitle rec-subtitle-page">
          {vendorId == null
            ? "Vendor ID not found"
            : `Published houses by vendor #${vendorId}`}
        </p>
      </div>

      {vendorId == null && (
        <div className="global-error">
          Login as vendor to see your listings.
        </div>
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

              {houses.map((house) => (
                <HouseCard
                  key={house?.house_id || Math.random()}
                  house={house}
                  expanded={openId === house?.house_id}
                  onToggle={() =>
                    setOpenId((cur) => (cur === house?.house_id ? null : house?.house_id))
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
