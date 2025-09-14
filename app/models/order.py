from app.extensions import db
from datetime import datetime
from sqlalchemy import DECIMAL

class Order(db.Model):
    __tablename__ = 'orders'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Order Number
    order_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Order Status
    status = db.Column(db.String(20), nullable=False, default='pending', index=True)
    # Status options: pending, confirmed, processing, shipped, delivered, cancelled
    
    # Financial Information
    subtotal = db.Column(db.DECIMAL(10, 2), nullable=False)
    shipping_cost = db.Column(db.DECIMAL(10, 2), nullable=False, default=0)
    tax_amount = db.Column(db.DECIMAL(10, 2), nullable=False, default=0)
    discount_amount = db.Column(db.DECIMAL(10, 2), nullable=False, default=0)
    total_amount = db.Column(db.DECIMAL(10, 2), nullable=False)

    # Shipping Information
    shipping_name = db.Column(db.String(100), nullable=False)
    shipping_phone = db.Column(db.String(20), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    shipping_city = db.Column(db.String(100), nullable=False)
    shipping_postal_code = db.Column(db.String(10), nullable=False)
    
    # Payment Information
    payment_method = db.Column(db.String(50), nullable=True)
    payment_status = db.Column(db.String(20), nullable=False, default='pending')
    # Payment status: pending, paid, failed, refunded
    
    # Notes
    notes = db.Column(db.Text, nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    shipped_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    # Methods
    def generate_order_number(self):
        """สร้างเลขที่ใบสั่งซื้อ"""
        from datetime import datetime
        now = datetime.utcnow()
        return f"GH{now.strftime('%Y%m%d')}{self.id:04d}"
    
    def get_item_count(self):
        """นับจำนวนรายการสินค้า"""
        return sum(item.quantity for item in self.items)
    
    def __repr__(self):
        return f'<Order {self.order_number}>'