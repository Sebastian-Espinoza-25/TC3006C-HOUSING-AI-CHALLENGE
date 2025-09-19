import { useMemo, useState } from "react";
import datasetSummary from "../../Assets/dataset_summary.json";
import "../../styles/buyer.css";

/* ---------- Helpers UI ---------- */

function Options({ values = [], placeholder }) {
  return (
    <>
      <option value="">{placeholder}</option>
      {values.map((v) => (
        <option key={v} value={v}>{v}</option>
      ))}
    </>
  );
}

function NumberRange({ label, minKey, maxKey, state, setState, step = "any" }) {
  const minVal = state[minKey] ?? "";
  const maxVal = state[maxKey] ?? "";
  const hasError = minVal !== "" && maxVal !== "" && parseFloat(minVal) > parseFloat(maxVal);

  const onChange = (key) => (e) => {
    const value = e.target.value;
    setState((prev) => ({ ...prev, [key]: value === "" ? "" : value }));
  };

  return (
    <div className="range-row">
      <label className="range-label">{label}</label>
      <div className="range-inputs">
        <input
          type="number"
          step={step}
          inputMode="decimal"
          placeholder="Min"
          value={minVal}
          onChange={onChange(minKey)}
          className={hasError ? "input error" : "input"}
        />
        <span className="range-sep">—</span>
        <input
          type="number"
          step={step}
          inputMode="decimal"
          placeholder="Max"
          value={maxVal}
          onChange={onChange(maxKey)}
          className={hasError ? "input error" : "input"}
        />
      </div>
      {hasError && <div className="field-hint error-text">Min debe ser ≤ Max.</div>}
    </div>
  );
}

function YesNo({ label, value, onChange }) {
  return (
    <div className="field">
      <label>{label}</label>
      <select className="input" value={value ?? ""} onChange={(e) => onChange(e.target.value === "true")}>
        <option value="">(cualquiera)</option>
        <option value="true">Sí</option>
        <option value="false">No</option>
      </select>
    </div>
  );
}

/* ---------- Component ---------- */

