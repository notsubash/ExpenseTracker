# ExpenseTracker with Streamlit UI

## Overview

This project is an enhanced version of the LangGraph Expense Tracker, now featuring a Streamlit user interface for improved usability. It allows users to upload pictures of invoices, which are then processed to structure and categorize expenses before storing them in a database.

## Features

- Process receipts by uploading images
- Manage expenses, categories, and payment methods through a user-friendly interface
- Utilizes LangGraph for intelligent expense categorization and structuring
- Stores data in a PostgreSQL database


## Setup Instructions

### 1. Create Project

1.1 Create virtual environment
Using Conda, venv or any other tool of your liking. I used poetry.

1.2 Activate virtual environment

1.3 Clone repo

1.4 Install requirements:

```poetry install```

1.5 Create .env file
See example in .env.example.

### 2. Set up the database

#### 2.1 Prerequisites

2.1.1 Install postgresql:

```brew install postgresql```

2.1.2 Install Docker:

```brew install docker```

#### 2.2 Make a Docker container

2.2.1 Create:

```docker run -d --name postgres-expenses -e POSTGRES_USER=expenses -e POSTGRES_PASSWORD=money$ -e POSTGRES_DB=expenses -p 6025:5432 postgres:latest```


2.2.2 Control:
Use the following command to see if the container is running correctly:

```docker ps```

It should show a list of running containers.

#### 2.3 Configure database

2.3.1 Create tables
Add tables for our expense tracking by running the `/src/database/create_tables.py` script

2.3.2 Inspect tables
Using a tool like [PGAdmin](pgadmin.org), you can inspect if the tables in the database are all there.

### 3. Set up API

Go to the root folder of your project and activate virtual environment:

```CD path/to/your/projectfolder workon expense-tracker```


Activate virtual environment:

```uvicorn src.api.run_api:app --reload```

You can visit [http://localhost:8000/docs#/](http://localhost:8000/docs#/) for a page with documentation about the API.

### 4. Running the Streamlit Interface

Launch the Streamlit interface:

```streamlit run src/streamlit.py```


## Using the Streamlit Interface

The Streamlit interface provides four main pages:

1. **Process Receipt**: Upload and process receipt images
2. **Expenses**: View and manage expenses
3. **Categories**: Manage expense categories
4. **Payment Methods**: Manage payment methods

## Database Structure

The database consists of three main tables:

### Table: categories
This table contains a list of categories for expenses. Each category has a unique ID and a name.

- **Columns**:
  - `category_id` (SERIAL, Primary Key): The unique ID for the category.
  - `category_name` (VARCHAR(100), Unique): The name of the category.

### Table: payment_methods
This table contains various payment methods that can be used for expenses.

- **Columns**:
  - `payment_method_id` (SERIAL, Primary Key): The unique ID for the payment method.
  - `payment_method_name` (VARCHAR(50), Unique): The name of the payment method.

### Table: expenses
This is the main table for tracking expenses. It contains information such as the date, the category (with a reference to the `categories` table), the payment method (with a reference to the `payment_methods` table), the amount, VAT, and other details.

- **Columns**:
  - `transaction_id` (SERIAL, Primary Key): The unique ID for the transaction.
  - `date` (DATE): The date of the expense.
  - `category_id` (INTEGER, Foreign Key): Reference to the `categories` table.
  - `description` (TEXT): A short description of the expense.
  - `amount` (DECIMAL(10, 2)): The amount of the expense.
  - `vat` (DECIMAL(10, 2)): The VAT for the expense.
  - `payment_method_id` (INTEGER, Foreign Key): Reference to the `payment_methods` table.
  - `business_personal` (VARCHAR(50)): Indicates whether the expense is business or personal.
  - `declared_on` (DATE): The date when the expense was declared.

## API Endpoints

The application provides the following key API endpoints:

### Expenses
- POST /expenses: Create a new expense
- GET /expenses: Retrieve all expenses
- DELETE /expenses/{transaction_id}: Delete an expense

### Categories
- POST /categories: Create a new category
- GET /categories: Retrieve all categories
- DELETE /categories/{category_id}: Delete a category

### Payment Methods
- POST /payment-methods: Create a new payment method
- GET /payment-methods: Retrieve all payment methods
- DELETE /payment-methods/{payment_method_id}: Delete a payment method

These endpoints provide Create, Read, and Delete (CRD) functionality for expenses, categories, and payment methods in your ExpenseTracker application.

For detailed API documentation, including request/response schemas and example usage, visit http://localhost:8000/docs# when the API is running.


