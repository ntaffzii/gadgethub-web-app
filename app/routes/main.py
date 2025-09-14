# app/routes/main.py
from flask import Blueprint, render_template, jsonify
from app.extensions import db
from app.models.user import User
from sqlalchemy import text

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return jsonify({
        'message': 'Welcome to GadgetHub!',
        'status': 'success',
        'database': 'connected' if db.engine else 'not connected'
    })

@bp.route('/test-db')
def test_db():
    try:
        # ทดสอบการเชื่อมต่อ database
        result = db.session.execute(text('SELECT VERSION()'))
        version = result.fetchone()[0]
        
        # ทดสอบสร้าง user
        user_count = User.query.count()
        
        return jsonify({
            'database': 'connected',
            'mysql_version': version,
            'user_count': user_count,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'database': 'error',
            'error': str(e),
            'status': 'failed'
        }), 500