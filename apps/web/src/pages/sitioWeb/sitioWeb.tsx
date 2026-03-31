import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../../components/sidebar/sidebar";
import { authService, sitesService } from "../../services";
import type { Site } from "../../types";
import "./sitioWeb.css";

function sitioWeb() {
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);
  const [sites, setSites] = useState<Site[]>([]);
  const [loading, setLoading] = useState(true);
  const [newSite, setNewSite] = useState({ name: "", slug: "" });
  const [error, setError] = useState("");
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }
    loadData();
  }, [navigate]);

  const loadData = async () => {
    try {
      const userData = await authService.getMe();
      setUser(userData);
      const sitesData = await sitesService.getAll();
      setSites(sitesData);
    } catch (err) {
      console.error("Error loading data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateSite = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setCreating(true);

    try {
      const created = await sitesService.create(newSite);
      setSites([...sites, created]);
      setNewSite({ name: "", slug: "" });
    } catch (err: any) {
      setError(err.response?.data?.detail || "Error al crear site");
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteSite = async (id: number) => {
    if (!confirm("¿Estás seguro de eliminar este site?")) return;

    try {
      await sitesService.delete(id);
      setSites(sites.filter((s) => s.id !== id));
    } catch (err) {
      console.error("Error deleting site:", err);
    }
  };

  const generateSlug = (name: string) => {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/(^-|-$)/g, "");
  };

  if (loading) {
    return <div className="loading">Cargando...</div>;
  }

  return (
    <div className="sitioWeb-container">
      <Sidebar />
      <div className="main-content">
        <div className="sitioWeb-header">
          <div>
            <h1>Bienvenido, {user?.first_name}</h1>
            <p className="user-email">{user?.email}</p>
          </div>
        </div>

        <div className="create-site-form">
          <h3>+ Crear Nuevo Site</h3>
          {error && <div className="error-message">{error}</div>}
          <form className="form-inline" onSubmit={handleCreateSite}>
            <div className="form-group">
              <label htmlFor="site-name">Nombre</label>
              <input
                id="site-name"
                type="text"
                value={newSite.name}
                onChange={(e) =>
                  setNewSite({
                    name: e.target.value,
                    slug: generateSlug(e.target.value),
                  })
                }
                placeholder="Mi Sitio Web"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="site-slug">Subdominio</label>
              <div className="input-group">
                <input
                  id="site-slug"
                  type="text"
                  value={newSite.slug}
                  onChange={(e) =>
                    setNewSite({
                      ...newSite,
                      slug: generateSlug(e.target.value),
                    })
                  }
                  placeholder="mi-sitio"
                  pattern="^[a-z0-9-]+$"
                  required
                />
                <span className="input-addon">.localtest.me</span>
              </div>
            </div>
            <button type="submit" className="btn-primary" disabled={creating}>
              {creating ? "Creando..." : "Crear"}
            </button>
          </form>
        </div>

        <div className="sites-section">
          <h2>Mis Sites ({sites.length})</h2>
          {sites.length === 0 ? (
            <div className="empty-state">
              <p>No tienes sites creados aún.</p>
              <p className="hint">
                Usa el formulario de arriba para crear tu primer sitio
              </p>
            </div>
          ) : (
            <div className="sites-grid">
              {sites.map((site) => (
                <div key={site.id} className="site-card">
                  <div className="site-info">
                    <h3>{site.name}</h3>
                    <span className="site-slug">{site.slug}.localtest.me</span>
                  </div>
                  <div className="site-actions">
                    <a
                      href={`http://localhost:8000/${site.slug}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn-icon"
                      title="Ver sitio"
                    >
                      🌐
                    </a>
                    <button
                      className="btn-icon btn-danger"
                      title="Eliminar"
                      onClick={() => handleDeleteSite(site.id)}
                    >
                      🗑
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default sitioWeb;
