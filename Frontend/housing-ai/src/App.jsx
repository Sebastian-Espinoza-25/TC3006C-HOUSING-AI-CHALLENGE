import "./styles/Styles.css";
import "./App.css";
import Navbar from "./Components/header/Navbar";
import AppRoutes from "./Components/routes/AppRoutes.js";
import Footer from "./Components/footer/Footer";

export default function App() {
  return (
    <div className="app-layout">
      <Navbar />
      <div className="container">
        <AppRoutes />
      </div>
      <Footer />
    </div>
  );
}

