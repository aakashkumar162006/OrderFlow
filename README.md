# OrderFlow API

A FastAPI-based inventory and order management system with PostgreSQL database.

## Features

- **Stock Management**: Create, read, update, and toggle stock availability
- **Order Processing**: Create orders with automatic stock deduction
- **Concurrency Control**: Row-level locking prevents race conditions
- **Auto-deactivation**: Stocks automatically deactivate when quantity reaches 0
- **Foreign Key Protection**: Preserves order history by preventing stock deletion

## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

## Project Structure

```
OrderFlow/
├── main.py              # API endpoints and business logic
├── models.py            # Pydantic schemas for validation
├── database_models.py   # SQLAlchemy ORM models
├── config.py            # Database configuration
└── requirements.txt     # Dependencies
```

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd OrderFlow
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database in `config.py`:
```python
DATABASE_URL = "postgresql://user:password@localhost/orderflow_db"
```

4. Run the application:
```bash
uvicorn main:api --reload
```

## API Endpoints

### Stocks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stocks` | Get all stocks |
| GET | `/stocks/{id}` | Get specific stock |
| POST | `/stocks` | Create new stock |
| PATCH | `/stocks/{id}` | Update stock details |
| PATCH | `/stocks/{id}/toggle-active` | Toggle stock availability |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders` | Get all orders |
| GET | `/orders/{id}` | Get specific order |
| POST | `/orders` | Create new order |

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example Usage

### Create an Order
```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{"stock_id": 1, "quantity": 5}'
```

### Get All Stocks
```bash
curl "http://localhost:8000/stocks"
```

## Database Schema

### Stocks Table
- `stock_id` (PK)
- `stock_name`
- `stock_price`
- `stock_quantity`
- `is_active`

### Orders Table
- `order_id` (PK)
- `stock_id` (FK)
- `quantity`
- `status`
- `created_at`

## Business Logic

- Orders automatically reduce stock quantity
- Stocks deactivate when quantity reaches 0
- Inactive stocks cannot accept new orders
- Row-level locking prevents concurrent order conflicts
- Initial sample data seeded on first run

## License

MIT