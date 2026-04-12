from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    # Prueba la ruta principal
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "CMS API funcionando", "version": "1.0.0"}

def test_docs_exist():
    # Prueba que la documentación Swagger de FastAPI cargue bien
    response = client.get("/docs")
    assert response.status_code == 200

def test_openapi_schema_exists():
    # Prueba que el esquema de rutas se genere correctamente
    response = client.get("/openapi.json")
    assert response.status_code == 200
