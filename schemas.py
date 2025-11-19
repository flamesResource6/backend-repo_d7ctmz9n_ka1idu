"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: Optional[str] = Field(None, description="Address")
    phone: Optional[str] = Field(None, description="Phone number")
    is_active: bool = Field(True, description="Whether user is active")

class MenuItem(BaseModel):
    """
    Menu items available for ordering
    Collection name: "menuitem"
    """
    name: str = Field(..., description="Dish name")
    description: Optional[str] = Field(None, description="Dish description")
    price: float = Field(..., ge=0, description="Price in dollars")
    image: Optional[str] = Field(None, description="Image URL")
    category: str = Field("General", description="Category like Pizza, Burgers, Drinks")
    available: bool = Field(True, description="Whether item is available")

class OrderItem(BaseModel):
    item_id: str = Field(..., description="ID of MenuItem")
    quantity: int = Field(1, ge=1, description="Quantity of the item")

class Order(BaseModel):
    """
    Orders placed by users
    Collection name: "order"
    """
    customer_name: str = Field(..., description="Customer full name")
    customer_phone: str = Field(..., description="Customer phone")
    customer_address: str = Field(..., description="Delivery address")
    items: List[OrderItem] = Field(..., description="Items in the order")
    subtotal: float = Field(..., ge=0, description="Subtotal before fees")
    delivery_fee: float = Field(0, ge=0, description="Delivery fee")
    total: float = Field(..., ge=0, description="Order total amount")
    status: str = Field("pending", description="Order status: pending, confirmed, delivered, cancelled")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# The Flames database viewer can read these models from GET /schema
