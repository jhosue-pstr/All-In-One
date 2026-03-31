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
from packages.core.schemas.site import SiteCreate, SiteResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/sites", tags=["sites"])


@router.get("", response_model=List[SiteResponse])
async def list_sites(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Site).where(Site.user_id == current_user.id)
    )
    sites = result.scalars().all()
    return sites


@router.post("", response_model=SiteResponse, status_code=status.HTTP_201_CREATED)
async def create_site(
    site_data: SiteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Site).where(Site.slug == site_data.slug))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El slug ya está en uso"
        )

    site = Site(
        name=site_data.name,
        slug=site_data.slug,
        user_id=current_user.id
    )
    db.add(site)
    await db.commit()
    await db.refresh(site)
    return site


@router.get("/{site_id}", response_model=SiteResponse)
async def get_site(
    site_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Site).where(Site.id == site_id, Site.user_id == current_user.id)
    )
    site = result.scalar_one_or_none()
    
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site no encontrado"
        )
    return site


@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_site(
    site_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Site).where(Site.id == site_id, Site.user_id == current_user.id)
    )
    site = result.scalar_one_or_none()
    
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site no encontrado"
        )
    
    await db.delete(site)
    await db.commit()
