from app.extensions import db
from datetime import datetime

class Cart(db.Model):
    __tablename__ = 'cart'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    
    # Cart Details
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Timestamps
    added_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='unique_user_product'),
    )
    
    # Methods
    @property
    def total_price(self):
        """คำนวณราคารวมของรายการนี้"""
        return self.quantity * self.product.price
    
    def __repr__(self):
        return f'<Cart User:{self.user_id} Product:{self.product_id} Qty:{self.quantity}>'