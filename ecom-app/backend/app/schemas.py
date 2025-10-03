from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int

class ProductUpdate(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    stock: int = None

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    is_admin: bool

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    created_at: str
    updated_at: str