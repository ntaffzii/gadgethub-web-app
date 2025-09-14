from app.extensions import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'categories'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Category Information
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Display Options
    icon = db.Column(db.String(50), nullable=True)  # Font Awesome icon class
    image_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    
    # SEO Fields
    meta_title = db.Column(db.String(60), nullable=True)
    meta_description = db.Column(db.String(160), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def get_product_count(self):
        """นับจำนวนสินค้าในหมวดหมู่"""
        return self.products.filter_by(is_active=True).count()
    
    def __repr__(self):
        return f'<Category {self.name}>'