import { Routes, Route } from "react-router-dom";
import LandingPage from "../../pages/LandingPage";
import SearchHouse from "../../pages/SearchHouse";
import Sell from "../../pages/Sell";
import HowItWorks from "../../pages/HowItWorks";
import Login from "../../pages/Login";
import Register from "../../pages/Register";
import About from "../../pages/About";
import RequireAuth from "../../guards/RequireAuth";
import Publish from "../../pages/seller/publish";
import Preferences from "../../pages/buyer/Preferences";

export default function AppRoutes() {
  return (
    <Routes>
      {/* Públicas */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/how-it-works" element={<HowItWorks />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/about" element={<About />} />

      {/* Privadas */}
      <Route
        path="/search"
        element={
          <RequireAuth>
            <SearchHouse />
          </RequireAuth>
        }
      />
      <Route
        path="/sell"
        element={
          <RequireAuth>
            <Sell />
          </RequireAuth>
        }
      />
      <Route
        path="/sell/publish"
        element={
          <RequireAuth>
            <Publish />
          </RequireAuth>
        }
      />
      <Route
        path="/preferences"
        element={
          <RequireAuth>
            <Preferences />
          </RequireAuth>
        }
      />
    </Routes>
  );
}
