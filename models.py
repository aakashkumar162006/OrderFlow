from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class StockRead(BaseModel):
    stock_id: int
    stock_name: str
    stock_price: float
    stock_quantity: int
    is_active: bool
    class Config:
        from_attributes = True

class StockCreate(BaseModel):
    stock_name: str
    stock_price: float
    stock_quantity: int

class StockUpdate(BaseModel):
    stock_name: Optional[str] = None
    stock_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None

class OrderRead(BaseModel):
    order_id: int
    stock_id: int
    quantity: int
    status: bool
    created_at: datetime
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    stock_id: int
    quantity: int = Field(gt=0)