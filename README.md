# OrderFlow API

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A FastAPI-based inventory and order management system with PostgreSQL database.

## ✨ Features

- **Stock Management** — Create, read, update, and toggle stock availability
- **Order Processing** — Create orders with automatic stock deduction
- **Concurrency Control** — Row-level locking prevents race conditions
- **Auto-deactivation** — Stocks automatically deactivate when quantity reaches 0
- **Foreign Key Protection** — Preserves order history by preventing stock deletion

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | Modern Python web framework |
| SQLAlchemy | ORM for database operations |
| PostgreSQL | Relational database |
| Pydantic | Data validation |
| Uvicorn | ASGI server |

## 📁 Project Structure

```
OrderFlow/
├── main.py              # API endpoints and business logic
├── models.py            # Pydantic schemas for validation
├── database_models.py   # SQLAlchemy ORM models
├── config.py            # Database configuration
├── requirements.txt     # Dependencies
└── README.md
```

## 🚀 Quick Start

```bash
# Clone and install
git clone <your-repo-url>
cd OrderFlow
pip install -r requirements.txt

# Configure and run
# Set DATABASE_URL in config.py or environment variable
uvicorn main:api --reload
```

## 📦 Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 13+
- pip

### Steps

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd OrderFlow
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   
   Set the database URL in `config.py` or via environment variable:
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost/orderflow_db"
   ```

5. **Run the application:**
   ```bash
   uvicorn main:api --reload
   ```

> **Note:** PostgreSQL database must exist before running. Tables are created automatically on startup.

## 🔌 API Endpoints

### Stocks

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/stocks` | Get all stocks |
| `GET` | `/stocks/{id}` | Get specific stock |
| `POST` | `/stocks` | Create new stock |
| `PATCH` | `/stocks/{id}` | Update stock details |
| `PATCH` | `/stocks/{id}/toggle-active` | Toggle stock availability |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/orders` | Get all orders |
| `GET` | `/orders/{id}` | Get specific order |
| `POST` | `/orders` | Create new order |

## 📖 API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 💡 Example Usage

### Create a Stock
```bash
curl -X POST "http://localhost:8000/stocks" \
  -H "Content-Type: application/json" \
  -d '{"stock_name": "Widget", "stock_price": 29.99, "stock_quantity": 100}'
```

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

## 🗄 Database Schema

```
┌─────────────────┐       ┌─────────────────┐
│     stocks      │       │     orders      │
├─────────────────┤       ├─────────────────┤
│ stock_id (PK)   │◄──────│ stock_id (FK)   │
│ stock_name      │       │ order_id (PK)   │
│ stock_price     │       │ quantity        │
│ stock_quantity  │       │ status          │
│ is_active       │       │ created_at      │
└─────────────────┘       └─────────────────┘
```

## 🎯 Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Soft Deletes** | Stocks use `is_active` flag instead of hard deletes to preserve order history |
| **Row-Level Locking** | `SELECT FOR UPDATE` prevents race conditions during concurrent orders |
| **Foreign Keys** | Enforces data consistency and prevents orphaned records |
| **Auto-seeding** | Initial sample data populates on first run for quick testing |

## ⚙️ Business Logic

- ✅ Orders automatically reduce stock quantity
- ✅ Stocks deactivate when quantity reaches 0
- ✅ Inactive stocks cannot accept new orders
- ✅ Row-level locking prevents concurrent order conflicts
- ✅ Initial sample data seeded on first run

## 📸 Screenshots

### Swagger UI Documentation
Interactive API documentation auto-generated by FastAPI, showing all available endpoints for stocks and orders management.

![Swagger UI](screenshots/swagger-ui.png)

---

### Get All Stocks
Response from `GET /stocks` endpoint showing the list of available inventory items with their prices, quantities, and active status.

![Get Stocks Response](screenshots/get-stocks.png)

---

### Create Order - Request
Example request body for `POST /orders` endpoint, specifying the stock ID and quantity to order.

![Create Order Request](screenshots/create-order-request.png)

---

### Create Order - Response
Successful order response showing the created order with calculated total price and automatic stock deduction.

![Create Order Response](screenshots/create-order-response.png)

---

### Database Schema
PostgreSQL database structure showing the `stocks` and `orders` tables with their relationships and foreign key constraints.

![Database Tables](screenshots/database-schema.png)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.