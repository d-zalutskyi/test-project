from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Column, Integer, String, Float


Base: DeclarativeMeta = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    external_id = Column(Integer, unique=True)
