// src/Components/routes/AppRoutes.jsx
import { Routes, Route } from "react-router-dom";

import LandingPage from "../../pages/LandingPage";
import SearchHouse from "../../pages/SearchHouse";
import Sell from "../../pages/Sell";
import HowItWorks from "../../pages/HowItWorks";
import Login from "../../pages/Login";
import Register from "../../pages/Register";
import About from "../../pages/About";

import RequireAuth from "../../guards/RequireAuth";
import RoleGate from "../../guards/RoleGate";

import Preferences from "../../pages/buyer/Preferences";

import Publish from "../../pages/seller/publish"; // ← por ahora NO expongas publish

import Listings from "../../pages/seller/listings";


export default function AppRoutes() {
  return (
    <Routes>
      {/* Públicas */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/how-it-works" element={<HowItWorks />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/about" element={<About />} />

      {/* PRIVADAS: Buyer (client) */}
      <Route
        path="/search"
        element={
          <RequireAuth>
            <RoleGate allow={["client"]}>
              <SearchHouse />
            </RoleGate>
          </RequireAuth>
        }
      />
      <Route
        path="/preferences"
        element={
          <RequireAuth>
            <RoleGate allow={["client"]}>
              <Preferences />
            </RoleGate>
          </RequireAuth>
        }
      />

      {/* PRIVADAS: Vendor — por ahora SOLO sell */}
      <Route
        path="/sell"
        element={
          <RequireAuth>
            <RoleGate allow={["vendor"]}>
              <Sell />
            </RoleGate>
          </RequireAuth>
        }
      />
      <Route
        path="/sell/publish"
        element={
          <RequireAuth>
            <RoleGate allow={["vendor"]}>
              <Publish />
            </RoleGate>
          </RequireAuth>
        }
      />
      <Route
        path="/publish"
        path="/sell/listings"
        element={
          <RequireAuth>
            <Listings />
          </RequireAuth>
        }
      />
      {/* Ruta para preferencias del comprador */}
      <Route
        path="/preferences"
        element={
          <RequireAuth>
            <RoleGate allow={["vendor"]}>
              <Publish />
            </RoleGate>
          </RequireAuth>
        }
      />

      {/* Fallback */}
      <Route path="*" element={<LandingPage />} />
    </Routes>
  );
}
