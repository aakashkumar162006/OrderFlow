from fastapi import FastAPI, Depends
from models import StockBase,StockCreate,StockRead,StockUpdate, OrderCreate,OrderRead
import database_models
from config import engine, SessionLocal
from sqlalchemy.orm import Session

api = FastAPI()
database_models.Base.metadata.create_all(bind = engine)

initial_stocks = [
    StockUpdate(
        stock_name="Phone",
        stock_price=399.0,
        stock_quantity=50,
        is_active=True
    ),
    StockUpdate(
        stock_name="Laptop",
        stock_price=999.0,
        stock_quantity=2,
        is_active=True
    ),
    StockUpdate(
        stock_name="Pen",
        stock_price=5.0,
        stock_quantity=0,
        is_active=False
    ),
    StockUpdate(
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
            
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@api.get("/stocks", response_model = list[StockRead])
def get_all_stocks(db: Session = Depends(get_db)):
    stocks = db.query(database_models.Stock).all()
    if stocks:
        return stocks
    else:
        return {"error" : "Stock Not Found"}
    

@api.get("/stocks/{id}", response_model = StockRead)
def get_stock(id: int, db: Session = Depends(get_db)):
    stock = db.query(database_models.Stock).filter(database_models.Stock.stock_id == id).first()
    if stock:
        return stock
    
@api.post("/stocks")
def add_stock(stock: StockBase, db: Session = Depends(get_db)):
    db.add(database_models.Stock(**stock.model_dump()))
    db.commit()
    return {'message' : 'Stock added successfully'}

@api.put("/stocks/{id}")
def update_stock(id: int, stock: StockUpdate, db: Session = Depends(get_db)):
    db_stock = db.query(database_models.Stock).filter(database_models.Stock.stock_id == id).first()
    if db_stock:
        updated_stock = stock.model_dump(exclude_unset=True)
        for field, value in updated_stock.items():
            setattr(db_stock, field, value)
        db.commit()
        return {'message' : 'Stock updated successfully'}
    return {'error' : 'Stock not found'}

@api.patch("/stocks/{id}/toggle-active")
def toggle_stock_activity(id: int, db: Session = Depends(get_db)):
    db_stock = db.query(database_models.Stock).filter(database_models.Stock.stock_id == id).first()
    if db_stock:
        db_stock.is_active = not db_stock.is_active
        db.commit()
        return {'message': f'Stock activity toggled to {db_stock.is_active}'}
    return {'error': 'Stock not found'}

@api.delete("/stocks/{id}")
def delete_stock(id: int, db: Session = Depends(get_db)):
    db_stock = db.query(database_models.Stock).filter(database_models.Stock.stock_id == id).first()
    if db_stock:
        db.delete(db_stock)
        db.commit()
        return {'message' : 'Stock removed successfully'}


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

