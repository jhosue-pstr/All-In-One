import sys
import os
sys.path.insert(0, "/app")
sys.path.insert(0, "/app/packages")

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from packages.core.models.site import Site
from packages.core.models.page import Page

router = APIRouter(tags=["public"])


def extract_subdomain(host: str) -> str | None:
    if not host:
        return None
    
    parts = host.split(".")
    
    if len(parts) >= 2:
        if parts[-1] in ["localtest", "me"] and len(parts) >= 3:
            return parts[0]
        
        if parts[-2:] == ["127", "0", "0", "1"]:
            return parts[0]
        
        if "nip" in host and ".nip.io" in host:
            return parts[0]
    
    if len(parts) >= 2:
        return parts[0]
    
    return None


@router.get("/{slug}")
async def get_site_home(
    request: Request,
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Site).where(Site.slug == slug))
    site = result.scalar_one_or_none()
    
    if not site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    
    page_result = await db.execute(
        select(Page).where(Page.site_id == site.id, Page.is_home == True, Page.is_published == True)
    )
    page = page_result.scalar_one_or_none()
    
    if not page:
        page_result = await db.execute(
            select(Page).where(Page.site_id == site.id, Page.is_published == True).limit(1)
        )
        page = page_result.scalar_one_or_none()
    
    if not page:
        return HTMLResponse(
            content=f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{site.name}</title>
                <style>
                    body {{
                        font-family: system-ui, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        margin: 0;
                        background: #f5f5f5;
                    }}
                    .container {{
                        text-align: center;
                        padding: 2rem;
                        background: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    h1 {{ color: #333; }}
                    p {{ color: #666; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>{site.name}</h1>
                    <p>Este sitio aún no tiene contenido publicado.</p>
                </div>
            </body>
            </html>
            """,
            status_code=200
        )
    
    html_content = page.gjs_html or page.content or f"<h1>{page.title}</h1>"
    
    css = page.gjs_css or ""
    
    return HTMLResponse(
        content=f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{page.meta_title or page.title} - {site.name}</title>
            <meta name="description" content="{page.meta_description or ''}">
            <style>{css}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """,
        status_code=200
    )


@router.get("/{slug}/api/info")
async def get_site_info(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Site).where(Site.slug == slug))
    site = result.scalar_one_or_none()
    
    if not site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    
    return {
        "id": site.id,
        "name": site.name,
        "slug": site.slug
    }


@router.get("/{slug}/{page_slug}")
async def get_page_by_slug(
    request: Request,
    slug: str,
    page_slug: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Site).where(Site.slug == slug))
    site = result.scalar_one_or_none()
    
    if not site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")
    
    page_result = await db.execute(
        select(Page).where(
            Page.site_id == site.id,
            Page.slug == page_slug,
            Page.is_published == True
        )
    )
    page = page_result.scalar_one_or_none()
    
    if not page:
        raise HTTPException(status_code=404, detail="Página no encontrada")
    
    html_content = page.gjs_html or page.content or f"<h1>{page.title}</h1>"
    css = page.gjs_css or ""
    
    return HTMLResponse(
        content=f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{page.meta_title or page.title} - {site.name}</title>
            <meta name="description" content="{page.meta_description or ''}">
            <style>{css}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """,
        status_code=200
    )
