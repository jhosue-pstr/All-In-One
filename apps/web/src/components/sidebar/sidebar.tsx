import "./sidebar.css";
import { authService, sitesService } from "../../services";
import { useNavigate } from "react-router-dom";

function Sidebar() {
  const navigate = useNavigate();
  const handleLogout = () => {
    authService.logout();
    navigate("/login");
  };

  return (
    <div className="sidebar">
      <div className="logo-container">
        <img src="" alt="Logo" />
        <h2>All In One</h2>
      </div>

      <div className="divider"></div>

      <ul className="nav-menu">
        <li className="active" onClick={() => navigate("/Dashboard")}>
          <span className="icon">🏠</span>
          Inicio
        </li>
        <li onClick={() => navigate("/sitioWeb")}>
          <span className="icon">🌐</span>
          Sitio Web
        </li>
        <li onClick={() => navigate("/modulos")}>
          <span className="icon">📦</span>
          Módulos
        </li>
        <li>
          <span className="icon">⚙️</span>
          Configuración
        </li>
      </ul>

      <div className="divider"></div>

      <ul className="nav-menu logout-section">
        <li onClick={handleLogout}>
          <span className="icon">🚪</span>
          Cerrar Sesión
        </li>
      </ul>
    </div>
  );
}

export default Sidebar;
