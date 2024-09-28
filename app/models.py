from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    descr = Column(String)
    price = Column(Float)
    total_amount = Column(Integer)

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    create_data = Column(DateTime, default=datetime.now)
    status = Column(String)
    items = relationship("OrderItem", lazy=False, viewonly=True)



class OrderItem(Base):
    __tablename__ = 'orderitem'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), index=True)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="SET NULL"), index=True)
    amount = Column(Integer)
    product = relationship("Product", lazy=False, viewonly=True)
