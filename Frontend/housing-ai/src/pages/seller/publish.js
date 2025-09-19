import { useState } from "react";
import { datasetMeta, quickDemoData } from "./publishData";

// --- Utilidades de transformación ---
const KEY_OVERRIDES = {
  // quickFields + comunes del dataset de casas
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

  // Extra comunes (por si usas el formulario largo)
  MSSubClass: "ms_sub_class",
  MSZoning: "ms_zoning",
  LotFrontage: "lot_frontage",
  LotShape: "lot_shape",
  LandContour: "land_contour",
  LotConfig: "lot_config",
  Alley: "alley",
  BldgType: "bldg_type",
  HouseStyle: "house_style",
  OverallCond: "overall_cond",
  YearRemodAdd: "year_remod_add",
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
  "1stFlrSF": "first_flr_sf", // refuerzo
  "2ndFlrSF": "second_flr_sf", // refuerzo
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
  Fireplaces: "fireplaces",
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
  // fallback genérico camelCase/PascalCase -> snake_case (mejor esfuerzo)
  return key
    .replace(/([a-z0-9])([A-Z])/g, "$1_$2")
    .replace(/([A-Z]+)([A-Z][a-z0-9]+)/g, "$1_$2")
    .toLowerCase();
}

function toSnakeCaseObject(obj) {
  const out = {};
  Object.keys(obj || {}).forEach((k) => {
    out[toSnakeKey(k)] = obj[k];
  });
  return out;
}

