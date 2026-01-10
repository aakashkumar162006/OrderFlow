from fastapi import FastAPI, Depends, HTTPException
from models import StockRead, StockCreate, StockUpdate, OrderRead, OrderCreate
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

#Stocks
@api.get("/stocks", response_model = list[StockRead], status_code = 200)
def get_all_stocks(db: Session = Depends(get_db)):
    stocks = db.query(database_models.Stock).all()
    return stocks
   
    

@api.get("/stocks/{id}", response_model = StockRead, status_code = 200)
def get_stock(id: int, db: Session = Depends(get_db)):
    stock = db.query(database_models.Stock).filter(database_models.Stock.stock_id == id).first()
    if stock:
        return stock
    else:
        raise HTTPException(status_code = 404, detail = "Stock Not Found")
    
@api.post("/stocks",response_model = StockRead,status_code = 201)
def add_stock(stock: StockCreate, db: Session = Depends(get_db)):
    created_stock = database_models.Stock(**stock.model_dump())
    db.add(created_stock)
    db.commit()
    db.refresh(created_stock)
    return created_stock

@api.patch("/stocks/{id}", response_model=StockRead, status_code = 200)
def update_stock(id: int, stock: StockUpdate, db: Session = Depends(get_db)):
    db_stock = db.query(database_models.Stock).filter(database_models.Stock.stock_id == id).first()
    if db_stock:
        updated_stock = stock.model_dump(exclude_unset=True)
        for field, value in updated_stock.items():
            setattr(db_stock, field, value)
        db.commit()
        return db_stock
    raise HTTPException(status_code = 404, detail = "Stock Not Found")

@api.patch("/stocks/{id}/toggle-active", response_model = StockRead, status_code = 200)
def toggle_stock_activity(id: int, db: Session = Depends(get_db)):
    db_stock = db.query(database_models.Stock).filter(database_models.Stock.stock_id == id).first()
    if db_stock:
        db_stock.is_active = not db_stock.is_active
        db.commit()
        return db_stock
    else:    
        raise HTTPException(status_code = 404, detail = "Stock Not Found")

# Order
@api.get("/orders", response_model = list[OrderRead], status_code = 200)
def get_all_orders(db: Session = Depends(get_db)):
    db_orders = db.query(database_models.Order).all()
    return db_orders
    

@api.get("/orders/{id}", response_model = OrderRead, status_code = 200)
def get_order(id: int, db: Session = Depends(get_db)):
    db_order = db.query(database_models.Order).filter(database_models.Order.order_id == id).first()
    if db_order:
        return db_order
    raise HTTPException(status_code = 404, detail = "Order Not Found")

@api.post("/orders", response_model = OrderRead, status_code = 201)
def add_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        stock = db.query(database_models.Stock).filter(database_models.Stock.stock_id == order.stock_id).with_for_update().first()
        if not stock:
            raise HTTPException(status_code = 404, detail = "Stock Not Found")
        
        if stock.is_active == False:
            raise HTTPException(status_code = 400, detail = "Stock currently unavailable")

        if stock.stock_quantity < order.quantity:
            raise HTTPException(status_code = 400, detail = "Order exceeds Stock quantity")
        
        stock.stock_quantity -= order.quantity
        if stock.stock_quantity == 0:
            stock.is_active = False
        
        created_order = database_models.Order(**order.model_dump())
        db.add(created_order) 
        db.commit()
        db.refresh(created_order)
        return created_order
    
    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise HTTPException(500, "Order Creation Failed")

