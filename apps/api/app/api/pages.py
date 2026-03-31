import sys
import os
sys.path.insert(0, "/app")
sys.path.insert(0, "/app/packages")

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.database import get_db
from packages.core.models.user import User
from packages.core.models.site import Site
from packages.core.models.page import Page
from packages.core.schemas.page import PageCreate, PageUpdate, PageResponse, PageListResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/pages", tags=["pages"])


@router.get("/site/{site_id}", response_model=List[PageListResponse])
async def list_pages(
    site_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Page).where(Page.site_id == site_id).order_by(Page.created_at.desc())
    )
    pages = result.scalars().all()
    return pages


@router.post("", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
async def create_page(
    page_data: PageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    site_result = await db.execute(
        select(Site).where(Site.id == page_data.site_id, Site.user_id == current_user.id)
    )
    site = site_result.scalar_one_or_none()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sitio no encontrado"
        )

    slug_result = await db.execute(
        select(Page).where(Page.site_id == page_data.site_id, Page.slug == page_data.slug)
    )
    if slug_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El slug ya está en uso en este sitio"
        )

    if page_data.is_home:
        await db.execute(
            select(Page).where(Page.site_id == page_data.site_id, Page.is_home == True)
        )
        home_pages = (await db.execute(
            select(Page).where(Page.site_id == page_data.site_id, Page.is_home == True)
        )).scalars().all()
        for hp in home_pages:
            hp.is_home = False

    page = Page(
        site_id=page_data.site_id,
        title=page_data.title,
        slug=page_data.slug,
        content=page_data.content,
        is_home=page_data.is_home,
        is_published=page_data.is_published,
        meta_title=page_data.meta_title,
        meta_description=page_data.meta_description,
    )
    db.add(page)
    await db.commit()
    await db.refresh(page)
    return page


@router.get("/{page_id}", response_model=PageResponse)
async def get_page(
    page_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Page).where(Page.id == page_id)
    )
    page = result.scalar_one_or_none()
    
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Página no encontrada"
        )
    
    site_result = await db.execute(
        select(Site).where(Site.id == page.site_id, Site.user_id == current_user.id)
    )
    if not site_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a esta página"
        )
    
    return page


@router.put("/{page_id}", response_model=PageResponse)
async def update_page(
    page_id: int,
    page_data: PageUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Page).where(Page.id == page_id))
    page = result.scalar_one_or_none()
    
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Página no encontrada"
        )
    
    site_result = await db.execute(
        select(Site).where(Site.id == page.site_id, Site.user_id == current_user.id)
    )
    if not site_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a esta página"
        )
    
    update_data = page_data.model_dump(exclude_unset=True)
    
    if page_data.is_home is True:
        other_home = (await db.execute(
            select(Page).where(
                Page.site_id == page.site_id,
                Page.is_home == True,
                Page.id != page_id
            )
        )).scalars().all()
        for hp in other_home:
            hp.is_home = False
    
    for field, value in update_data.items():
        setattr(page, field, value)
    
    await db.commit()
    await db.refresh(page)
    return page


@router.delete("/{page_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_page(
    page_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Page).where(Page.id == page_id))
    page = result.scalar_one_or_none()
    
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Página no encontrada"
        )
    
    site_result = await db.execute(
        select(Site).where(Site.id == page.site_id, Site.user_id == current_user.id)
    )
    if not site_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a esta página"
        )
    
    await db.delete(page)
    await db.commit()


@router.post("/{page_id}/save-editor", response_model=PageResponse)
async def save_page_editor(
    page_id: int,
    gjs_data: str,
    gjs_html: str,
    gjs_css: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Page).where(Page.id == page_id))
    page = result.scalar_one_or_none()
    
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Página no encontrada"
        )
    
    site_result = await db.execute(
        select(Site).where(Site.id == page.site_id, Site.user_id == current_user.id)
    )
    if not site_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a esta página"
        )
    
    page.gjs_data = gjs_data
    page.gjs_html = gjs_html
    page.gjs_css = gjs_css
    
    await db.commit()
    await db.refresh(page)
    return page