export default function Publish() {
  const [formType, setFormType] = useState(null); // "quick" | "long"
  const [formData, setFormData] = useState({});
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  // Creación de casa
  const [showCreateCard, setShowCreateCard] = useState(false);
  const [createLoading, setCreateLoading] = useState(false);
  const [createResult, setCreateResult] = useState(null);
  const [lastPayload, setLastPayload] = useState(null);

  // Campos adicionales (el usuario los llena). sale_price se precarga con el precio calculado (sin redondear).
  const [createData, setCreateData] = useState({
    title: "",
    sale_price: 0,
    contact_phone: "",
    contact_email: "",
  });

  const quickFields = [
    "TotalSF",
    "OverallQual",
    "OverallCond",
    "GrLivArea",
    "Neighborhood",
    "TotalBath",
    "LotArea",
    "CentralAir",
    "YearBuilt",
    "RemodAge",
    "YearRemodAdd",
    "1stFlrSF",
    "HouseAge",
    "GarageArea",
    "GarageScore",
    "BsmtFinSF1",
    "SaleCondition",
    "TotalPorchSF",
    "GarageCars",
    "2ndFlrSF",
    "Fireplaces",
    "RoomsPlusBathEq",
  ];

  // -------- Handlers --------
  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleDemo = () => {
    if (formType === "quick") {
      setFormData(quickDemoData);
      return;
    }
    const newData = {};
    const allFields = [
      ...Object.keys(datasetMeta.numeric_means),
      ...Object.keys(datasetMeta.categorical_uniques),
    ];
    allFields.forEach((f) => {
      if (datasetMeta.numeric_means[f] !== undefined) {
        newData[f] = datasetMeta.numeric_means[f];
      } else if (datasetMeta.categorical_uniques[f]) {
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

      // SIN redondear:
      const predicted = Number(
        data && data.predicted_price ? data.predicted_price : 0
      );
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
      // intenta varias ubicaciones comunes
      const rawUser =
        localStorage.getItem("user") ||
        localStorage.getItem("auth") ||
        localStorage.getItem("profile");

      // si guardaste vendorId directo:
      const directVendorId = localStorage.getItem("vendorId");
      if (directVendorId) return Number(directVendorId);

      if (!rawUser) return null;
      const parsed = JSON.parse(rawUser);
      return (
        parsed?.vendorId ??
        parsed?.vendor_id ??
        parsed?.user?.vendorId ??
        parsed?.user?.vendor_id ??
        null
      );
    } catch {
      return null;
    }
  };

  const getAuthToken = () => {
    try {
      return localStorage.getItem("token") || localStorage.getItem("authToken") || null;
    } catch {
      return null;
    }
  };

  const handleCreateHouse = () => {
    setShowCreateCard(true);
  };

  const handleCreateDataChange = (field, value) => {
    setCreateData((prev) => ({ ...prev, [field]: value }));
  };

  const handleCreateHouseSubmit = async (e) => {
    e.preventDefault();

    if (!lastPayload) {
      alert("Primero calcula el precio enviando el formulario.");
      return;
    }

    const vendorId = getVendorIdFromLocalStorage();
    if (!vendorId) {
      alert("No se encontró vendorId en localStorage. Inicia sesión nuevamente.");
      return;
    }

    // 1) Convierte TODOS los atributos del formulario a snake_case
    const snakeFromForm = toSnakeCaseObject(lastPayload);

    // 2) Construye el payload final en snake_case (sin redondear sale_price)
    const createPayload = {
      ...snakeFromForm,
      title: createData.title,
      sale_price: Number(createData.sale_price), // sin redondear
      contact_phone: createData.contact_phone,
      contact_email: createData.contact_email,
      predicted_price: prediction ? prediction.predicted_price : undefined,
      model_type: prediction ? prediction.model_type : undefined,
      vendor_id: Number(vendorId),
      status: "available", // opcional: quítalo si tu backend lo asigna por defecto
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
      setCreateResult(json);
      alert("Casa creada exitosamente");
    } catch (err) {
      console.error(err);
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
        <div key={field}>
          <label>
            {field}:{" "}
            <select
              value={formData[field] ?? ""}
              onChange={(e) => handleChange(field, e.target.value)}
            >
              <option value="">Select...</option>
              {datasetMeta.categorical_uniques[field].map((opt) => (
                <option key={opt} value={opt}>
                  {opt}
                </option>
              ))}
            </select>
          </label>
        </div>
      );
    }

    return (
      <div key={field}>
        <label>
          {field}:{" "}
          <input
            type="number"
            value={formData[field] ?? ""}
            onChange={(e) => handleChange(field, parseFloat(e.target.value) || 0)}
          />
        </label>
      </div>
    );
  };

  // -------- Render --------
  return (
    <div>
      <h1>Publish a New Listing</h1>

      {!formType && (
        <div>
          <button onClick={() => setFormType("quick")}>Quick Form</button>
          <button onClick={() => setFormType("long")}>Long Form</button>
        </div>
      )}

      {formType && (
        <form onSubmit={handleSubmit}>
          <button type="button" onClick={handleDemo}>Demo</button>

          {(formType === "quick"
            ? quickFields
            : [
                ...Object.keys(datasetMeta.numeric_means),
                ...Object.keys(datasetMeta.categorical_uniques),
              ]
          ).map((f) => renderField(f))}

          <button type="submit">{loading ? "Submitting..." : "Submit"}</button>
        </form>
      )}

      {prediction && (
        <div>
          <h2>Prediction Result:</h2>
          <pre>{JSON.stringify(prediction, null, 2)}</pre>

          {!showCreateCard && (
            <button onClick={handleCreateHouse}>Crea tu casa ahora</button>
          )}
        </div>
      )}

      {showCreateCard && (
        <div>
          <h3>Detalles de la publicación</h3>
          <form onSubmit={handleCreateHouseSubmit}>
            <div>
              <label>
                Título:{" "}
                <input
                  type="text"
                  value={createData.title}
                  placeholder="Título del anuncio"
                  onChange={(e) => handleCreateDataChange("title", e.target.value)}
                  required
                />
              </label>
            </div>

            <div>
              <label>
                Precio de venta (calculado):{" "}
                <input
                  type="number"
                  value={createData.sale_price}
                  readOnly
                />
              </label>
            </div>

            <div>
              <label>
                Teléfono de contacto:{" "}
                <input
                  type="tel"
                  value={createData.contact_phone}
                  placeholder="Ej. 555-0123"
                  onChange={(e) => handleCreateDataChange("contact_phone", e.target.value)}
                  required
                />
              </label>
            </div>

            <div>
              <label>
                Email de contacto:{" "}
                <input
                  type="email"
                  value={createData.contact_email}
                  placeholder="vendor@example.com"
                  onChange={(e) => handleCreateDataChange("contact_email", e.target.value)}
                  required
                />
              </label>
            </div>

            <button type="submit" disabled={createLoading}>
              {createLoading ? "Creando..." : "Crear casa"}
            </button>
          </form>

          {createResult && (
            <div>
              <strong>Respuesta del servidor:</strong>
              <pre>{JSON.stringify(createResult, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
