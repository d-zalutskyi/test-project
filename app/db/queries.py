from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import Product
from app.db.pydantic_schemas import ProductCreate, ProductUpdate


class TaskQueries:

    @classmethod
    async def create_product(cls, db: AsyncSession, product: ProductCreate):
        db_product = Product(**product.dict())
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return db_product

    @classmethod
    async def get_product(cls, db: AsyncSession, product_id: int):
        result = await db.execute(select(Product).where(Product.id == product_id))
        return result.scalars().first()

    @classmethod
    async def update_product(cls, db: AsyncSession, product_id: int, product: ProductUpdate):
        db_product = await cls.get_product(db, product_id)
        if db_product:
            for key, value in product.dict().items():
                setattr(db_product, key, value)
            await db.commit()
            await db.refresh(db_product)
        return db_product

    @classmethod
    async def delete_product(cls, db: AsyncSession, product_id: int):
        db_product = await cls.get_product(db, product_id)
        if db_product:
            await db.delete(db_product)
            await db.commit()
        return db_product

    @classmethod
    async def list_products(cls, db: AsyncSession):
        result = await db.execute(select(Product))
        return result.scalars().all()
