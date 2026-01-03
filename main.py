from fastapi import FastAPI
from models import Stock, Order
import database_models
from config import engine

api = FastAPI()
database_models.Base.metadata.create_all(bind = engine)


#Stock
@api.get("\stocks")
def get_all_stocks():
    pass

@api.get("\stock\{id}")
def get_stock(id: int):
    pass

@api.post("\stock")
def add_stock(order: Order):
    pass

@api.put("\stock\{id}")
def update_stock(id: int, order: Order):
    pass

@api.patch("\stock\{id}")
def change_stock_activity(id: int):
    pass


#Order
@api.get("\orders")
def get_all_orders():
    pass

@api.get("\order\{id}")
def get_order(id: int):
    pass

@api.post("\order")
def add_order(order: Order):
    pass

