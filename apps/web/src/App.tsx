import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";
import Login from "./components/login/login";
import Register from "./components/register/register";
import Dashboard from "./pages/dashboard/dashboard";
import SitioWeb from "./pages/sitioWeb/sitioWeb";
import Modulos from "./pages/modulos/modulos";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/sitioWeb" element={<SitioWeb />} />
        <Route path="/modulos" element={<Modulos />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
