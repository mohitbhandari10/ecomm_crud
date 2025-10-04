
# Ecommerce Product Management System

A full-stack ecommerce application for product management with user authentication and admin controls.

## Features

* User Registration & Login
* Product CRUD Operations (Create, Read, Update, Delete)
* Admin-only product management
* Responsive design
* JWT-based authentication

## Tech Stack

* **Backend** : FastAPI, PostgreSQL, SQLAlchemy
* **Frontend** : HTML, CSS, JavaScript
* **Authentication** : JWT tokens
* **Database** : PostgreSQL

## Setup Instructions

### Prerequisites

* Python 3.8+
* PostgreSQL
* pip (Python package manager)

### Database Setup

1. **Install PostgreSQL** (if not already installed):
   **bash**

   Copy

   Download

   ```
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   ```
2. **Create Database and User** :
   **bash**

   Copy

   Download

```
   sudo -u postgres psql
```

   In PostgreSQL shell:
   **sql**

   Copy

   Download

```
   -- Create database
   CREATE DATABASE ecommerce_db;

   -- Create user
   CREATE USER ecommerce_user WITH PASSWORD 'ecommerce_password';

   -- Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;

   -- Connect to database and grant schema privileges
   \c ecommerce_db;
   GRANT ALL ON SCHEMA public TO ecommerce_user;
   GRANT ALL ON SCHEMA ecommerce_schema TO ecommerce_user;
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ecommerce_user;
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA ecommerce_schema TO ecommerce_user;

   -- Exit PostgreSQL
   \q
```

### Backend Setup

1. **Navigate to the backend directory** :
   **bash**

   Copy

   Download

```
   cd backend
```

1. **Create and activate virtual environment** :
   **bash**

   Copy

   Download

```
   python3 -m venv venv
   source venv/bin/activate
```

1. **Install dependencies** :
   **bash**

   Copy

   Download

```
   pip install -r requirements.txt
```

1. **Configure environment variables** :
   Create/update `.env` file in backend directory:
   **env**

   Copy

   Download

```
   DATABASE_URL=postgresql://ecommerce_user:ecommerce_password@localhost/ecommerce_db
   SECRET_KEY=your-super-secret-key-here-make-it-very-long-and-random-at-least-32-characters
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
```

    **Note** : Replace the values with your actual:

* Database credentials
* A strong secret key (can generate with: `openssl rand -hex 32`)

1. **Run the backend server** :
   **bash**

   Copy

   Download

```
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

   The backend will:

* Create `ecommerce_schema` automatically
* Create tables (`users`, `products`) in the schema
* Start API server on `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory** (in a new terminal):
   **bash**

   Copy

   Download

   ```
   cd frontend
   ```
2. **Start the frontend server** :
   **bash**

   Copy

   Download

```
   python3 -m http.server 3000
```

1. **Access the application** :

* Frontend: `http://localhost:3000`
* Backend API: `http://localhost:8000`
* API Documentation: `http://localhost:8000/docs`

## Usage Instructions

### User Registration & Login

1. **Register a new user** :

* Go to `http://localhost:3000/register.html`
* Fill in email and password
* Click "Register"

1. **Login** :

* Go to `http://localhost:3000/login.html`
* Enter credentials
* Click "Login"

### Making a User Admin

By default, new users are not admins. To make a user an admin:

1. **Access PostgreSQL** :
   **bash**

   Copy

   Download

```
   sudo -u postgres psql
```

1. **Connect to database and update user** :
   **sql**

   Copy

   Download

```
   \c ecommerce_db
   UPDATE ecommerce_schema.users SET is_admin = true WHERE email = 'your-email@example.com';
```

   Example:
   **sql**

   Copy

   Download

```
   UPDATE ecommerce_schema.users SET is_admin = true WHERE email = 'admin@123.com';
```

1. **Verify the update** :
   **sql**

   Copy

   Download

```
   SELECT email, is_admin FROM ecommerce_schema.users;
```

### Product Management

 **For Admin Users** :

* **View Products** : All users can view products
* **Add Product** : Click "Add Product" button on products page
* **Edit Product** : Click "Edit" button on product card
* **Delete Product** : Click "Delete" button on product card

 **For Regular Users** :

* Only view products (no edit/delete permissions)

## API Endpoints

### Authentication

* `POST /register` - User registration
* `POST /login` - User login

### Products

* `GET /products` - Get all products (all users)
* `POST /products` - Create product (admin only)
* `PUT /products/{id}` - Update product (admin only)
* `DELETE /products/{id}` - Delete product (admin only)

## Database Schema

### Users Table (`ecommerce_schema.users`)

* `id` (Primary Key)
* `email` (Unique)
* `password` (Hashed)
* `is_admin` (Boolean)
* `created_at` (Timestamp)

### Products Table (`ecommerce_schema.products`)

* `id` (Primary Key)
* `name`
* `description`
* `price`
* `stock`
* `created_at` (Timestamp)
* `updated_at` (Timestamp)

## Troubleshooting

### Common Issues

1. **Database Connection Error** :

* Verify PostgreSQL is running: `sudo systemctl status postgresql`
* Check database credentials in `.env` file
* Ensure user has proper permissions

1. **Schema/Tables Not Created** :

* Check backend logs for errors
* Verify DATABASE_URL in `.env` is correct
* Restart backend server

1. **CORS Issues** :

* Ensure frontend is running on port 3000
* Backend CORS is configured to allow all origins

1. **Password Hashing Issues** :

* If facing bcrypt errors, the system falls back to SHA256 hashing

### Verification Steps

1. **Check if tables are created** :
   **sql**

   Copy

   Download

```
   \c ecommerce_db
   \dt ecommerce_schema.*
```

1. **Check if users exist** :
   **sql**

   Copy

   Download

```
   SELECT * FROM ecommerce_schema.users;
```

1. **Test API endpoints** :
   **bash**

   Copy

   Download

```
   curl http://localhost:8000/
```

## Development

### Project Structure

**text**

Copy

Download

```
ecommerce-app/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── database.py      # Database configuration
│   │   ├── auth.py          # Authentication utilities
│   │   └── crud.py          # Database operations
│   ├── requirements.txt     # Python dependencies
│   └── .env                # Environment variables
├── frontend/
│   ├── index.html          # Home page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── products.html       # Products management
│   ├── styles.css          # CSS styles
│   └── app.js              # Frontend JavaScript
└── README.md
```

### Adding New Features

1. **Backend** :

* Add new models in `models.py`
* Create API endpoints in `main.py`
* Add business logic in `crud.py`

1. **Frontend** :

* Create new HTML pages
* Update `app.js` with new functionality
* Style with `styles.css`

## License

This project is for educational purposes.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Verify all setup steps are completed
3. Check server logs for error messages
4. Ensure all dependencies are installed

---

 **Note** : This is a development setup. For production, consider:

* Using environment variables for all secrets
* Setting up proper CORS origins
* Implementing input validation
* Adding rate limiting
* Using HTTPS
* Database connection pooling
