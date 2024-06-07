# inventory-management

This is a Flask-based web application designed to manage the inventory of products in various locations or warehouses. It provides functionalities to add, edit, and view products, locations, and product movements. Additionally, it offers a report on the balance quantity of products in each location.

## Features

- **Products Management**: Add, edit, and view products.
- **Locations Management**: Add, edit, and view locations.
- **Product Movements**: Track the movement of products between different locations.
- **Report**: View the balance quantity of products in each location.

## Prerequisites

- Python 3.6 or higher
- Flask
- Flask-SQLAlchemy

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/inventory-management.git
    cd inventory-management
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Set up the database**:
    ```sh
    flask db init
    flask db upgrade
    ```

4. **Run the application**:
    ```sh
    flask run
    ```

The application should now be running on `http://127.0.0.1:5000`.

## Directory Structure

```plaintext
FLASKPROJECT/
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── routes.py
│   └── templates/
│       ├── base.html
│       ├── products.html
│       ├── add_edit_product.html
│       ├── locations.html
│       ├── add_edit_location.html
│       ├── movements.html
│       ├── add_edit_movement.html
│       └── report.html
├── config.py
├── run.py
├── requirements.txt
└── README.md
