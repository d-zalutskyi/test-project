from pydantic import BaseModel
from typing import Optional, List


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    external_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductInDB(ProductBase):
    id: int
    class Config:
        orm_mode = True
