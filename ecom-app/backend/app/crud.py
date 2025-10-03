from sqlalchemy.orm import Session
from app.models import Product, User
from app.auth import get_password_hash

def create_user(db: Session, user):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_product(db: Session, product):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: Session, product_id: int, product):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        if product.name is not None:
            db_product.name = product.name
        if product.description is not None:
            db_product.description = product.description
        if product.price is not None:
            db_product.price = product.price
        if product.stock is not None:
            db_product.stock = product.stock
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False