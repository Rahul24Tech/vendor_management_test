# Vendor Management System

This is a Vendor Management System developed using Django and Django REST Framework. The system handles vendor profiles, tracks purchase orders, and calculates vendor performance metrics.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Django 3.2+
- Django REST Framework
- PostgreSQL (or any preferred database)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-repo/vendor-management.git
    cd vendor-management
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

7. Access the admin site at `http://localhost:8000/admin/` and login with your superuser credentials.

## API Endpoints

### Vendor Endpoints

- **Create a new vendor**
    ```http
    POST /api/vendors/
    ```

- **List all vendors**
    ```http
    GET /api/vendors/
    ```

- **Retrieve a specific vendor's details**
    ```http
    GET /api/vendors/{vendor_id}/
    ```

- **Update a vendor's details**
    ```http
    PUT /api/vendors/{vendor_id}/
    ```

- **Delete a vendor**
    ```http
    DELETE /api/vendors/{vendor_id}/
    ```

- **Retrieve a vendor's performance metrics**
    ```http
    GET /api/vendors/{vendor_id}/performance/
    ```

### Purchase Order Endpoints

- **Create a purchase order**
    ```http
    POST /api/purchase_orders/
    ```

- **List all purchase orders**
    ```http
    GET /api/purchase_orders/
    ```

- **Retrieve details of a specific purchase order**
    ```http
    GET /api/purchase_orders/{po_id}/
    ```

- **Update a purchase order**
    ```http
    PUT /api/purchase_orders/{po_id}/
    ```

- **Delete a purchase order**
    ```http
    DELETE /api/purchase_orders/{po_id}/
    ```

## Authentication

To access the API, you need to authenticate using JWT tokens.

- **Obtain a token**
    ```http
    POST /api/token/
    ```

- **Refresh a token**
    ```http
    POST /api/token/refresh/
    ```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## Running Tests

Run the test suite to verify the functionality and reliability of the endpoints:
```sh
python manage.py test
