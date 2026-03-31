import Sidebar from "../../components/sidebar/sidebar";
import "./modulos.css";

function Modulos() {
  return (
    <div className="dashboard-container">
      <Sidebar />
      <div className="main-content">
        <h1>Modulos</h1>
        <p>Gestiona los Modulos desde aqui</p>
      </div>
    </div>
  );
}

export default Modulos;
