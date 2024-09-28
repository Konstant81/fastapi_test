from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base


DATABASE_URL_TEST = "postgresql+psycopg2://postgres_test:postgres@localhost:5434/test_db"

engine_test = create_engine(DATABASE_URL_TEST)

SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

# Base.metadata.create_all(bind=engine_test)

def override_get_db():
    db = SessionTest()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope="session")
def prepare_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)

client = TestClient(app)


def test_add_product():
    response = client.post("/products",
                            json={"name":"Phone", "descr":"Very good phone",
                                  "price":9999.99, "total_amount":5})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {"price":9999.99,"total_amount":5,
                    "name":"Phone","id":1,
                    "descr":"Very good phone"}
    
def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0] == {"price":9999.99,"total_amount":5,
                    "name":"Phone","id":1,
                    "descr":"Very good phone"}
    
def test_get_product():
    response = client.get("/products/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {"price":9999.99,"total_amount":5,
                    "name":"Phone","id":1,
                    "descr":"Very good phone"}
    
def test_get_not_found_product():
    response = client.get("/products/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["message"] == "Товар не найден"
    
def test_update_product():
    response = client.put("/products/1", json={"name":"Phone", "descr":"The best phone",
                                  "price":19999.99, "total_amount":15})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {"price":19999.99,"total_amount":15,
                    "name":"Phone","id":1,
                    "descr":"The best phone"}
    
def test_post_order_bad_status():
    response = client.post("/orders",
                           json={"status": "Где-то", "items": [{"product_id": 1, "amount": 20}]})
    assert response.status_code == 422, response.text
    data = response.json()
    data["detail"][0]["msg"] == "Value error, Поле статуса должно иметь значение 'В процессе', 'Отправлен' или 'Доставлен'"

def test_post_order_too_many_amount():
    response = client.post("/orders",
                           json={"status": "В процессе", "items": [{"product_id": 1, "amount": 20}]})
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["message"] == "На складе недостаточное количество товара с id = 1"

def test_post_order():
    response = client.post("/orders",
                           json={"status": "В процессе", "items": [{"product_id": 1, "amount": 10}]})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["status"] == "В процессе"
    assert data["items"][0]["product_id"] == 1
    assert data["items"][0]["amount"] == 10
    assert data["items"][0]["order_id"] == 1
    assert data["items"][0]["product"]["name"] == "Phone"
    assert data["items"][0]["product"]["total_amount"] == 5

def test_get_not_found_order():
    response = client.get("/orders/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["message"] == "Заказ не найден"

def test_get_order():
    response = client.get("/orders/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["status"] == "В процессе"
    assert data["items"][0]["product_id"] == 1
    assert data["items"][0]["amount"] == 10
    assert data["items"][0]["order_id"] == 1
    assert data["items"][0]["product"]["name"] == "Phone"
    assert data["items"][0]["product"]["total_amount"] == 5

def test_change_bad_status_order():
    response = client.patch("/orders/1", json={"status": "Поехал"})
    assert response.status_code == 422, response.text
    data = response.json()
    data["detail"][0]["msg"] == "Value error, Поле статуса должно иметь значение 'В процессе', 'Отправлен' или 'Доставлен'"

def test_change_status_order():
    response = client.patch("/orders/1", json={"status": "Отправлен"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "Отправлен"

def test_delete_product():
    response = client.delete("/products/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == {"price":19999.99,"total_amount":5,
                    "name":"Phone","id":1,
                    "descr":"The best phone"}
    
def test_check_deletion():
    response = client.get("/products/1")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["message"] == "Товар не найден"
