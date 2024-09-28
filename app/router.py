from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models import Order, OrderItem, Product
from app.schemas import ProductBase, OrderBase, PatchOrderBase
from app.database import get_db


order_router = APIRouter(prefix="/orders")
product_router = APIRouter(prefix="/products")

db_dependency = Annotated[Session, Depends(get_db)]


@product_router.get("")
async def get_products(db:db_dependency):
    return db.query(Product).all()

@product_router.get("/{prod_id}")
async def get_product(prod_id: int, db: db_dependency):
    db_product = db.query(Product).filter(Product.id == prod_id).first()
    if db_product is None:
        return JSONResponse(status_code=404, content={"message": "Товар не найден"})
    return db_product

@product_router.post("")
async def add_product(product: ProductBase, db: db_dependency):
    db_product = Product(name=product.name, descr=product.descr, price=product.price, total_amount=product.total_amount)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@product_router.put("/{prod_id}")
async def update_product(prod_id: int, product: ProductBase,  db: db_dependency):
    db_product = db.query(Product).filter(Product.id==prod_id).first()
    if db_product is None:
        return JSONResponse(status_code=404, content={"message": "Товар не найден"})
    db_product.name = product.name
    db_product.descr = product.descr
    db_product.price = product.price
    db_product.total_amount = product.total_amount
    db.commit()
    db.refresh(db_product)
    return db_product

@product_router.delete("/{prod_id}")
async def delete_product(prod_id: int, db: db_dependency):
    db_product = db.query(Product).filter(Product.id == prod_id).first()
    if db_product is None:
        return JSONResponse(status_code=404, content={"message": "Товар не найден"})
    db.delete(db_product)
    db.commit()
    return db_product

@order_router.post("")
async def add_order(order: OrderBase, db: db_dependency):
    db_order = Order(status=order.status)
    db.add(db_order)
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product.total_amount < item.amount:
            db.expunge_all()
            return JSONResponse(status_code=404, content={"message": f"На складе недостаточное количество товара с id = {item.product_id}"})
        product.total_amount -= item.amount
    db.commit()
    db.refresh(db_order)
    for item in order.items:
        item_db = OrderItem(order_id=db_order.id, product_id=item.product_id, amount=item.amount)
        db.add(item_db)
    db.commit()
    db.refresh(db_order)
    return db_order

@order_router.get("")
async def get_orders(db: db_dependency):
    return db.query(Order).all()

@order_router.get("/{order_id}")
async def get_order(order_id: int, db: db_dependency):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        return JSONResponse(status_code=404, content={"message": "Заказ не найден"})
    return db_order

@order_router.patch("/{order_id}")
async def patch_order(order_id: int, order: PatchOrderBase, db: db_dependency):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        return JSONResponse(status_code=404, content={"message": "Заказ не найден"})
    db_order.status = order.status
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
