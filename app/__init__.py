from flask import Flask
from flask_login import LoginManager
from app.extensions import db  # ✅ import db จาก extensions

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config.from_object('config.Config')  # ถ้ามี config แยกไว้

    from datetime import timedelta

    # ตั้งเวลา session ให้หมดอายุใน 30 นาที
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    
    # ✅ เชื่อม SQLAlchemy กับ app
    db.init_app(app)

    # ✅ เชื่อม LoginManager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'กรุณาเข้าสู่ระบบเพื่อเข้าถึงหน้านี้'
    login_manager.login_message_category = 'warning'

    # ✅ import model หลังจาก db.init_app
    with app.app_context():
        from app.models.user import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    # ✅ ลงทะเบียน Blueprints
    from app.routes.auth import bp as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.routes.main import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    return app