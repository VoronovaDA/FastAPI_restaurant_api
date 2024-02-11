from fastapi import APIRouter, Depends, HTTPException, status

from app.sessions import get_db
from typing import List

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from config import prefixes, MENUS_LINK, MENU_LINK
from app.models import Menu as DBMenu, SubMenu as DBSubMenu, Dish as DBDish
from app.schemas import Menu, MenuCreate


router = APIRouter(prefix=prefixes, tags=["Menu"])


@router.get(MENUS_LINK, response_model=List[Menu])
async def read_all_menus(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        menus_with_counts = await db.execute(
            select(
                DBMenu,
                func.count(DBSubMenu.id.distinct()).label('submenus_count'),
                func.count(DBDish.id.distinct()).label('dishes_count')
            ).select_from(DBMenu).outerjoin(DBSubMenu).outerjoin(DBDish).group_by(DBMenu.id).offset(skip).limit(limit)
        )
        result_menus = []
        for menu, submenus_count, dishes_count in menus_with_counts:
            menu_with_counts = Menu(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus_count=submenus_count,
                dishes_count=dishes_count
            )
            result_menus.append(menu_with_counts)

    return result_menus


@router.get(MENU_LINK, response_model=Menu)
async def read_menu(menu_id: str, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        menu_data = await db.execute(
            select(
                DBMenu,
                func.count(DBSubMenu.id.distinct()).label('submenus_count'),
                func.count(DBDish.id.distinct()).label('dishes_count')
            ).outerjoin(DBSubMenu, DBMenu.id == DBSubMenu.menu_id).outerjoin(DBDish, DBSubMenu.id == DBDish.submenu_id)
            .filter(DBMenu.id == menu_id).group_by(DBMenu.id)
        )

        menu_row = menu_data.fetchone()

        if not menu_row:
            raise HTTPException(status_code=404, detail="menu not found")

        menu, submenus_count, dishes_count = menu_row
        menu_with_counts = Menu(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count
        )

    return menu_with_counts


@router.post(MENUS_LINK, response_model=Menu, status_code=status.HTTP_201_CREATED)
async def create_menu(menu: MenuCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        db_menu = DBMenu(**menu.dict())
        session.add(db_menu)
        await session.commit()
        await session.refresh(db_menu)
        return db_menu


@router.patch(MENU_LINK, response_model=Menu)
async def update_menu(menu_id: str, menu: MenuCreate, db: AsyncSession = Depends(get_db)):
    db_menu = (await db.execute(select(DBMenu).filter(DBMenu.id == menu_id))).scalars().first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    for key, value in menu.dict(exclude_unset=True).items():
        setattr(db_menu, key, value)
    await db.commit()
    await db.refresh(db_menu)
    return db_menu


@router.delete(MENU_LINK)
async def delete_menu(menu_id: str, db: AsyncSession = Depends(get_db)):
    db_menu = await db.execute(select(DBMenu).filter(DBMenu.id == menu_id))
    db_menu = db_menu.scalars().first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    await db.delete(db_menu)
    await db.commit()
    return {"message": "Menu deleted successfully"}