export default function Preferences() {
  /* Categóricos del dataset (memo estables para evitar warnings) */
  const U = useMemo(() => datasetSummary?.categorical_uniques ?? {}, []);
  const C = useMemo(
    () => ({
      Neighborhood: U.Neighborhood ?? [],
      MSZoning: U.MSZoning ?? [],
      LotShape: U.LotShape ?? [],
      LandContour: U.LandContour ?? [],
      LotConfig: U.LotConfig ?? [],
      Condition1: U.Condition1 ?? [],
      BldgType: U.BldgType ?? [],
      HouseStyle: U.HouseStyle ?? [],
      RoofStyle: U.RoofStyle ?? [],
      Exterior1st: U.Exterior1st ?? [],
      Exterior2nd: U.Exterior2nd ?? [],
      Foundation: U.Foundation ?? [],
      ExterQual: U.ExterQual ?? [],
      ExterCond: U.ExterCond ?? [],
      BsmtQual: U.BsmtQual ?? [],
      BsmtCond: U.BsmtCond ?? [],
      BsmtExposure: U.BsmtExposure ?? [],
      BsmtFinType1: U.BsmtFinType1 ?? [],
      BsmtFinType2: U.BsmtFinType2 ?? [],
      HeatingQC: U.HeatingQC ?? [],
      Electrical: U.Electrical ?? [],
      KitchenQual: U.KitchenQual ?? [],
      Functional: U.Functional ?? [],
      FireplaceQu: U.FireplaceQu ?? [],
      GarageType: U.GarageType ?? [],
      GarageFinish: U.GarageFinish ?? [],
      GarageQual: U.GarageQual ?? [],
      GarageCond: U.GarageCond ?? [],
      PavedDrive: U.PavedDrive ?? [],
      PoolQC: U.PoolQC ?? [],
      Fence: U.Fence ?? [],
      MiscFeature: U.MiscFeature ?? [],
      SaleType: U.SaleType ?? [],
      SaleCondition: U.SaleCondition ?? [],
    }),
    [U]
  );

  /* State del formulario (nombres idénticos a tu tabla, más los nuevos de TotalSF) */
  const [form, setForm] = useState({
    // Ubicación y zona
    preferred_neighborhood: "",
    preferred_ms_zoning: "",
    preferred_lot_shape: "",
    preferred_land_contour: "",
    preferred_lot_config: "",
    preferred_condition1: "",

    // Tipo de casa
    preferred_bldg_type: "",
    preferred_house_style: "",
    preferred_roof_style: "",
    preferred_exterior1st: "",
    preferred_exterior2nd: "",
    preferred_foundation: "",

    // Calidad y condición
    min_overall_qual: "",
    max_overall_qual: "",
    min_overall_cond: "",
    max_overall_cond: "",
    min_exter_qual: "",
    min_exter_cond: "",

    // Años
    min_year_built: "",
    max_year_built: "",
    min_year_remod_add: "",
    max_year_remod_add: "",

    // Tamaños / áreas
    min_lot_area: "",
    max_lot_area: "",
    min_lot_frontage: "",
    max_lot_frontage: "",
    min_gr_liv_area: "",
    max_gr_liv_area: "",
    min_total_bsmt_sf: "",
    max_total_bsmt_sf: "",

    // Habitaciones y baños
    min_bedroom_abv_gr: "",
    max_bedroom_abv_gr: "",
    min_kitchen_abv_gr: "",
    max_kitchen_abv_gr: "",
    min_tot_rms_abv_grd: "",
    max_tot_rms_abv_grd: "",
    min_full_bath: "",
    max_full_bath: "",
    min_half_bath: "",
    max_half_bath: "",
    min_bsmt_full_bath: "",
    max_bsmt_full_bath: "",
    min_bsmt_half_bath: "",
    max_bsmt_half_bath: "",

    // Sótano
    preferred_bsmt_qual: "",
    preferred_bsmt_cond: "",
    preferred_bsmt_exposure: "",
    preferred_bsmt_fin_type1: "",
    preferred_bsmt_fin_type2: "",
    min_bsmt_fin_sf1: "",
    max_bsmt_fin_sf1: "",
    min_bsmt_fin_sf2: "",
    max_bsmt_fin_sf2: "",
    min_bsmt_unf_sf: "",
    max_bsmt_unf_sf: "",

    // Calefacción y A/A
    preferred_heating_qc: "",
    central_air_required: "",
    preferred_electrical: "",

    // Cocina
    min_kitchen_qual: "",

    // Funcionalidad
    preferred_functional: "",

    // Chimeneas
    min_fireplaces: "",
    max_fireplaces: "",
    preferred_fireplace_qu: "",

    // Garaje
    preferred_garage_type: "",
    min_garage_yr_blt: "",
    max_garage_yr_blt: "",
    preferred_garage_finish: "",
    min_garage_cars: "",
    max_garage_cars: "",
    min_garage_area: "",
    max_garage_area: "",
    preferred_garage_qual: "",
    preferred_garage_cond: "",
    preferred_paved_drive: "",

    // Porches / exteriores
    min_wood_deck_sf: "",
    max_wood_deck_sf: "",
    min_open_porch_sf: "",
    max_open_porch_sf: "",
    min_enclosed_porch: "",
    max_enclosed_porch: "",
    min_3ssn_porch: "",
    max_3ssn_porch: "",
    min_screen_porch: "",
    max_screen_porch: "",

    // Piscina
    min_pool_area: "",
    max_pool_area: "",
    preferred_pool_qc: "",

    // Cercas y misceláneos
    preferred_fence: "",
    preferred_misc_feature: "",

    // Precio
    min_sale_price: "",
    max_sale_price: "",

    // Tipo/condición venta
    preferred_sale_type: "",
    preferred_sale_condition: "",

    /* --------- Derivados: TotalSF --------- */
    totalSF_min_1st: "",
    totalSF_min_2nd: "",
    totalSF_min_bsmt: "",
    totalSF_max_1st: "",
    totalSF_max_2nd: "",
    totalSF_max_bsmt: "",
  });

  const [globalError, setGlobalError] = useState("");

  /* Pares numéricos a validar min<=max */
  const pairs = [
    ["min_overall_qual", "max_overall_qual"],
    ["min_overall_cond", "max_overall_cond"],
    ["min_year_built", "max_year_built"],
    ["min_year_remod_add", "max_year_remod_add"],
    ["min_lot_area", "max_lot_area"],
    ["min_lot_frontage", "max_lot_frontage"],
    ["min_gr_liv_area", "max_gr_liv_area"],
    ["min_total_bsmt_sf", "max_total_bsmt_sf"],
    ["min_bedroom_abv_gr", "max_bedroom_abv_gr"],
    ["min_kitchen_abv_gr", "max_kitchen_abv_gr"],
    ["min_tot_rms_abv_grd", "max_tot_rms_abv_grd"],
    ["min_full_bath", "max_full_bath"],
    ["min_half_bath", "max_half_bath"],
    ["min_bsmt_full_bath", "max_bsmt_full_bath"],
    ["min_bsmt_half_bath", "max_bsmt_half_bath"],
    ["min_bsmt_fin_sf1", "max_bsmt_fin_sf1"],
    ["min_bsmt_fin_sf2", "max_bsmt_fin_sf2"],
    ["min_bsmt_unf_sf", "max_bsmt_unf_sf"],
    ["min_fireplaces", "max_fireplaces"],
    ["min_garage_yr_blt", "max_garage_yr_blt"],
    ["min_garage_cars", "max_garage_cars"],
    ["min_garage_area", "max_garage_area"],
    ["min_wood_deck_sf", "max_wood_deck_sf"],
    ["min_open_porch_sf", "max_open_porch_sf"],
    ["min_enclosed_porch", "max_enclosed_porch"],
    ["min_3ssn_porch", "max_3ssn_porch"],
    ["min_screen_porch", "max_screen_porch"],
    ["min_pool_area", "max_pool_area"],
    ["min_sale_price", "max_sale_price"],
    /* TotalSF pares internos */
    ["totalSF_min_1st", "totalSF_max_1st"],
    ["totalSF_min_2nd", "totalSF_max_2nd"],
    ["totalSF_min_bsmt", "totalSF_max_bsmt"],
  ];

  const onSel = (key) => (e) => setForm((p) => ({ ...p, [key]: e.target.value }));
  const onBool = (key) => (v) => setForm((p) => ({ ...p, [key]: v }));

  const sanitize = (value, isInt = false) => {
    if (value === "" || value == null) return null;
    const num = isInt ? parseInt(value, 10) : parseFloat(value);
    return Number.isFinite(num) ? num : null;
  };

  /* TotalSF derivado */
  const sum3 = (a, b, c) => {
    const na = a === "" ? null : parseFloat(a);
    const nb = b === "" ? null : parseFloat(b);
    const nc = c === "" ? null : parseFloat(c);
    if (na == null || nb == null || nc == null) return null;
    return na + nb + nc;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    for (const [minK, maxK] of pairs) {
      const minV = form[minK];
      const maxV = form[maxK];
      if (minV !== "" && maxV !== "" && parseFloat(minV) > parseFloat(maxV)) {
        setGlobalError("Revisa los rangos: hay campos con Min > Max.");
        return;
      }
    }
    setGlobalError("");

    const min_total_sf_calc = sum3(form.totalSF_min_1st, form.totalSF_min_2nd, form.totalSF_min_bsmt);
    const max_total_sf_calc = sum3(form.totalSF_max_1st, form.totalSF_max_2nd, form.totalSF_max_bsmt);

    const payload = {
      // Ubicación y zona
      preferred_neighborhood: form.preferred_neighborhood || null,
      preferred_ms_zoning: form.preferred_ms_zoning || null,
      preferred_lot_shape: form.preferred_lot_shape || null,
      preferred_land_contour: form.preferred_land_contour || null,
      preferred_lot_config: form.preferred_lot_config || null,
      preferred_condition1: form.preferred_condition1 || null,

      // Tipo de casa
      preferred_bldg_type: form.preferred_bldg_type || null,
      preferred_house_style: form.preferred_house_style || null,
      preferred_roof_style: form.preferred_roof_style || null,
      preferred_exterior1st: form.preferred_exterior1st || null,
      preferred_exterior2nd: form.preferred_exterior2nd || null,
      preferred_foundation: form.preferred_foundation || null,

      // Calidad y condición
      min_overall_qual: sanitize(form.min_overall_qual),
      max_overall_qual: sanitize(form.max_overall_qual),
      min_overall_cond: sanitize(form.min_overall_cond),
      max_overall_cond: sanitize(form.max_overall_cond),
      min_exter_qual: form.min_exter_qual || null,
      min_exter_cond: form.min_exter_cond || null,

      // Años
      min_year_built: sanitize(form.min_year_built, true),
      max_year_built: sanitize(form.max_year_built, true),
      min_year_remod_add: sanitize(form.min_year_remod_add, true),
      max_year_remod_add: sanitize(form.max_year_remod_add, true),

      // Tamaños / áreas
      min_lot_area: sanitize(form.min_lot_area),
      max_lot_area: sanitize(form.max_lot_area),
      min_lot_frontage: sanitize(form.min_lot_frontage),
      max_lot_frontage: sanitize(form.max_lot_frontage),
      min_gr_liv_area: sanitize(form.min_gr_liv_area),
      max_gr_liv_area: sanitize(form.max_gr_liv_area),
      min_total_bsmt_sf: sanitize(form.min_total_bsmt_sf),
      max_total_bsmt_sf: sanitize(form.max_total_bsmt_sf),

      // Habitaciones y baños
      min_bedroom_abv_gr: sanitize(form.min_bedroom_abv_gr, true),
      max_bedroom_abv_gr: sanitize(form.max_bedroom_abv_gr, true),
      min_kitchen_abv_gr: sanitize(form.min_kitchen_abv_gr, true),
      max_kitchen_abv_gr: sanitize(form.max_kitchen_abv_gr, true),
      min_tot_rms_abv_grd: sanitize(form.min_tot_rms_abv_grd, true),
      max_tot_rms_abv_grd: sanitize(form.max_tot_rms_abv_grd, true),
      min_full_bath: sanitize(form.min_full_bath, true),
      max_full_bath: sanitize(form.max_full_bath, true),
      min_half_bath: sanitize(form.min_half_bath, true),
      max_half_bath: sanitize(form.max_half_bath, true),
      min_bsmt_full_bath: sanitize(form.min_bsmt_full_bath, true),
      max_bsmt_full_bath: sanitize(form.max_bsmt_full_bath, true),
      min_bsmt_half_bath: sanitize(form.min_bsmt_half_bath, true),
      max_bsmt_half_bath: sanitize(form.max_bsmt_half_bath, true),

      // Sótano
      preferred_bsmt_qual: form.preferred_bsmt_qual || null,
      preferred_bsmt_cond: form.preferred_bsmt_cond || null,
      preferred_bsmt_exposure: form.preferred_bsmt_exposure || null,
      preferred_bsmt_fin_type1: form.preferred_bsmt_fin_type1 || null,
      preferred_bsmt_fin_type2: form.preferred_bsmt_fin_type2 || null,
      min_bsmt_fin_sf1: sanitize(form.min_bsmt_fin_sf1),
      max_bsmt_fin_sf1: sanitize(form.max_bsmt_fin_sf1),
      min_bsmt_fin_sf2: sanitize(form.min_bsmt_fin_sf2),
      max_bsmt_fin_sf2: sanitize(form.max_bsmt_fin_sf2),
      min_bsmt_unf_sf: sanitize(form.min_bsmt_unf_sf),
      max_bsmt_unf_sf: sanitize(form.max_bsmt_unf_sf),

      // Calefacción y A/A
      preferred_heating_qc: form.preferred_heating_qc || null,
      central_air_required:
        form.central_air_required === "" ? null : Boolean(form.central_air_required),
      preferred_electrical: form.preferred_electrical || null,

      // Cocina
      min_kitchen_qual: form.min_kitchen_qual || null,

      // Funcionalidad
      preferred_functional: form.preferred_functional || null,

      // Chimeneas
      min_fireplaces: sanitize(form.min_fireplaces, true),
      max_fireplaces: sanitize(form.max_fireplaces, true),
      preferred_fireplace_qu: form.preferred_fireplace_qu || null,

      // Garaje
      preferred_garage_type: form.preferred_garage_type || null,
      min_garage_yr_blt: sanitize(form.min_garage_yr_blt, true),
      max_garage_yr_blt: sanitize(form.max_garage_yr_blt, true),
      preferred_garage_finish: form.preferred_garage_finish || null,
      min_garage_cars: sanitize(form.min_garage_cars, true),
      max_garage_cars: sanitize(form.max_garage_cars, true),
      min_garage_area: sanitize(form.min_garage_area),
      max_garage_area: sanitize(form.max_garage_area),
      preferred_garage_qual: form.preferred_garage_qual || null,
      preferred_garage_cond: form.preferred_garage_cond || null,
      preferred_paved_drive: form.preferred_paved_drive || null,

      // Porches / exteriores
      min_wood_deck_sf: sanitize(form.min_wood_deck_sf),
      max_wood_deck_sf: sanitize(form.max_wood_deck_sf),
      min_open_porch_sf: sanitize(form.min_open_porch_sf),
      max_open_porch_sf: sanitize(form.max_open_porch_sf),
      min_enclosed_porch: sanitize(form.min_enclosed_porch),
      max_enclosed_porch: sanitize(form.max_enclosed_porch),
      min_3ssn_porch: sanitize(form.min_3ssn_porch),
      max_3ssn_porch: sanitize(form.max_3ssn_porch),
      min_screen_porch: sanitize(form.min_screen_porch),
      max_screen_porch: sanitize(form.max_screen_porch),

      // Piscina
      min_pool_area: sanitize(form.min_pool_area),
      max_pool_area: sanitize(form.max_pool_area),
      preferred_pool_qc: form.preferred_pool_qc || null,

      // Cercas y misceláneos
      preferred_fence: form.preferred_fence || null,
      preferred_misc_feature: form.preferred_misc_feature || null,

      // Precio
      min_sale_price: sanitize(form.min_sale_price),
      max_sale_price: sanitize(form.max_sale_price),

      // Tipo/condición de venta
      preferred_sale_type: form.preferred_sale_type || null,
      preferred_sale_condition: form.preferred_sale_condition || null,

      /* Derivados: TotalSF (FLOAT) */
      min_total_sf: min_total_sf_calc,
      max_total_sf: max_total_sf_calc,
    };

    console.log("Client preferences payload:", payload);
    alert("¡Preferencias guardadas localmente! (revisa la consola)");
  };

  const handleReset = () => {
    setForm((prev) => Object.fromEntries(Object.keys(prev).map((k) => [k, ""])));
    setGlobalError("");
  };

  return (
    <div className="pref-page">
      <div className="pref-container">
        <h1 className="pref-title">Preferencias del comprador</h1>
        <p className="pref-subtitle">
          Selecciona tus preferencias y define rangos mínimos y máximos.
        </p>

        <form className="pref-form" onSubmit={handleSubmit}>
          {/* Ubicación & Zona */}
          <section className="pref-section">
            <h2 className="section-title">Ubicación & Zona</h2>
            <div className="grid-2">
              <div className="field">
                <label>Barrio (Neighborhood)</label>
                <select className="input" value={form.preferred_neighborhood} onChange={onSel("preferred_neighborhood")}>
                  <Options values={C.Neighborhood} placeholder="Selecciona barrio" />
                </select>
              </div>
              <div className="field">
                <label>MS Zoning</label>
                <select className="input" value={form.preferred_ms_zoning} onChange={onSel("preferred_ms_zoning")}>
                  <Options values={C.MSZoning} placeholder="Selecciona MS Zoning" />
                </select>
              </div>
              <div className="field">
                <label>Lot Shape</label>
                <select className="input" value={form.preferred_lot_shape} onChange={onSel("preferred_lot_shape")}>
                  <Options values={C.LotShape} placeholder="Selecciona Lot Shape" />
                </select>
              </div>
              <div className="field">
                <label>Land Contour</label>
                <select className="input" value={form.preferred_land_contour} onChange={onSel("preferred_land_contour")}>
                  <Options values={C.LandContour} placeholder="Selecciona Land Contour" />
                </select>
              </div>
              <div className="field">
                <label>Lot Config</label>
                <select className="input" value={form.preferred_lot_config} onChange={onSel("preferred_lot_config")}>
                  <Options values={C.LotConfig} placeholder="Selecciona Lot Config" />
                </select>
              </div>
              <div className="field">
                <label>Condition1</label>
                <select className="input" value={form.preferred_condition1} onChange={onSel("preferred_condition1")}>
                  <Options values={C.Condition1} placeholder="Selecciona Condition1" />
                </select>
              </div>
            </div>
          </section>

          {/* Tipo de casa */}
          <section className="pref-section">
            <h2 className="section-title">Tipo de casa</h2>
            <div className="grid-2">
              <div className="field">
                <label>BldgType</label>
                <select className="input" value={form.preferred_bldg_type} onChange={onSel("preferred_bldg_type")}>
                  <Options values={C.BldgType} placeholder="Selecciona BldgType" />
                </select>
              </div>
              <div className="field">
                <label>HouseStyle</label>
                <select className="input" value={form.preferred_house_style} onChange={onSel("preferred_house_style")}>
                  <Options values={C.HouseStyle} placeholder="Selecciona HouseStyle" />
                </select>
              </div>
              <div className="field">
                <label>RoofStyle</label>
                <select className="input" value={form.preferred_roof_style} onChange={onSel("preferred_roof_style")}>
                  <Options values={C.RoofStyle} placeholder="Selecciona RoofStyle" />
                </select>
              </div>
              <div className="field">
                <label>Exterior1st</label>
                <select className="input" value={form.preferred_exterior1st} onChange={onSel("preferred_exterior1st")}>
                  <Options values={C.Exterior1st} placeholder="Selecciona Exterior1st" />
                </select>
              </div>
              <div className="field">
                <label>Exterior2nd</label>
                <select className="input" value={form.preferred_exterior2nd} onChange={onSel("preferred_exterior2nd")}>
                  <Options values={C.Exterior2nd} placeholder="Selecciona Exterior2nd" />
                </select>
              </div>
              <div className="field">
                <label>Foundation</label>
                <select className="input" value={form.preferred_foundation} onChange={onSel("preferred_foundation")}>
                  <Options values={C.Foundation} placeholder="Selecciona Foundation" />
                </select>
              </div>
            </div>
          </section>

          {/* Calidad / condición */}
          <section className="pref-section">
            <h2 className="section-title">Calidad & Condición</h2>
            <div className="grid-2">
              <NumberRange label="OverallQual" minKey="min_overall_qual" maxKey="max_overall_qual" state={form} setState={setForm} />
              <NumberRange label="OverallCond" minKey="min_overall_cond" maxKey="max_overall_cond" state={form} setState={setForm} />
              <div className="field">
                <label>Umbral ExterQual (mín.)</label>
                <select className="input" value={form.min_exter_qual} onChange={onSel("min_exter_qual")}>
                  <Options values={C.ExterQual} placeholder="(cualquiera)" />
                </select>
              </div>
              <div className="field">
                <label>Umbral ExterCond (mín.)</label>
                <select className="input" value={form.min_exter_cond} onChange={onSel("min_exter_cond")}>
                  <Options values={C.ExterCond} placeholder="(cualquiera)" />
                </select>
              </div>
            </div>
          </section>

          {/* Años */}
          <section className="pref-section">
            <h2 className="section-title">Años</h2>
            <div className="grid-2">
              <NumberRange label="YearBuilt" minKey="min_year_built" maxKey="max_year_built" state={form} setState={setForm} step="1" />
              <NumberRange label="YearRemodAdd" minKey="min_year_remod_add" maxKey="max_year_remod_add" state={form} setState={setForm} step="1" />
            </div>
          </section>

          {/* Tamaños & Áreas */}
          <section className="pref-section">
            <h2 className="section-title">Tamaños & Áreas (ft²)</h2>
            <div className="grid-2">
              <NumberRange label="LotArea" minKey="min_lot_area" maxKey="max_lot_area" state={form} setState={setForm} />
              <NumberRange label="LotFrontage (ft)" minKey="min_lot_frontage" maxKey="max_lot_frontage" state={form} setState={setForm} />
              <NumberRange label="GrLivArea" minKey="min_gr_liv_area" maxKey="max_gr_liv_area" state={form} setState={setForm} />
              <NumberRange label="TotalBsmtSF" minKey="min_total_bsmt_sf" maxKey="max_total_bsmt_sf" state={form} setState={setForm} />
            </div>
          </section>

          {/* Derivado: TotalSF */}
          <section className="pref-section">
            <h2 className="section-title">Superficie total (TotalSF)</h2>
            <p className="field-hint">
              TotalSF = 1stFlrSF + 2ndFlrSF + TotalBsmtSF. Aquí ingresas los tres componentes y nosotros calculamos y enviamos solo TotalSF.
            </p>
            <div className="grid-2">
              <NumberRange label="1stFlrSF" minKey="totalSF_min_1st" maxKey="totalSF_max_1st" state={form} setState={setForm} />
              <NumberRange label="2ndFlrSF" minKey="totalSF_min_2nd" maxKey="totalSF_max_2nd" state={form} setState={setForm} />
              <NumberRange label="TotalBsmtSF" minKey="totalSF_min_bsmt" maxKey="totalSF_max_bsmt" state={form} setState={setForm} />
            </div>
          </section>

          {/* Habitaciones y baños */}
          <section className="pref-section">
            <h2 className="section-title">Habitaciones & Baños</h2>
            <div className="grid-2">
              <NumberRange label="Bedrooms (abv gr)" minKey="min_bedroom_abv_gr" maxKey="max_bedroom_abv_gr" state={form} setState={setForm} step="1" />
              <NumberRange label="Kitchens" minKey="min_kitchen_abv_gr" maxKey="max_kitchen_abv_gr" state={form} setState={setForm} step="1" />
              <NumberRange label="Total rooms (abv grd)" minKey="min_tot_rms_abv_grd" maxKey="max_tot_rms_abv_grd" state={form} setState={setForm} step="1" />
              <NumberRange label="Full baths" minKey="min_full_bath" maxKey="max_full_bath" state={form} setState={setForm} step="1" />
              <NumberRange label="Half baths" minKey="min_half_bath" maxKey="max_half_bath" state={form} setState={setForm} step="1" />
              <NumberRange label="Bsmt full bath" minKey="min_bsmt_full_bath" maxKey="max_bsmt_full_bath" state={form} setState={setForm} step="1" />
              <NumberRange label="Bsmt half bath" minKey="min_bsmt_half_bath" maxKey="max_bsmt_half_bath" state={form} setState={setForm} step="1" />
            </div>
          </section>

          {/* Sótano */}
          <section className="pref-section">
            <h2 className="section-title">Sótano</h2>
            <div className="grid-2">
              <div className="field">
                <label>BsmtQual</label>
                <select className="input" value={form.preferred_bsmt_qual} onChange={onSel("preferred_bsmt_qual")}>
                  <Options values={C.BsmtQual} placeholder="(cualquiera)" />
                </select>
              </div>
              <div className="field">
                <label>BsmtCond</label>
                <select className="input" value={form.preferred_bsmt_cond} onChange={onSel("preferred_bsmt_cond")}>
                  <Options values={C.BsmtCond} placeholder="(cualquiera)" />
                </select>
              </div>
              <div className="field">
                <label>BsmtExposure</label>
                <select className="input" value={form.preferred_bsmt_exposure} onChange={onSel("preferred_bsmt_exposure")}>
                  <Options values={C.BsmtExposure} placeholder="(cualquiera)" />
                </select>
              </div>
              <div className="field">
                <label>BsmtFinType1</label>
                <select className="input" value={form.preferred_bsmt_fin_type1} onChange={onSel("preferred_bsmt_fin_type1")}>
                  <Options values={C.BsmtFinType1} placeholder="(cualquiera)" />
                </select>
              </div>
              <div className="field">
                <label>BsmtFinType2</label>
                <select className="input" value={form.preferred_bsmt_fin_type2} onChange={onSel("preferred_bsmt_fin_type2")}>
                  <Options values={C.BsmtFinType2} placeholder="(cualquiera)" />
                </select>
              </div>
              <NumberRange label="BsmtFinSF1" minKey="min_bsmt_fin_sf1" maxKey="max_bsmt_fin_sf1" state={form} setState={setForm} />
              <NumberRange label="BsmtFinSF2" minKey="min_bsmt_fin_sf2" maxKey="max_bsmt_fin_sf2" state={form} setState={setForm} />
              <NumberRange label="BsmtUnfSF" minKey="min_bsmt_unf_sf" maxKey="max_bsmt_unf_sf" state={form} setState={setForm} />
            </div>
          </section>

          {/* Calefacción / A/A & eléctricos */}
          <section className="pref-section">
            <h2 className="section-title">Calefacción, A/A & Eléctrico</h2>
            <div className="grid-2">
              <div className="field">
                <label>HeatingQC</label>
                <select className="input" value={form.preferred_heating_qc} onChange={onSel("preferred_heating_qc")}>
                  <Options values={C.HeatingQC} placeholder="(cualquiera)" />
                </select>
              </div>
              <YesNo label="¿Requiere aire acondicionado central?" value={form.central_air_required === "" ? "" : form.central_air_required} onChange={onBool("central_air_required")} />
              <div className="field">
                <label>Electrical</label>
                <select className="input" value={form.preferred_electrical} onChange={onSel("preferred_electrical")}>
                  <Options values={C.Electrical} placeholder="(cualquiera)" />
                </select>
              </div>
            </div>
          </section>

          {/* Cocina, funcionalidad, chimeneas */}
          <section className="pref-section">
            <h2 className="section-title">Cocina, Funcionalidad & Chimeneas</h2>
            <div className="grid-2">
              <div className="field">
                <label>Umbral KitchenQual (mín.)</label>
                <select className="input" value={form.min_kitchen_qual} onChange={onSel("min_kitchen_qual")}>
                  <Options values={C.KitchenQual} placeholder="(cualquiera)" />
                </select>
              </div>
              <div className="field">
                <label>Functional</label>
                <select className="input" value={form.preferred_functional} onChange={onSel("preferred_functional")}>
                  <Options values={C.Functional} placeholder="(cualquiera)" />
                </select>
              </div>
              <NumberRange label="Fireplaces" minKey="min_fireplaces" maxKey="max_fireplaces" state={form} setState={setForm} step="1" />
              <div className="field">
                <label>FireplaceQu</label>
                <select className="input" value={form.preferred_fireplace_qu} onChange={onSel("preferred_fireplace_qu")}>
                  <Options values={C.FireplaceQu} placeholder="(cualquiera)" />
                </select>
              </div>
            </div>
          </section>

          {/* Garaje */}
          <section className="pref-section">
            <h2 className="section-title">Garaje</h2>
            <div className="grid-2">
              <div className="field">
                <label>GarageType</label>
                <select className="input" value={form.preferred_garage_type} onChange={onSel("preferred_garage_type")}>
                  <Options values={C.GarageType} placeholder="(cualquiera)" />
                </select>
              </div>
              <NumberRange label="GarageYrBlt" minKey="min_garage_yr_blt" maxKey="max_garage_yr_blt" state={form} setState={setForm} step="1" />
              <div className="field">
                <label>GarageFinish</label>
                <select className="input" value={form.preferred_garage_finish} onChange={onSel("preferred_garage_finish")}>
                  <Options values={C.GarageFinish} placeholder="(cualquiera)" />
                </select>
              </div>
              <NumberRange label="GarageCars" minKey="min_garage_cars" maxKey="max_garage_cars" state={form} setState={setForm} step="1" />
              <NumberRange label="GarageArea" minKey="min_garage_area" maxKey="max_garage_area" state={form} setState={setForm} />
              <div className="field">
                <label>GarageQual</label>
                <select className="input" value={form.preferred_garage_qual} onChange={onSel("preferred_garage_qual")}>
                  <Options values={C.GarageQual} placeholder="(cualquiera)" />
                </select>
              </div>
              <div className="field">
                <label>GarageCond</label>
                <select className="input" value={form.preferred_garage_cond} onChange={onSel("preferred_garage_cond")}>
                  <Options values={C.GarageCond} placeholder="(cualquiera)" />
                </select>
              </div>
              <div className="field">
                <label>PavedDrive</label>
                <select className="input" value={form.preferred_paved_drive} onChange={onSel("preferred_paved_drive")}>
                  <Options values={C.PavedDrive} placeholder="(cualquiera)" />
                </select>
              </div>
            </div>
          </section>

          {/* Porches / exteriores */}
          <section className="pref-section">
            <h2 className="section-title">Porches & Exteriores</h2>
            <div className="grid-2">
              <NumberRange label="WoodDeckSF" minKey="min_wood_deck_sf" maxKey="max_wood_deck_sf" state={form} setState={setForm} />
              <NumberRange label="OpenPorchSF" minKey="min_open_porch_sf" maxKey="max_open_porch_sf" state={form} setState={setForm} />
              <NumberRange label="EnclosedPorch" minKey="min_enclosed_porch" maxKey="max_enclosed_porch" state={form} setState={setForm} />
              <NumberRange label="3SsnPorch" minKey="min_3ssn_porch" maxKey="max_3ssn_porch" state={form} setState={setForm} />
              <NumberRange label="ScreenPorch" minKey="min_screen_porch" maxKey="max_screen_porch" state={form} setState={setForm} />
            </div>
          </section>

          {/* Piscina / misceláneos */}
          <section className="pref-section">
            <h2 className="section-title">Piscina & Misceláneos</h2>
            <div className="grid-2">
              <NumberRange label="PoolArea" minKey="min_pool_area" maxKey="max_pool_area" state={form} setState={setForm} />
              <div className="field">
                <label>PoolQC</label>
                <select className="input" value={form.preferred_pool_qc} onChange={onSel("preferred_pool_qc")}>
                  <Options values={C.PoolQC} placeholder="(cualquiera)" />
                </select>
              </div>
              <div className="field">
                <label>Fence</label>
                <select className="input" value={form.preferred_fence} onChange={onSel("preferred_fence")}>
                  <Options values={C.Fence} placeholder="(cualquiera)" />
                </select>
              </div>
              <div className="field">
                <label>MiscFeature</label>
                <select className="input" value={form.preferred_misc_feature} onChange={onSel("preferred_misc_feature")}>
                  <Options values={C.MiscFeature} placeholder="(cualquiera)" />
                </select>
              </div>
            </div>
          </section>

          {/* Precio y venta */}
          <section className="pref-section">
            <h2 className="section-title">Precio & Venta</h2>
            <div className="grid-2">
              <NumberRange label="SalePrice ($)" minKey="min_sale_price" maxKey="max_sale_price" state={form} setState={setForm} />
              <div className="field">
                <label>SaleType</label>
                <select className="input" value={form.preferred_sale_type} onChange={onSel("preferred_sale_type")}>
                  <Options values={C.SaleType} placeholder="(cualquiera)" />
                </select>
              </div>
              <div className="field">
                <label>SaleCondition</label>
                <select className="input" value={form.preferred_sale_condition} onChange={onSel("preferred_sale_condition")}>
                  <Options values={C.SaleCondition} placeholder="(cualquiera)" />
                </select>
              </div>
            </div>
          </section>

          {globalError && <div className="global-error">{globalError}</div>}

          <div className="form-actions">
            <button type="button" className="btn ghost" onClick={handleReset}>
              Limpiar
            </button>
            <button type="submit" className="btn primary">
              Guardar preferencias
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
