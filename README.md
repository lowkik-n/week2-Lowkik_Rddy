<!-- filename: README.md -->

# Online Shopping API

## FastAPI Backend Application

This project implements the backend API for an online shopping application.

The application is built using Python and FastAPI.

The system allows users to register and log in.

Users can browse available categories.

Users can view and search products.

Users can add products to a shopping cart.

Users can update or remove cart items.

Users can view their cart summary.

Users can place orders through checkout.

Users can view their order history.

Users can view detailed information about individual orders.

The project follows a layered architecture.

The application separates API routes, business logic, database access, schemas, and models.

The design is intended to be simple, maintainable, and extensible.

---

## Table of Contents

1. Project Overview
2. Problem Statement
3. Project Objectives
4. Key Features
5. Technology Stack
6. Application Architecture
7. Project Structure
8. Request Processing Flow
9. Database Design
10. Entity Relationships
11. Users Table
12. Categories Table
13. Products Table
14. Cart Items Table
15. Orders Table
16. Order Details Table
17. FastAPI Concepts
18. Router Layer
19. Schema Layer
20. Service Layer
21. Repository Layer
22. Model Layer
23. Database Layer
24. Utility Layer
25. Application Startup
26. API Endpoints
27. User APIs
28. Category APIs
29. Product APIs
30. Cart APIs
31. Order APIs
32. Validation Rules
33. SQL Concepts
34. SQLAlchemy Concepts
35. Transactions
36. Error Handling
37. Swagger Testing
38. Testing Sequence
39. Running the Application
40. Troubleshooting
41. Security Considerations
42. Non-Functional Requirements
43. Future Enhancements
44. Development Guidelines
45. Milestones
46. Conclusion

---

## Project Overview

The Online Shopping API is a backend application.

It exposes REST API endpoints for online shopping activities.

The application does not contain a frontend user interface.

Users interact with the application through APIs.

Swagger UI can be used to test the APIs.

FastAPI automatically generates the Swagger documentation.

The application uses SQLAlchemy to communicate with the database.

The application can use SQLite for local development.

The application can be configured to use PostgreSQL.

The application uses Pydantic schemas for validation.

The application uses routers to organize endpoints.

The application uses services to implement business rules.

The application uses repositories to perform database operations.

The application uses models to represent database tables.

---

## Problem Statement

ABC currently operates a successful physical store.

ABC wants to expand its business to an online shopping platform.

The online platform must allow customers to create accounts.

Customers must be able to log in.

Customers must be able to browse products.

Customers must be able to search for products.

Customers must be able to add products to a cart.

Customers must be able to update cart quantities.

Customers must be able to remove products from a cart.

Customers must be able to place orders.

Customers must be able to view their previous orders.

The backend must be implemented using Python FastAPI.

The application must use a relational database.

The application must apply basic validations.

The application must use a maintainable project structure.

---

## Project Objectives

The first objective is to create a working FastAPI application.

The second objective is to create database models using SQLAlchemy.

The third objective is to define request and response schemas.

The fourth objective is to implement user registration.

The fifth objective is to implement user login.

The sixth objective is to implement product browsing.

The seventh objective is to implement product searching.

The eighth objective is to implement cart management.

The ninth objective is to implement checkout.

The tenth objective is to implement order history.

The final objective is to demonstrate a layered backend architecture.

---

## Key Features

### User Management

Users can register using their name, email, password, and mobile number.

The email address must be unique.

Users can log in using their email and password.

Invalid login details result in an error response.

### Category Browsing

Users can view all available product categories.

Categories can be sorted alphabetically.

The current customer-facing requirement includes a GET categories API.

Category creation can be added later for administrative users.

### Product Browsing

Users can view all products.

Users can view an individual product.

Users can search products by name.

Users can filter products by category.

Products display their price and available quantity.

### Cart Management

Users can add products to their cart.

Users can add a specific quantity.

Users can update the quantity of a cart item.

Users can remove an item from their cart.

Users can view the total cart amount.

Users cannot add more products than available stock.

### Order Management

Users can check out their cart.

The system calculates the order total.

The system creates an order record.

The system creates order detail records.

The system reduces product inventory.

The system clears the cart after successful checkout.

Users can view order history.

Users can view order details.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | Web API framework |
| Uvicorn | ASGI application server |
| SQLAlchemy | ORM and database access |
| Pydantic | Request and response validation |
| SQLite | Local development database |
| PostgreSQL | Production-capable relational database |
| Swagger UI | API testing and documentation |
| Git | Source control |
| Visual Studio Code | Development environment |

---

## Application Architecture

The application follows a layered architecture.

Each layer has a separate responsibility.

The router layer receives HTTP requests.

The schema layer validates request and response data.

The service layer contains business logic.

The repository layer communicates with the database.

The model layer defines database tables.

The database layer creates sessions and connections.

The utility layer contains reusable helper functions.

The main application connects all routers together.

---

## Layered Request Flow

A request begins at Swagger UI or another API client.

The request enters the FastAPI application.

The request is matched to a router endpoint.

The router receives the request payload.

The schema validates the payload.

The router creates or calls a service object.

The service checks business rules.

The service calls one or more repositories.

The repository executes database queries.

The database returns a result.

The repository returns the result to the service.

The service applies any additional business logic.

The router returns a response schema.

FastAPI serializes the response.

The response is displayed to the client.

---

## Project Structure

```text
app/
|
├── main.py
|
├── db/
│   ├── __init__.py
│   ├── session.py
│   └── base.py
|
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── category.py
│   ├── product.py
│   ├── cart.py
│   └── order.py
|
├── schemas/
│   ├── __init__.py
│   ├── user_schema.py
│   ├── product_schema.py
│   ├── cart_schema.py
│   └── order_schema.py
|
├── repositories/
│   ├── __init__.py
│   ├── user_repository.py
│   ├── category_repository.py
│   ├── product_repository.py
│   ├── cart_repository.py
│   └── order_repository.py
|
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   ├── category_service.py
│   ├── product_service.py
│   ├── cart_service.py
│   └── order_service.py
|
├── routers/
│   ├── __init__.py
│   ├── user_router.py
│   ├── category_router.py
│   ├── product_router.py
│   ├── cart_router.py
│   └── order_router.py
|
├── utils/
│   ├── __init__.py
│   ├── exceptions.py
│   └── helpers.py
|
├── tests/
|
└── requirements.txt
