from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.queries import TaskQueries
from app.api.external_api import fetch_external_product


async def refresh_all_products(db: AsyncSession, background_tasks: BackgroundTasks):
    products = await TaskQueries.list_products(db)
    for product in products:
        background_tasks.add_task(refresh_product, db, product)

async def refresh_product(db: AsyncSession, product):
    updated_data = await fetch_external_product(product.external_id)
    await TaskQueries.update_product(db, product.id, updated_data)
