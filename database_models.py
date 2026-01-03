from sqlalchemy import Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Stock(Base):

    __tablename__ = "stocks"

    stock_id : Mapped[int] = mapped_column(Integer, primary_key=True)
    stock_name: Mapped[str] = mapped_column(String, nullable=False)
    stock_price: Mapped[float] = mapped_column(Float, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)

class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.stock_id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[str] = mapped_column(String, nullable=False)