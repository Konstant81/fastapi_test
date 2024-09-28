from fastapi import FastAPI
from app.database import engine, Base
from app.router import order_router, product_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(product_router)
app.include_router(order_router)
