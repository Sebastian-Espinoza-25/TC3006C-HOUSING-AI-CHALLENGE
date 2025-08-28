import { Routes, Route } from "react-router-dom";
import LandingPage from "../../pages/LandingPage";
import SearchHouse from "../../pages/SearchHouse";
import Sell from "../../pages/Sell";
import HowItWorks from "../../pages/HowItWorks";
import Login from "../../pages/Login";
import About from "../../pages/About";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/search" element={<SearchHouse />} />
      <Route path="/sell" element={<Sell />} />
      <Route path="/how-it-works" element={<HowItWorks />} />
      <Route path="/login" element={<Login />} />
      <Route path="/about" element={<About/>} />
    </Routes>
  );
}
