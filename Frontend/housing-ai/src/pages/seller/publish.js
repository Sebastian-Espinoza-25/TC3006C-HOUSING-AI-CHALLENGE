import { useState, useEffect } from "react";
import { datasetMeta, quickDemoData } from "./publishData";
import { categoricalFields } from "./publishOptions";
import "../../styles/seller/publishForms.css";


const KEY_OVERRIDES = {
  TotalSF: "total_sf",
  OverallQual: "overall_qual",
  OverallCond: "overall_cond",
  GrLivArea: "gr_liv_area",
  Neighborhood: "neighborhood",
  TotalBath: "total_bath",
  LotArea: "lot_area",
  CentralAir: "central_air",
  YearBuilt: "year_built",
  RemodAge: "remod_age",
  YearRemodAdd: "year_remod_add",
  "1stFlrSF": "first_flr_sf",
  HouseAge: "house_age",
  GarageArea: "garage_area",
  GarageScore: "garage_score",
  BsmtFinSF1: "bsmt_fin_sf1",
  SaleCondition: "sale_condition",
  TotalPorchSF: "total_porch_sf",
  GarageCars: "garage_cars",
  "2ndFlrSF": "second_flr_sf",
  Fireplaces: "fireplaces",
  RoomsPlusBathEq: "rooms_plus_bath_eq",
  MSSubClass: "ms_sub_class",
  MSZoning: "ms_zoning",
  LotFrontage: "lot_frontage",
  LotShape: "lot_shape",
  LandContour: "land_contour",
  LotConfig: "lot_config",
  Alley: "alley",
  BldgType: "bldg_type",
  HouseStyle: "house_style",
  RoofStyle: "roof_style",
  Exterior1st: "exterior1st",
  Exterior2nd: "exterior2nd",
  MasVnrType: "mas_vnr_type",
  MasVnrArea: "mas_vnr_area",
  ExterQual: "exter_qual",
  ExterCond: "exter_cond",
  Foundation: "foundation",
  BsmtQual: "bsmt_qual",
  BsmtCond: "bsmt_cond",
  BsmtExposure: "bsmt_exposure",
  BsmtFinType1: "bsmt_fin_type1",
  BsmtFinType2: "bsmt_fin_type2",
  BsmtFinSF2: "bsmt_fin_sf2",
  BsmtUnfSF: "bsmt_unf_sf",
  TotalBsmtSF: "total_bsmt_sf",
  HeatingQC: "heating_qc",
  Electrical: "electrical",
  OpenPorchSF: "open_porch_sf",
  EnclosedPorch: "enclosed_porch",
  ThreeSsnPorch: "three_ssn_porch",
  ScreenPorch: "screen_porch",
  PoolArea: "pool_area",
  PoolQC: "pool_qc",
  Fence: "fence",
  MiscFeature: "misc_feature",
  MoSold: "mo_sold",
  YrSold: "yr_sold",
  KitchenAbvGr: "kitchen_abv_gr",
  KitchenQual: "kitchen_qual",
  TotRmsAbvGrd: "tot_rms_abv_grd",
  Functional: "functional",
  FireplaceQu: "fireplace_qu",
  GarageType: "garage_type",
  GarageYrBlt: "garage_yr_blt",
  GarageFinish: "garage_finish",
  GarageQual: "garage_qual",
  GarageCond: "garage_cond",
  PavedDrive: "paved_drive",
  WoodDeckSF: "wood_deck_sf",
  SaleType: "sale_type",
};

function toSnakeKey(key) {
  if (KEY_OVERRIDES[key] != null) return KEY_OVERRIDES[key];
  return key
    .replace(/([a-z0-9])([A-Z])/g, "$1_$2")
    .replace(/([A-Z]+)([A-Z][a-z0-9]+)/g, "$1_$2")
    .toLowerCase();
}
function toSnakeCaseObject(obj) {
  const out = {};
  Object.keys(obj || {}).forEach((k) => { out[toSnakeKey(k)] = obj[k]; });
  return out;
}

