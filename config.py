import os

from dotenv import load_dotenv

load_dotenv()
prefixes = '/api/v1'
# PREFIX_LINK = 'http://127.0.0.1:8000/api/v1'
MENUS_LINK = '/menus/'
MENU_LINK = '/menus/{menu_id}'
SUBMENUS_LINK = '/menus/{menu_id}/submenus/'
SUBMENU_LINK = '/menus/{menu_id}/submenus/{submenu_id}'
DISHES_LINK = '/menus/{menu_id}/submenus/{submenu_id}/dishes/'
DISH_LINK = '/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'

PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_DB = os.getenv('PG_DB')

conn_url = f'postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@localhost:5432/{PG_DB}'
