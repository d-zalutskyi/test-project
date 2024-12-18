import logging

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.pydantic_schemas import ProductCreate, ProductUpdate
from app.db.queries import TaskQueries
from app.api.external_api import fetch_external_product
from app.api.background_tasks import refresh_all_products


logger = logging.getLogger(__name__)

task_router = APIRouter(
    prefix="/products",
    tags=["Tasks API"]
)


@task_router.post("/")
async def create(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        products = await TaskQueries.create_product(db, product)
        return products
    except Exception as exc:
        logger.error(f"Error appeared - {exc}")
        raise exc


@task_router.get("/")
async def read_all(db: AsyncSession = Depends(get_db)):
    try:
        products = await TaskQueries.list_products(db)
        return products
    except Exception as exc:
        logger.error(f"Error appeared - {exc}")
        raise exc


@task_router.get("/{product_id}")
async def read(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        product = await TaskQueries.get_product(db, product_id)
        return product
    except Exception as exc:
        logger.error(f"Error appeared - {exc}")
        raise exc


@task_router.put("/{product_id}")
async def update(
    product_id: int,
    product: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        product = await TaskQueries.update_product(db, product_id, product)
        return product
    except Exception as exc:
        logger.error(f"Error appeared - {exc}")
        raise exc


@task_router.delete("/{product_id}")
async def delete(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        product = await TaskQueries.delete_product(db, product_id)
        return product
    except Exception as exc:
        logger.error(f"Error appeared - {exc}")
        raise exc


@task_router.post("/fetch_external/")
async def fetch_and_create(
    external_ids: list[int],
    db: AsyncSession = Depends(get_db)
):
    try:
        products = []
        for external_id in external_ids:
            external_product = await fetch_external_product(external_id)
            products.append(await TaskQueries.create_product(db, external_product))
        return products
    except Exception as exc:
        logger.error(f"Error appeared - {exc}")
        raise exc


@task_router.post("/refresh_all/")
async def refresh_all(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    try:
        await refresh_all_products(db, background_tasks)
        return {"message": "Refresh started"}
    except Exception as exc:
        logger.error(f"Error appeared - {exc}")
        raise exc