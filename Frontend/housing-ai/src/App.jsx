import "./styles/Styles.css";
import "./App.css";
import Navbar from "./Components/header/Navbar";
import AppRoutes from "./Components/routes/AppRoutes.js";
import Footer from "./Components/footer/Footer";
import ScrollToTop from "./Components/common/ScrollToTop";

export default function App() {
  return (
    <div className="app-layout">
      <Navbar />
      <ScrollToTop />
      <main className="app-main">
        <div className="container">
          <AppRoutes />
        </div>
      </main>
      <Footer />
    </div>
  );
}

