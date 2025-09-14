from app.extensions import db
from datetime import datetime
from sqlalchemy import DECIMAL

class Product(db.Model):
    __tablename__ = 'products'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Information
    name = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    short_description = db.Column(db.String(255), nullable=True)
    
    # Pricing
    price = db.Column(DECIMAL(10, 2), nullable=False, index=True)
    original_price = db.Column(DECIMAL(10, 2), nullable=True)  # สำหรับโปรโมชั่น
    cost = db.Column(DECIMAL(10, 2), nullable=True)  # ราคาทุน

    # Product Details
    brand = db.Column(db.String(100), nullable=True, index=True)
    model = db.Column(db.String(100), nullable=True)
    sku = db.Column(db.String(50), unique=True, nullable=True, index=True)
    
    # Inventory
    stock_quantity = db.Column(db.Integer, default=0, nullable=False)
    min_stock_level = db.Column(db.Integer, default=5, nullable=False)
    
    # Product Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    
    # Media
    main_image = db.Column(db.String(255), nullable=True)
    images = db.Column(db.JSON, nullable=True)  # List of image URLs
    
    # Specifications (JSON field for flexible product attributes)
    specifications = db.Column(db.JSON, nullable=True)
    
    # SEO
    meta_title = db.Column(db.String(60), nullable=True)
    meta_description = db.Column(db.String(160), nullable=True)
    
    # Metrics
    view_count = db.Column(db.Integer, default=0, nullable=False)
    sales_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Foreign Keys
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cart_items = db.relationship('Cart', backref='product', lazy='dynamic')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    reviews = db.relationship('Review', backref='product', lazy='dynamic')
    
    # Methods
    @property
    def is_on_sale(self):
        """ตรวจสอบว่าสินค้าลดราคาหรือไม่"""
        return self.original_price and self.original_price > self.price
    
    @property
    def discount_percentage(self):
        """คำนวณเปอร์เซ็นต์ส่วนลด"""
        if self.is_on_sale:
            return int((self.original_price - self.price) / self.original_price * 100)
        return 0
    
    @property
    def is_in_stock(self):
        """ตรวจสอบว่ามีสินค้าในสต็อก"""
        return self.stock_quantity > 0
    
    @property
    def is_low_stock(self):
        """ตรวจสอบว่าสินค้าใกล้หมด"""
        return self.stock_quantity <= self.min_stock_level
    
    def get_average_rating(self):
        """คำนวณคะแนนรีวิวเฉลี่ย"""
        if self.reviews.count() == 0:
            return 0
        total = sum(review.rating for review in self.reviews)
        return round(total / self.reviews.count(), 1)
    
    def __repr__(self):
        return f'<Product {self.name}>'
