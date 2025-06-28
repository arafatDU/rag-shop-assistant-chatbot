from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from database.init_db import get_db
from database.models import Product
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/products")
def get_products(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    """Get paginated products from PostgreSQL database"""
    try:
        # Calculate offset for pagination
        offset = (page - 1) * page_size
        
        # Query with pagination and limit
        products = db.query(Product).offset(offset).limit(page_size).all()
        
        # Convert SQLAlchemy objects to dictionaries
        products_dict = []
        for product in products:
            products_dict.append({
                "id": product.id,
                "ProductID": product.ProductID,
                "ProductName": product.ProductName,
                "ProductBrand": product.ProductBrand,
                "Gender": product.Gender,
                "Price": product.Price,
                "Description": product.Description,
                "PrimaryColor": product.PrimaryColor
            })
        
        return products_dict
        
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=503, detail="Database connection temporarily unavailable")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/products/summary")
def get_products_summary(db: Session = Depends(get_db)):
    """Get summary information about products"""
    try:
        total_count = db.query(Product).count()
        brands = db.query(Product.ProductBrand).distinct().all()
        genders = db.query(Product.Gender).distinct().all()
        colors = db.query(Product.PrimaryColor).distinct().all()
        
        return {
            "total_products": total_count,
            "brands": [b[0] for b in brands if b[0]],
            "genders": [g[0] for g in genders if g[0]],
            "colors": [c[0] for c in colors if c[0]]
        }
        
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=503, detail="Database connection temporarily unavailable")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")