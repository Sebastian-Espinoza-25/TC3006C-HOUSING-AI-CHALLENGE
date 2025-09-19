import { useState } from "react";
import { datasetMeta, quickDemoData } from "./publishData";

export default function Publish() {
  const [formType, setFormType] = useState(null); // "quick" | "long"
  const [formData, setFormData] = useState({});
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  // -------------------------
  // QUICK FORM CONFIG
  // -------------------------
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

  // -------------------------
  // HANDLERS
  // -------------------------
  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleDemo = () => {
    if (formType === "quick") {
      setFormData(quickDemoData);
      return;
    }

    // Demo largo: promedio de dataset
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

    let transformed;
    if (formType === "quick") {
      transformed = { ...formData }; // JSON reducido
    } else {
      transformed = { ...formData }; // JSON largo
    }

    console.log("🚀 Sending JSON:", transformed);

    try {
      setLoading(true);
      const response = await fetch(
        "http://127.0.0.1:5001/api/ai/predict/simple",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(transformed),
        }
      );

      if (!response.ok) throw new Error("Error fetching prediction");

      const data = await response.json();
      console.log("✅ Prediction result:", data);
      setPrediction(data);
    } catch (err) {
      console.error("❌ Error:", err);
      alert("Error sending data to prediction API.");
    } finally {
      setLoading(false);
    }
  };

  // -------------------------
  // FIELD RENDER
  // -------------------------
  const renderField = (field) => {
    const isNumeric = datasetMeta.numeric_means[field] !== undefined;

    // Categóricos
    if (!isNumeric && datasetMeta.categorical_uniques[field]) {
      return (
        <div key={field} style={{ marginBottom: "1rem" }}>
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

    // Numéricos
    return (
      <div key={field} style={{ marginBottom: "1rem" }}>
        <label>
          {field}:{" "}
          <input
            type="number"
            value={formData[field] ?? ""}
            onChange={(e) =>
              handleChange(field, parseFloat(e.target.value) || 0)
            }
          />
        </label>
      </div>
    );
  };

  // -------------------------
  // RENDER
  // -------------------------
  return (
    <div style={{ padding: "2rem" }}>
      <h1>Publish a New Listing</h1>

      {!formType && (
        <div style={{ display: "flex", gap: "1rem", marginTop: "2rem" }}>
          <button onClick={() => setFormType("quick")}>Quick Form</button>
          <button onClick={() => setFormType("long")}>Long Form</button>
        </div>
      )}

      {formType && (
        <form onSubmit={handleSubmit} style={{ marginTop: "2rem" }}>
          {/* DEMO BUTTON */}
          <button
            type="button"
            onClick={handleDemo}
            style={{ marginBottom: "1.5rem" }}
          >
            Demo
          </button>

          {(formType === "quick"
            ? quickFields
            : [
                ...Object.keys(datasetMeta.numeric_means),
                ...Object.keys(datasetMeta.categorical_uniques),
              ]
          ).map((f) => renderField(f))}

          <button type="submit" style={{ marginTop: "1.5rem" }}>
            {loading ? "Submitting..." : "Submit"}
          </button>
        </form>
      )}

      {prediction && (
        <div
          style={{
            marginTop: "2rem",
            padding: "1rem",
            background: "#f5f5f5",
            borderRadius: "8px",
          }}
        >
          <h2>Prediction Result:</h2>
          <pre>{JSON.stringify(prediction, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}