from fastapi import FastAPI
from models import StockBase,StockCreate,StockRead,StockUpdate, OrderCreate,OrderRead
import database_models
from config import engine, SessionLocal

api = FastAPI()
database_models.Base.metadata.create_all(bind = engine)

initial_stocks = [
    StockBase(
        stock_name="Phone",
        stock_price=399.0,
        stock_quantity=50,
        is_active=True
    ),
    StockBase(
        stock_name="Laptop",
        stock_price=999.0,
        stock_quantity=2,
        is_active=True
    ),
    StockBase(
        stock_name="Pen",
        stock_price=5.0,
        stock_quantity=0,
        is_active=False
    ),
    StockBase(
        stock_name="Table",
        stock_price=199.0,
        stock_quantity=10,
        is_active=True
    )
]

def init_db():
    db = SessionLocal()
    count = db.query(database_models.Stock).count()
    if count == 0:
        for i in initial_stocks:
            db.add(database_models.Stock(**i.model_dump()))
        db.commit()
    db.close()
        

init_db()
            



#Stock
# @api.get("/stocks")
# def get_all_stocks():
#     pass

# @api.get("/stocks/{id}")
# def get_stock(id: int):
#     pass

# @api.post("/stocks")
# def add_stock(order: Order):
#     pass

# @api.put("/stocks/{id}")
# def update_stock(id: int, order: Order):
#     pass

# @api.patch("/stocks/{id}")
# def change_stock_activity(id: int):
#     pass


# #Order
# @api.get("/orders")
# def get_all_orders():
#     pass

# @api.get("/orders/{id}")
# def get_order(id: int):
#     pass

# @api.post("/orders")
# def add_order(order: Order):
#     pass

