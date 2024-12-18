import httpx

from app.db.pydantic_schemas import ProductCreate
from app.settings import config


async def fetch_external_product(external_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{config.EXTERNAL_API_URL}/{external_id}")
        response.raise_for_status()
        data = response.json()
        return ProductCreate(
            name=data.get("title"),
            description=data.get("body"),
            price=0.0,  # Example
            external_id=external_id,
        )