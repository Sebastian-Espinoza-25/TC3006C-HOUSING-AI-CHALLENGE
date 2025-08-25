import { Routes, Route } from "react-router-dom";
import LandingPage from "../../pages/LandingPage";
import SearchHouse from "../../pages/SearchHouse";
import Sell from "../../pages/Sell";
import HowItWorks from "../../pages/HowItWorks";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/search" element={<SearchHouse />} />
      <Route path="/sell" element={<Sell />} />
      <Route path="/how-it-works" element={<HowItWorks />} />
    </Routes>
  );
}
