from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.extensions import Base, Engine, Session, db


class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(1000))
    price = Column(Float)

    def __init__(self, product_name, price):
        self.product_name = product_name
        self.price = price
