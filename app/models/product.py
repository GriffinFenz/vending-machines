from __future__ import annotations
from sqlalchemy import Column, Integer, String, DECIMAL, exists
from sqlalchemy.orm import relationship, Session
from app.extensions import Base
from app.utils.result import Result
from typing import List, Optional
from marshmallow_dataclass import dataclass


@dataclass
class Product(Base):
    product_id: int
    product_name: str
    price: float

    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(1000), nullable=False)
    price = Column(DECIMAL(precision=10, scale=2), nullable=False)

    parents = relationship(
        "MachineStock", back_populates="child", cascade="all,delete")

    def __init__(self, product_name: str, price: float):
        self.product_name = product_name
        self.price = price

    @staticmethod
    def has_product_by_id(session: Session, product_id: int) -> bool:
        return session.query(exists().where(Product.product_id == product_id)).scalar()

    @staticmethod
    def has_product_by_name(session: Session, product_name: str) -> bool:
        return session.query(exists().where(Product.product_name == product_name)).scalar()

    @staticmethod
    def get_product_by_id(session: Session, product_id: str) -> Optional[Product]:
        try:
            product_id = int(product_id)
        except ValueError:
            return None
        return session.query(Product).filter(Product.product_id == product_id).first()

    @staticmethod
    def get_product_by_name(session: Session, product_name: str) -> Optional[Product]:
        return session.query(Product).filter(Product.product_id == product_name).first()

    @staticmethod
    def get_all_products(session: Session) -> Optional[List[Product]]:
        return session.query(Product).all()

    @staticmethod
    def create(session: Session, product_name: str, price: str) -> Result:
        if product_name is None:
            return Result.fail('product_name cannot be None-type object')
        if price is None:
            return Result.fail('price cannot be None-type object')
        if Product.has_product_by_name(session, product_name):
            return Result.fail(f'product with name: {product_name} already exists')
        try:
            price = float(price)
            if price < 0:
                raise ValueError
        except ValueError:
            return Result.fail(f'product cannot be made with invalid price')

        return Result('product created', Product(product_name=product_name, price=price))

    @staticmethod
    def delete(session: Session, product_id: str) -> Result:
        product_to_delete = Product.get_product_by_id(session, product_id)
        if product_to_delete is None:
            return Result.fail('product could not be found')
        session.delete(product_to_delete)
        session.commit()
        return Result.success('product has been deleted', product_to_delete)

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'price': self.price
        }
