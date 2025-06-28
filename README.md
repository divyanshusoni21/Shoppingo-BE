# 🛒 Shoppingo - Ecommerce Web Application

A modern, full-featured ecommerce web application built with Django REST Framework, featuring user authentication, product management, shopping cart functionality, order processing, and secure payment integration with Razorpay.

## 📚 API Documentation

### 📖 **Complete API Documentation**
For detailed API documentation with examples, request/response schemas, and testing capabilities, visit  **Postman Collection**:

🔗 **[View Complete API Documentation](https://documenter.getpostman.com/view/18000926/2s9YJW5RP9)**


## ✨ Features

### 🔐 User Management
- **Custom User Model**: Email-based authentication with phone number support
- **JWT Authentication**: Secure token-based authentication using Simple JWT
- **User Registration & Login**: Complete user account management
- **Email Verification**: Email-based account verification system
- **Profile Management**: User profile with personal information

### 🛍️ Product Management
- **Product Catalog**: Comprehensive product listing with categories and subcategories
- **Product Details**: Rich product information including images, descriptions, pricing, and reviews
- **Brand Management**: Product organization by brands
- **Product Tags**: Categorization and search functionality
- **Inventory Management**: Stock tracking and quantity management
- **Product Reviews & Ratings**: User-generated reviews and rating system

### 🛒 Shopping Experience
- **Shopping Cart**: Add, remove, and manage items in cart
- **Product Search**: Find products by name, category, or tags
- **Product Filtering**: Filter by category, brand, price range, and ratings
- **Wishlist**: Save products for later purchase

### 📦 Order Management
- **Order Processing**: Complete order lifecycle management
- **Order Tracking**: Track order status (Booked → Shipped → Delivered)
- **Order History**: View past orders and their details
- **Order Cancellation**: Cancel orders with proper status updates

### 💳 Payment Integration
- **Razorpay Integration**: Secure payment processing
- **Payment Verification**: Signature verification for payment security
- **Payment Status Tracking**: Real-time payment status updates
- **Multiple Payment Methods**: Support for various payment options

### 🧪 Testing
- **Comprehensive Test Suite**: Unit tests for models, views, and API endpoints
- **Test Coverage**: Extensive testing for all major functionality
- **API Testing**: REST API endpoint testing

## 🛠️ Technology Stack

- **Backend**: Django 4.x, Django REST Framework
- **Database**: SQLite (Development), PostgreSQL (Production ready)
- **Authentication**: JWT (JSON Web Tokens)
- **Payment Gateway**: Razorpay
- **Email Service**: SMTP (Brevo/Email service)
- **Image Handling**: Pillow
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Testing**: Django Test Framework, Locust (Load testing)

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd shoppingo
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory with the following variables:

```env
SECRET_KEY='your-secret-key'
DEBUG=True

# Email Configuration
EMAIL_HOST=smtp-relay.brevo.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=Shoppingo <your-email@example.com>

# Razorpay Configuration
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-secret-key

# Frontend Domain
FE_DOMAIN=http://127.0.0.1:8000

# JWT Token Configuration
ACCESS_TOKEN_LIFETIME=15
REFRESH_TOKEN_LIFETIME=30
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`


## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test home
python manage.py test usermgmt
python manage.py test order
python manage.py test payment
