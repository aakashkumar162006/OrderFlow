from pydantic import BaseModel

class Stock(BaseModel):
    stock_id: int
    stock_name: str
    stock_price: float
    stock_quantity: int
    is_active: bool

class Order(BaseModel):
    order_id: int
    item_id: int
    quantity: int
    status: str
    created_at: str