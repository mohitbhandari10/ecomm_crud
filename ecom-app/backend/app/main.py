from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Dict, Any
from typing_extensions import Annotated

from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db, engine
from app.models import Base, User
from app.auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from app.crud import create_user, get_user_by_email, create_product, get_products, get_product, update_product, delete_product
from app.schemas import ProductCreate, ProductUpdate, UserCreate, UserResponse, LoginResponse, ProductResponse

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ecommerce API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth endpoints
@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = create_user(db=db, user=user)
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        is_admin=new_user.is_admin
    )

# @app.post("/login", response_model=LoginResponse)
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires
#     )
#     return LoginResponse(
#         access_token=access_token,
#         token_type="bearer",
#         user_id=user.id,
#         is_admin=user.is_admin
#     )

@app.post("/login", response_model=LoginResponse)
def login(form_data: dict, db: Session = Depends(get_db)):
    email = form_data.get("email")
    password = form_data.get("password")
    
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email and password are required",
        )
    
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        is_admin=user.is_admin
    )

# Product endpoints
@app.get("/products", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return [
        ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            created_at=product.created_at.isoformat(),
            updated_at=product.updated_at.isoformat()
        )
        for product in products
    ]

@app.post("/products", response_model=ProductResponse)
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    new_product = create_product(db=db, product=product)
    return ProductResponse(
        id=new_product.id,
        name=new_product.name,
        description=new_product.description,
        price=new_product.price,
        stock=new_product.stock,
        created_at=new_product.created_at.isoformat(),
        updated_at=new_product.updated_at.isoformat()
    )

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product_endpoint(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    updated_product = update_product(db=db, product_id=product_id, product=product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(
        id=updated_product.id,
        name=updated_product.name,
        description=updated_product.description,
        price=updated_product.price,
        stock=updated_product.stock,
        created_at=updated_product.created_at.isoformat(),
        updated_at=updated_product.updated_at.isoformat()
    )

@app.delete("/products/{product_id}")
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    success = delete_product(db=db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@app.get("/")
def read_root():
    return {"message": "Ecommerce API is running"}  