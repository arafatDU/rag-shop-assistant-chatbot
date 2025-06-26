from sqlalchemy import Column, Integer, String, Float, Text
from .init_db import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    ProductID = Column(String, unique=True, index=True)
    ProductName = Column(String, index=True)
    ProductBrand = Column(String)
    Gender = Column(String)
    Price = Column(Float)
    Description = Column(Text)
    PrimaryColor = Column(String)
    
    def __repr__(self):
        return f"<Product(id={self.id}, ProductName='{self.ProductName}')>"
