import { useState } from "react";
import { datasetMeta, quickDemoData } from "./publishData";
import "../../styles/seller/publishForms.css"; // estilos

// --- Utilidades de transformación ---
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

export default function Publish() {
  const [formType, setFormType] = useState(null); // "quick" | "long"
  const [formData, setFormData] = useState({});
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  // Creación de casa
  const [showCreateCard, setShowCreateCard] = useState(false);
  const [createLoading, setCreateLoading] = useState(false);
  const [lastPayload, setLastPayload] = useState(null);

  // Campos adicionales (el usuario los llena). sale_price se precarga con el precio calculado (sin redondear).
  const [createData, setCreateData] = useState({
    title: "",
    sale_price: 0,
    contact_phone: "",
    contact_email: "",
  });

  const quickFields = [
    "TotalSF","OverallQual","OverallCond","GrLivArea","Neighborhood","TotalBath","LotArea","CentralAir",
    "YearBuilt","RemodAge","YearRemodAdd","1stFlrSF","HouseAge","GarageArea","GarageScore","BsmtFinSF1",
    "SaleCondition","TotalPorchSF","GarageCars","2ndFlrSF","Fireplaces","RoomsPlusBathEq",
  ];

  // -------- Handlers --------
  const handleChange = (field, value) => { setFormData((prev) => ({ ...prev, [field]: value })); };

  const handleDemo = () => {
    if (formType === "quick") { setFormData(quickDemoData); return; }
    const newData = {};
    const allFields = [
      ...Object.keys(datasetMeta.numeric_means),
      ...Object.keys(datasetMeta.categorical_uniques),
    ];
    allFields.forEach((f) => {
      if (datasetMeta.numeric_means[f] !== undefined) newData[f] = datasetMeta.numeric_means[f];
      else if (datasetMeta.categorical_uniques[f]) {
        const opts = datasetMeta.categorical_uniques[f];
        newData[f] = opts[Math.floor(Math.random() * opts.length)];
      }
    });
    setFormData(newData);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const transformed = { ...formData }; // JSON camelCase para predicción
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
    const isNumeric = datasetMeta.numeric_means[field] !== undefined;

    if (!isNumeric && datasetMeta.categorical_uniques[field]) {
      return (
        <div className="field" key={field}>
          <label>{field}</label>
          <select
            className="input"
            value={formData[field] ?? ""}
            onChange={(e) => handleChange(field, e.target.value)}
          >
            <option value="">Select...</option>
            {datasetMeta.categorical_uniques[field].map((opt) => (
              <option key={opt} value={opt}>{opt}</option>
            ))}
          </select>
        </div>
      );
    }

    return (
      <div className="field" key={field}>
        <label>{field}</label>
        <input
          className="input"
          type="number"
          value={formData[field] ?? ""}
          onChange={(e) => handleChange(field, parseFloat(e.target.value) || 0)}
        />
      </div>
    );
  };

  // -------- Render --------
  return (
    <div className="pref-page">
      <div className="pref-container">
        <h1 className="pref-title">Publish a New House</h1>
        <p className="pref-subtitle">Fill in the form to predict a house price.</p>

        {!formType && (
          <div className="form-actions">
            <button className="btn" onClick={() => setFormType("quick")}>Quick Form</button>
            {/* Eliminado el botón de Long Form */}
          </div>
        )}

        {formType && (
          <form className="pref-form" onSubmit={handleSubmit}>
            <div className="pref-section">
              <div className="form-actions">
                <button type="button" className="btn ghost" onClick={handleDemo}>Demo</button>
              </div>

              <h3 className="section-title">Form</h3>

              <div className="grid-2">
                {quickFields.map((f) => renderField(f))}
              </div>

              <div className="form-actions">
                <button type="submit" className="btn" disabled={loading}>
                  {loading ? "Submitting..." : "Submit"}
                </button>
              </div>
            </div>
          </form>
        )}

        {prediction && (
          <div className="pref-section">
            <h3 className="section-title">PRICE</h3>
            <div className="pref-title" style={{ fontSize: "clamp(22px, 4vw, 36px)", margin: 0 }}>
              {formatPrice(prediction?.predicted_price)}
            </div>

            {!showCreateCard && (
              <div className="form-actions">
                <button className="btn" onClick={handleCreateHouse}>Crea tu casa ahora</button>
              </div>
            )}
          </div>
        )}

        {showCreateCard && (
          <div className="pref-section">
            <h3 className="section-title">Detalles de la publicación</h3>
            <form className="pref-form" onSubmit={handleCreateHouseSubmit}>
              <div className="grid-2">
                <div className="field">
                  <label>Título</label>
                  <input
                    className="input"
                    type="text"
                    value={createData.title}
                    placeholder="Título del anuncio"
                    onChange={(e) => handleCreateDataChange("title", e.target.value)}
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
                    onChange={(e) => handleCreateDataChange("contact_phone", e.target.value)}
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
                    onChange={(e) => handleCreateDataChange("contact_email", e.target.value)}
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
  );
}