// formatea el precio (sin asumir moneda; si quieres MXN pon currency: 'MXN')
const formatPrice = (v) =>
  new Intl.NumberFormat("es-MX", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(Number(v || 0));


// Define las secciones y los campos de cada una (solo los de quickDemoData)
const formSections = [
  {
    label: "Generales",
    fields: [
      "TotalSF",
      "OverallQual",
      "OverallCond",
      "GrLivArea",
      "Neighborhood",
      "YearBuilt",
      "RemodAge",
      "YearRemodAdd",
      "HouseAge",
      "1stFlrSF"
    ]
  },
  {
    label: "Características",
    fields: [
      "TotalBath",
      "LotArea",
      "CentralAir",
      "GarageArea",
      "GarageScore",
      "GarageCars",
      "BsmtFinSF1"
    ]
  },
  {
    label: "Extras",
    fields: [
      "SaleCondition",
      "TotalPorchSF",
      "2ndFlrSF",
      "Fireplaces",
      "RoomsPlusBathEq"
    ]
  }
];

const fieldLabels = {
  TotalSF: "Superficie total (m²)",
  OverallQual: "Calidad general",
  OverallCond: "Condición general",
  GrLivArea: "Área habitable (m²)",
  Neighborhood: "Vecindario",
  TotalBath: "Baños totales",
  LotArea: "Área del terreno (m²)",
  CentralAir: "Aire acondicionado central",
  YearBuilt: "Año de construcción",
  RemodAge: "Años desde remodelación",
  YearRemodAdd: "Año de remodelación",
  "1stFlrSF": "Superficie 1er piso (m²)",
  HouseAge: "Edad de la casa (años)",
  GarageArea: "Área de cochera (m²)",
  GarageScore: "Puntaje de cochera",
  BsmtFinSF1: "Sótano terminado 1 (m²)",
  SaleCondition: "Condición de venta",
  TotalPorchSF: "Superficie de porches (m²)",
  GarageCars: "Coches en cochera",
  "2ndFlrSF": "Superficie 2do piso (m²)",
  Fireplaces: "Chimeneas",
  RoomsPlusBathEq: "Habitaciones + baños eq.",
};

export default function Publish() {
  const [formType, setFormType] = useState(null);
  const [formData, setFormData] = useState({});
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  // Sección activa del formulario
  const [activeSection, setActiveSection] = useState(0);

  // Creación de casa
  const [showCreateCard, setShowCreateCard] = useState(false);
  const [createLoading, setCreateLoading] = useState(false);
  const [lastPayload, setLastPayload] = useState(null);

  const [createData, setCreateData] = useState({
    title: "",
    sale_price: 0,
    contact_phone: "",
    contact_email: "",
  });

  const [hasSubmitted, setHasSubmitted] = useState(false);

  // -------- Handlers --------
  const handleChange = (field, value) => { setFormData((prev) => ({ ...prev, [field]: value })); };

  const handleDemo = () => {
    // Llena todos los campos de todas las secciones con quickDemoData si existe, si no, usa el meta
    const demo = {};
    formSections.forEach(section => {
      section.fields.forEach(f => {
        if (quickDemoData[f] !== undefined) {
          demo[f] = quickDemoData[f];
        } else if (datasetMeta.numeric_means[f] !== undefined) {
          demo[f] = datasetMeta.numeric_means[f];
        } else if (datasetMeta.categorical_uniques[f]) {
          const opts = datasetMeta.categorical_uniques[f];
          demo[f] = opts[Math.floor(Math.random() * opts.length)];
        }
      });
    });
    setFormData(demo);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("JSON enviado:", JSON.stringify(formData, null, 2));
    // Asegura que los campos numéricos sean floats
    const transformed = {};
    Object.keys(formData).forEach((k) => {
      if (datasetMeta.numeric_means[k] !== undefined) {
        transformed[k] = parseFloat(formData[k]) || 0.0;
      } else {
        transformed[k] = formData[k];
      }
    });
    setLastPayload(transformed);

    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:5001/api/ai/predict/simple", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(transformed),
      });
      if (!response.ok) throw new Error("Error fetching prediction");
      const data = await response.json();
      setPrediction(data);

      const predicted = Number(data && data.predicted_price ? data.predicted_price : 0);
      setCreateData((prev) => ({ ...prev, sale_price: predicted }));
    } catch (err) {
      console.error("Error:", err);
      alert("Error enviando datos a la API de predicción.");
    } finally {
      setLoading(false);
    }
  };

  const getVendorIdFromLocalStorage = () => {
    try {
      const directVendorId = localStorage.getItem("vendorId");
      if (directVendorId) return Number(directVendorId);
      const rawUser =
        localStorage.getItem("user") ||
        localStorage.getItem("auth") ||
        localStorage.getItem("profile");
      if (!rawUser) return null;
      const parsed = JSON.parse(rawUser);
      return (
        parsed?.vendorId ??
        parsed?.vendor_id ??
        parsed?.user?.vendorId ??
        parsed?.user?.vendor_id ??
        null
      );
    } catch { return null; }
  };

  const getAuthToken = () => {
    try { return localStorage.getItem("token") || localStorage.getItem("authToken") || null; }
    catch { return null; }
  };

  const handleCreateHouse = () => { setShowCreateCard(true); };
  const handleCreateDataChange = (field, value) => { setCreateData((prev) => ({ ...prev, [field]: value })); };

  const handleCreateHouseSubmit = async (e) => {
    e.preventDefault();
    if (!lastPayload) { alert("Primero calcula el precio enviando el formulario."); return; }

    const vendorId = getVendorIdFromLocalStorage();
    if (!vendorId) { alert("No se encontró vendorId en localStorage. Inicia sesión nuevamente."); return; }

    const snakeFromForm = toSnakeCaseObject(lastPayload);
    const createPayload = {
      ...snakeFromForm,
      title: createData.title,
      sale_price: Number(createData.sale_price), // sin redondear
      contact_phone: createData.contact_phone,
      contact_email: createData.contact_email,
      predicted_price: prediction ? prediction.predicted_price : undefined,
      model_type: prediction ? prediction.model_type : undefined,
      vendor_id: Number(vendorId),
      status: "available",
    };

    try {
      setCreateLoading(true);
      const token = getAuthToken();
      const res = await fetch(`http://127.0.0.1:5001/api/vendors/${vendorId}/houses`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify(createPayload),
      });
      if (!res.ok) {
        let errText = await res.text();
        try { errText = JSON.stringify(JSON.parse(errText), null, 2); } catch {}
        throw new Error(errText || "Error creando la casa");
      }
      const json = await res.json();
      console.log("✅ Casa creada:", json);
      alert("Casa creada exitosamente");
      setShowCreateCard(false);
    } catch (err) {
      console.error("❌ Error al crear la casa:", err);
      alert("Error al crear la casa (ver consola).");
    } finally {
      setCreateLoading(false);
    }
  };

  // -------- UI helpers --------
  const renderField = (field) => {
    // Busca si el campo es categórico y tiene opciones amigables
    const catField = categoricalFields.find(f => f.name === field);
    const label = catField?.label || fieldLabels[field] || field;

    if (catField) {
      return (
        <div className="field" key={field}>
          <label>{label}</label>
          <select
            className="input"
            value={formData[field] ?? ""}
            onChange={(e) => handleChange(field, e.target.value)}
          >
            <option value="">Selecciona...</option>
            {catField.options.map((opt) => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>
      );
    }

    // Campos numéricos
    return (
      <div className="field" key={field}>
        <label>{label}</label>
        <input
          className="input"
          type="number"
          value={formData[field] ?? ""}
          onChange={(e) => handleChange(field, parseFloat(e.target.value) || 0)}
        />
      </div>
    );
  };

  const [startAnim, setStartAnim] = useState(false);

  const handleStartClick = () => {
    setStartAnim(true);
    setTimeout(() => {
      setFormType("quick");
      setStartAnim(false);
    }, 900);
  };

  // Calcula el porcentaje de progreso basado en campos llenados
  const allFields = formSections.flatMap(section => section.fields);
  const filledFields = allFields.filter(f => formData[f] !== undefined && formData[f] !== "" && formData[f] !== null);
  const progressPercent = (filledFields.length / allFields.length) * 100;

  // Estado para controlar el submit en la última sección
  const [canSubmit, setCanSubmit] = useState(true);

  useEffect(() => {
    if (activeSection === formSections.length - 1) {
      setCanSubmit(false);
      const timer = setTimeout(() => setCanSubmit(true), 1000);
      return () => clearTimeout(timer);
    } else {
      setCanSubmit(true);
    }
  }, [activeSection]);

  // -------- Render --------
  return (
    <div className="publish-bg">
      {/* Card de inicio */}
      {!formType && (
        <div className="publish-start-card">
          <h1 className="publish-title">Publica una casa</h1>
          <p className="publish-subtitle">Llena el formulario para predecir el precio de una casa.</p>
          <button
            className={`start-btn-anim${startAnim ? " animating" : ""}`}
            onClick={handleStartClick}
            disabled={startAnim}
          >
            {startAnim ? (
              <span className="checkmark">
                <svg viewBox="0 0 32 32" width="28" height="28">
                  <polyline
                    points="8 17.5 14 23 24 11"
                    style={{
                      fill: "none",
                      stroke: "#fff",
                      strokeWidth: 3.5,
                      strokeLinecap: "round",
                      strokeLinejoin: "round",
                    }}
                  />
                </svg>
              </span>
            ) : (
              "Comenzar"
            )}
          </button>
        </div>
      )}

      {/* Card del formulario multisección */}
      {formType && (
        <div style={{ width: "100%", display: "flex", flexDirection: "column", alignItems: "center" }}>
          {/* Tabs de secciones - FUERA de la card */}
          <div className="form-tabs">
            {formSections.map((section, idx) => (
              <button
                key={section.label}
                className={`form-tab${activeSection === idx ? " active" : ""}`}
                onClick={() => setActiveSection(idx)}
                type="button"
                disabled={activeSection === idx}
              >
                {section.label}
              </button>
            ))}
          </div>

          {/* Card del formulario multisección */}
          <div className="form-card">
            {/* Aquí va la barra de progreso */}
            <div className="form-progress-bar-outer">
              <div
                className="form-progress-bar-inner"
                style={{ width: `${progressPercent}%` }}
              />
            </div>

            {/* Formulario de la sección activa */}
            <form
              className="pref-form"
              onSubmit={(e) => {
                // Solo permite submit si está en la última sección y fue por botón
                if (activeSection !== formSections.length - 1 || !hasSubmitted) {
                  e.preventDefault();
                  setHasSubmitted(false);
                  return;
                }
                handleSubmit(e);
                setHasSubmitted(false); // reset
              }}
              onKeyDown={(e) => {
                // Previene submit con Enter en cualquier campo
                if (e.key === "Enter") {
                  e.preventDefault();
                }
              }}
            >
              <div
                className={
                  "form-fields" +
                  (formSections[activeSection].fields.length > 5 ? " grid-2" : "")
                }
              >
                {formSections[activeSection].fields.map((f) => renderField(f))}
              </div>
              <div className="form-actions">
                {activeSection > 0 && (
                  <button type="button" className="btn ghost" onClick={() => setActiveSection(activeSection - 1)}>
                    Anterior
                  </button>
                )}
                {activeSection < formSections.length - 1 ? (
                  <button
                    type="button"
                    className="btn"
                    onClick={() => setActiveSection(activeSection + 1)}
                  >
                    Siguiente
                  </button>
                ) : (
                  <button
                    type="submit"
                    className="btn"
                    disabled={loading || !canSubmit}
                    onClick={() => setHasSubmitted(true)}
                  >
                    {loading ? "Enviando..." : "Enviar"}
                  </button>
                )}
                <button type="button" className="btn ghost" onClick={handleDemo} style={{marginLeft: "auto"}}>
                  Demo
                </button>
              </div>
            </form>

            {/* Resultado de predicción */}
            {prediction && (
              <div className="form-result">
                <h3 className="section-title">PRECIO ESTIMADO</h3>
                <div className="pref-title" style={{ fontSize: "clamp(22px, 4vw, 36px)", margin: 0 }}>
                  {formatPrice(prediction?.predicted_price)}
                </div>
                {!showCreateCard && (
                  <div className="form-actions">
                    <button className="btn" onClick={() => setShowCreateCard(true)}>Crea tu casa ahora</button>
                  </div>
                )}
              </div>
            )}

            {/* Card para crear la casa */}
            {showCreateCard && (
              <div className="form-result">
                <h3 className="section-title">Detalles de la publicación</h3>
                <form className="pref-form" onSubmit={handleCreateHouseSubmit}>
                  <div className="form-fields">
                    <div className="field">
                      <label>Título</label>
                      <input
                        className="input"
                        type="text"
                        value={createData.title}
                        placeholder="Título del anuncio"
                        onChange={(e) => setCreateData((prev) => ({ ...prev, title: e.target.value }))}
                        required
                      />
                    </div>
                    <div className="field">
                      <label>Precio de venta (calculado)</label>
                      <input
                        className="input"
                        type="number"
                        value={createData.sale_price}
                        readOnly
                      />
                    </div>
                    <div className="field">
                      <label>Teléfono de contacto</label>
                      <input
                        className="input"
                        type="tel"
                        value={createData.contact_phone}
                        placeholder="Ej. 555-0123"
                        onChange={(e) => setCreateData((prev) => ({ ...prev, contact_phone: e.target.value }))}
                        required
                      />
                    </div>
                    <div className="field">
                      <label>Email de contacto</label>
                      <input
                        className="input"
                        type="email"
                        value={createData.contact_email}
                        placeholder="vendor@example.com"
                        onChange={(e) => setCreateData((prev) => ({ ...prev, contact_email: e.target.value }))}
                        required
                      />
                    </div>
                  </div>
                  <div className="form-actions">
                    <button type="submit" className="btn" disabled={createLoading}>
                      {createLoading ? "Creando..." : "Crear casa"}
                    </button>
                    <button type="button" className="btn ghost" onClick={() => setShowCreateCard(false)}>
                      Cancelar
                    </button>
                  </div>
                </form>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
