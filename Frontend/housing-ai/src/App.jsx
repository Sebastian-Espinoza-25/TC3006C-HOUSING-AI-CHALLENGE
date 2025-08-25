import "./styles/Styles.css";
import "./App.css";
import Navbar from "./Components/header/Navbar";
import AppRoutes from "./Components/routes/AppRoutes";

function App() {
  return (
    <>
      <Navbar />
      <div className="container">
      <AppRoutes />
      </div>
    </>
  );
}

export default App;
