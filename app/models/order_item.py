from app.extensions import db
from datetime import datetime
from sqlalchemy import DECIMAL

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    
    # Item Details
    product_name = db.Column(db.String(200), nullable=False)  # Snapshot ชื่อสินค้าตอนสั่งซื้อ
    product_sku = db.Column(db.String(50), nullable=True)
    unit_price = db.Column(DECIMAL(10, 2), nullable=False)  # ราคาตอนสั่งซื้อ
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(DECIMAL(10, 2), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<OrderItem {self.product_name} x{self.quantity}>'