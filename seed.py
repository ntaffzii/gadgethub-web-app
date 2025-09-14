from app import create_app, db
from app.models import Category, Product

app = create_app()

def init_database():
    """สร้างตารางและใส่ข้อมูลเริ่มต้น"""
    from app import db
    
    # Drop all tables (ระวัง! จะลบข้อมูลทั้งหมด)
    print("Dropping all tables...")
    db.drop_all()
    
    # Create all tables
    print("Creating all tables...")
    db.create_all()
    
    print("Database initialized successfully!")

def seed_sample_data():
    """ใส่ข้อมูลตัวอย่าง"""
    from app import db
    
    print("Seeding sample data...")
    
    # 1. Create Categories
    categories_data = [
        {
            'name': 'สมาร์ทโฟน',
            'slug': 'smartphones',
            'description': 'โทรศัพท์มือถือและสมาร์ทโฟนทุกยี่ห้อ',
            'icon': 'fas fa-mobile-alt',
            'sort_order': 1
        },
        {
            'name': 'แล็ปท็อป',
            'slug': 'laptops',
            'description': 'คอมพิวเตอร์พกพาและแล็ปท็อป',
            'icon': 'fas fa-laptop',
            'sort_order': 2
        },
        {
            'name': 'อุปกรณ์เสริม',
            'slug': 'accessories',
            'description': 'อุปกรณ์เสริมและอะไหล่',
            'icon': 'fas fa-headphones',
            'sort_order': 3
        },
        {
            'name': 'แท็บเล็ต',
            'slug': 'tablets',
            'description': 'แท็บเล็ตและอีรีดเดอร์',
            'icon': 'fas fa-tablet-alt',
            'sort_order': 4
        },
        {
            'name': 'สมาร์ทวอทช์',
            'slug': 'smartwatches',
            'description': 'นาฬิกาอัจฉริยะและเครื่องสวมใส่',
            'icon': 'fas fa-clock',
            'sort_order': 5
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.session.add(category)
        categories.append(category)
    
    db.session.commit()
    print(f"Created {len(categories)} categories")
    
    # 2. Create Products
    products_data = [
        # Smartphones
        {
            'name': 'iPhone 15 Pro Max',
            'slug': 'iphone-15-pro-max',
            'description': 'โทรศัพท์ iPhone รุ่นล่าสุดด้วยชิป A17 Pro',
            'short_description': 'iPhone 15 Pro Max 256GB Natural Titanium',
            'price': 45900.00,
            'original_price': 48900.00,
            'brand': 'Apple',
            'model': 'iPhone 15 Pro Max',
            'sku': 'IPH15PM256NT',
            'stock_quantity': 25,
            'category_id': 1,
            'is_featured': True,
            'main_image': '/static/images/iphone-15-pro-max.jpg',
            'specifications': {
                'screen': '6.7" Super Retina XDR',
                'processor': 'A17 Pro chip',
                'storage': '256GB',
                'camera': '48MP + 12MP + 12MP',
                'battery': 'Up to 29 hours video playback'
            }
        },
        {
            'name': 'Samsung Galaxy S24 Ultra',
            'slug': 'samsung-galaxy-s24-ultra',
            'description': 'สมาร์ทโฟน Samsung Galaxy S24 Ultra พร้อม S Pen',
            'short_description': 'Galaxy S24 Ultra 512GB Titanium Gray',
            'price': 42900.00,
            'brand': 'Samsung',
            'model': 'Galaxy S24 Ultra',
            'sku': 'SGS24U512TG',
            'stock_quantity': 18,
            'category_id': 1,
            'is_featured': True,
            'main_image': '/static/images/galaxy-s24-ultra.jpg'
        },
        
        # Laptops
        {
            'name': 'MacBook Pro 16" M3 Max',
            'slug': 'macbook-pro-16-m3-max',
            'description': 'MacBook Pro 16 นิ้วพร้อมชิป M3 Max',
            'short_description': 'MacBook Pro 16" M3 Max 1TB Space Black',
            'price': 109900.00,
            'brand': 'Apple',
            'model': 'MacBook Pro 16"',
            'sku': 'MBP16M3MAX1TB',
            'stock_quantity': 12,
            'category_id': 2,
            'is_featured': True,
            'main_image': '/static/images/macbook-pro-16.jpg'
        },
        {
            'name': 'ASUS ROG Strix G16',
            'slug': 'asus-rog-strix-g16',
            'description': 'เกมมิ่งแล็ปท็อป ASUS ROG Strix G16',
            'short_description': 'ROG Strix G16 RTX 4070 32GB RAM',
            'price': 54900.00,
            'original_price': 59900.00,
            'brand': 'ASUS',
            'model': 'ROG Strix G16',
            'sku': 'ROGSTG16RTX4070',
            'stock_quantity': 8,
            'category_id': 2,
            'main_image': '/static/images/asus-rog-strix.jpg'
        },
        
        # Accessories
        {
            'name': 'AirPods Pro (3rd Generation)',
            'slug': 'airpods-pro-3rd-gen',
            'description': 'หูฟังไร้สาย AirPods Pro รุ่นที่ 3',
            'short_description': 'AirPods Pro 3 with MagSafe Case',
            'price': 8900.00,
            'brand': 'Apple',
            'model': 'AirPods Pro 3',
            'sku': 'APP3MAGSAFE',
            'stock_quantity': 45,
            'category_id': 3,
            'is_featured': True,
            'main_image': '/static/images/airpods-pro.jpg'
        },
        
        # Tablets
        {
            'name': 'iPad Pro 12.9" M2',
            'slug': 'ipad-pro-12-9-m2',
            'description': 'iPad Pro 12.9 นิ้วพร้อมชิป M2',
            'short_description': 'iPad Pro 12.9" M2 512GB Wi-Fi + Cellular',
            'price': 38900.00,
            'brand': 'Apple',
            'model': 'iPad Pro 12.9"',
            'sku': 'IPP129M2512WC',
            'stock_quantity': 15,
            'category_id': 4,
            'main_image': '/static/images/ipad-pro-129.jpg'
        },
        
        # Smartwatches
        {
            'name': 'Apple Watch Ultra 2',
            'slug': 'apple-watch-ultra-2',
            'description': 'นาฬิกา Apple Watch Ultra 2 รุ่นท็อป',
            'short_description': 'Apple Watch Ultra 2 49mm Natural Titanium',
            'price': 24900.00,
            'brand': 'Apple',
            'model': 'Watch Ultra 2',
            'sku': 'AWU249TNT',
            'stock_quantity': 20,
            'category_id': 5,
            'is_featured': True,
            'main_image': '/static/images/apple-watch-ultra2.jpg'
        }
    ]
    
    # เพิ่มสินค้าเพิ่มเติมให้ครบ 50 รายการ
    additional_products = [
        # เพิ่ม smartphones
        {'name': 'Xiaomi 14 Ultra', 'price': 28900.00, 'brand': 'Xiaomi', 'category_id': 1, 'stock_quantity': 22},
        {'name': 'OPPO Find X7 Pro', 'price': 32900.00, 'brand': 'OPPO', 'category_id': 1, 'stock_quantity': 16},
        {'name': 'Vivo X100 Pro', 'price': 29900.00, 'brand': 'Vivo', 'category_id': 1, 'stock_quantity': 19},
        
        # เพิ่ม laptops
        {'name': 'HP Pavilion Gaming', 'price': 24900.00, 'brand': 'HP', 'category_id': 2, 'stock_quantity': 14},
        {'name': 'Lenovo ThinkPad X1', 'price': 45900.00, 'brand': 'Lenovo', 'category_id': 2, 'stock_quantity': 9},
        {'name': 'Dell XPS 13', 'price': 39900.00, 'brand': 'Dell', 'category_id': 2, 'stock_quantity': 11},
        
        # เพิ่ม accessories
        {'name': 'Sony WH-1000XM5', 'price': 12900.00, 'brand': 'Sony', 'category_id': 3, 'stock_quantity': 35},
        {'name': 'Logitech MX Master 3S', 'price': 3590.00, 'brand': 'Logitech', 'category_id': 3, 'stock_quantity': 50},
        {'name': 'Keychron K2 V2', 'price': 2990.00, 'brand': 'Keychron', 'category_id': 3, 'stock_quantity': 28},
        
        # เพิ่ม tablets
        {'name': 'Samsung Galaxy Tab S9+', 'price': 28900.00, 'brand': 'Samsung', 'category_id': 4, 'stock_quantity': 13},
        {'name': 'Microsoft Surface Pro 9', 'price': 35900.00, 'brand': 'Microsoft', 'category_id': 4, 'stock_quantity': 10},
        
        # เพิ่ม smartwatches
        {'name': 'Samsung Galaxy Watch6', 'price': 9900.00, 'brand': 'Samsung', 'category_id': 5, 'stock_quantity': 24},
        {'name': 'Garmin Forerunner 965', 'price': 19900.00, 'brand': 'Garmin', 'category_id': 5, 'stock_quantity': 17},
    ]
    
    # สร้าง slug และข้อมูลอื่นๆ สำหรับสินค้าเพิ่มเติม
    for i, product_data in enumerate(additional_products):
        product_data['slug'] = product_data['name'].lower().replace(' ', '-')
        product_data['sku'] = f"PROD{1000 + i}"
        product_data['description'] = f"รายละเอียดของ {product_data['name']}"
        product_data['short_description'] = product_data['name']
        product_data['main_image'] = f"/static/images/product-{1000 + i}.jpg"
        
        products_data.append(product_data)
    
    # เพิ่มสินค้าลงฐานข้อมูล
    products = []
    for prod_data in products_data:
        product = Product(**prod_data)
        db.session.add(product)
        products.append(product)
    
    db.session.commit()
    print(f"Created {len(products)} products")
    
if __name__ == '__main__':
    with app.app_context():
        init_database()
        seed_sample_data()
        print("✅ Database setup and sample data seeding completed!")