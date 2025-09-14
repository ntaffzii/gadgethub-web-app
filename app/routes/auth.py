from flask import Blueprint, render_template, redirect, session, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.extensions import db
from app.models.user import User
from app.forms import LoginForm, RegistrationForm
from datetime import datetime
import re

bp = Blueprint('auth', __name__)

@bp.route('/logout')
def logout():
    """Route for logging out the user."""
    logout_user()
    flash('คุณได้ออกจากระบบเรียบร้อยแล้ว', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Route for user login."""
    # Redirect if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))

    form = LoginForm()
    if form.validate_on_submit():
        # The LoginForm's custom validators have already found the user
        # and checked the password. The user object is stored in form.user.
        user = form.user
        
        # Log the user in with Flask-Login
        login_user(user, remember=form.remember_me.data)
        session.permanent = True  # ✅ เพิ่มตรงนี้

        
        # Get the 'next' URL parameter if it exists
        next_page = request.args.get('next')
        
        flash(f'ยินดีต้อนรับกลับ, {user.username}!', 'success')
        
        # Redirect to the 'next' page or the default home page
        return redirect(next_page or url_for('auth.home'))
    
    # If the form is not submitted or validation fails, re-render the login page
    return render_template('auth/login.html', title='เข้าสู่ระบบ', form=form)

@bp.route('/home')
def home():
    """หน้าหลักของเว็บไซต์ (สมมติว่าเป็นหน้าสำหรับล็อกอินแล้ว)"""
    return render_template('auth/home.html', title='หน้าแรก')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """หน้าสมัครสมาชิก"""
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            # สร้าง User object ใหม่
            user = User(
                username=form.username.data,
                email=form.email.data.lower(),  # เก็บ email เป็นตัวเล็ก
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone=form.phone.data if form.phone.data else None
            )
            
            # เซ็ตรหัสผ่าน (จะถูก hash อัตโนมัติ)
            user.set_password(form.password.data)
            
            # บันทึกลงฐานข้อมูล
            db.session.add(user)
            db.session.commit()
            
            # แสดงข้อความสำเร็จ
            flash(f'ยินดีต้อนรับ {user.first_name}! สมัครสมาชิกสำเร็จแล้ว', 'success')
            flash('กรุณาเข้าสู่ระบบเพื่อเริ่มใช้งาน', 'info')
            
            # redirect ไปหน้า login
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            # ถ้าเกิดข้อผิดพลาด rollback และแสดงข้อความ
            db.session.rollback()
            flash('เกิดข้อผิดพลาดในการสมัครสมาชิก กรุณาลองใหม่อีกครั้ง', 'danger')
            print(f"Registration error: {str(e)}")  # สำหรับ debug
    
    return render_template('auth/register.html', form=form, title='สมัครสมาชิก')

@bp.route('/check-username')
def check_username():
    """API สำหรับตรวจสอบ username แบบ real-time"""
    username = request.args.get('username', '').strip()
    
    if not username:
        return {'available': False, 'message': 'กรุณากรอกชื่อผู้ใช้'}
    
    if len(username) < 3:
        return {'available': False, 'message': 'ชื่อผู้ใช้ต้องมีอย่างน้อย 3 ตัวอักษร'}
    
    # ตรวจสอบรูปแบบ
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return {'available': False, 'message': 'ใช้ได้เฉพาะตัวอักษร ตัวเลข - และ _'}
    
    # ตรวจสอบในฐานข้อมูล
    user = User.query.filter_by(username=username).first()
    if user:
        return {'available': False, 'message': 'ชื่อผู้ใช้นี้ถูกใช้แล้ว'}
    
    return {'available': True, 'message': 'ชื่อผู้ใช้นี้ใช้ได้'}

@bp.route('/check-email')
def check_email():
    """API สำหรับตรวจสอบ email แบบ real-time"""
    email = request.args.get('email', '').strip().lower()
    
    if not email:
        return {'available': False, 'message': 'กรุณากรอกอีเมล'}
    
    # ตรวจสอบรูปแบบ email พื้นฐาน
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return {'available': False, 'message': 'รูปแบบอีเมลไม่ถูกต้อง'}
    
    # ตรวจสอบในฐานข้อมูล
    user = User.query.filter_by(email=email).first()
    if user:
        return {'available': False, 'message': 'อีเมลนี้ถูกใช้แล้ว'}
    
    return {'available': True, 'message': 'อีเมลนี้ใช้ได้'}