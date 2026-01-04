from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StockBase(BaseModel):
    stock_name: str
    stock_price: float
    stock_quantity: int

class StockCreate(StockBase):
    pass

class StockUpdate(BaseModel):
    stock_name: Optional[str] = None
    stock_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None

class StockRead(StockBase):
    stock_id: int
    is_active: bool
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    stock_id: int
    quantity: int
    
class OrderRead(BaseModel):
    order_id: int
    stock_id: int
    quantity: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True