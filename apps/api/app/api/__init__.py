from app.api.auth import router as auth_router
from app.api.sites import router as sites_router
from app.api.pages import router as pages_router
from app.api.public import router as public_router

__all__ = ["auth_router", "sites_router", "pages_router", "public_router"]
