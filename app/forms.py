from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.user import User
import re

class LoginForm(FlaskForm):
    """Form สำหรับเข้าสู่ระบบ"""

    username_or_email = StringField('ชื่อผู้ใช้หรืออีเมล', validators=[DataRequired(message='กรุณากรอกชื่อผู้ใช้หรืออีเมล')])
    password = PasswordField('รหัสผ่าน', validators=[DataRequired(message='กรุณากรอกรหัสผ่าน')])
    remember_me = BooleanField('จดจำฉัน')
    submit = SubmitField('เข้าสู่ระบบ')
    
    # Custom Validator
    def validate_username_or_email(self, field):
        """
        ตรวจสอบว่าชื่อผู้ใช้หรืออีเมลมีอยู่ในฐานข้อมูลหรือไม่
        และเชื่อมโยงข้อมูลผู้ใช้กับฟอร์ม
        """
        user = User.query.filter_by(username=field.data).first()
        if not user:
            user = User.query.filter_by(email=field.data.lower()).first()
        
        if not user:
            raise ValidationError('ชื่อผู้ใช้หรืออีเมลไม่ถูกต้อง')

        self.user = user

    def validate_password(self, password):
        """ตรวจสอบรหัสผ่านที่กรอกว่าตรงกับที่บันทึกไว้ในฐานข้อมูลหรือไม่"""
        if hasattr(self, 'user') and not self.user.check_password(password.data):
            raise ValidationError('รหัสผ่านไม่ถูกต้อง')

class RegistrationForm(FlaskForm):
    """Form สำหรับสมัครสมาชิก"""
    
    # Basic Information
    username = StringField('ชื่อผู้ใช้', validators=[
        DataRequired(message='กรุณากรอกชื่อผู้ใช้'),
        Length(min=3, max=20, message='ชื่อผู้ใช้ต้องมี 3-20 ตัวอักษร')
    ])
    
    email = StringField('อีเมล', validators=[
        DataRequired(message='กรุณากรอกอีเมล'),
        Email(message='รูปแบบอีเมลไม่ถูกต้อง')
    ])
    
    # Personal Information
    first_name = StringField('ชื่อ', validators=[
        DataRequired(message='กรุณากรอกชื่อ'),
        Length(min=2, max=50, message='ชื่อต้องมี 2-50 ตัวอักษร')
    ])
    
    last_name = StringField('นามสกุล', validators=[
        DataRequired(message='กรุณากรอกนามสกุล'),
        Length(min=2, max=50, message='นามสกุลต้องมี 2-50 ตัวอักษร')
    ])
    
    phone = StringField('เบอร์โทรศัพท์', validators=[
        Length(min=10, max=15, message='เบอร์โทรต้องมี 10-15 หลัก')
    ])
    
    # Password
    password = PasswordField('รหัสผ่าน', validators=[
        DataRequired(message='กรุณากรอกรหัสผ่าน'),
        Length(min=6, message='รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร')
    ])
    
    confirm_password = PasswordField('ยืนยันรหัสผ่าน', validators=[
        DataRequired(message='กรุณายืนยันรหัสผ่าน'),
        EqualTo('password', message='รหัsผ่านไม่ตรงกัน')
    ])
    
    # Terms and Conditions
    agree_terms = BooleanField('ฉันยอมรับ', validators=[
        DataRequired(message='กรุณายอมรับเงื่อนไขการใช้งาน')
    ])
    
    submit = SubmitField('สมัครสมาชิก')
    
    # Custom Validators
    def validate_username(self, username):
        """ตรวจสอบว่า username ซ้ำหรือไม่"""
        # ตรวจสอบรูปแบบ username (ตัวอักษร ตัวเลข _ - เท่านั้น)
        if not re.match(r'^[a-zA-Z0-9_-]+$', username.data):
            raise ValidationError('ชื่อผู้ใช้ใช้ได้เฉพาะตัวอักษร ตัวเลข - และ _ เท่านั้น')
        
        # ตรวจสอบว่ามีอยู่ในฐานข้อมูลแล้วหรือไม่
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('ชื่อผู้ใช้นี้ถูกใช้แล้ว กรุณาเลือกชื่ออื่น')
    
    def validate_email(self, email):
        """ตรวจสอบว่า email ซ้ำหรือไม่"""
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('อีเมลนี้ถูกใช้แล้ว กรุณาใช้อีเมลอื่น')
    
    def validate_password(self, password):
        """ตรวจสอบความแข็งแกร่งของรหัสผ่าน"""
        password_str = password.data
        
        # ตรวจสอบว่ามีตัวพิมพ์ใหญ่
        if not re.search(r'[A-Z]', password_str):
            raise ValidationError('รหัสผ่านต้องมีตัวพิมพ์ใหญ่อย่างน้อย 1 ตัว')
        
        # ตรวจสอบว่ามีตัวพิมพ์เล็ก
        if not re.search(r'[a-z]', password_str):
            raise ValidationError('รหัสผ่านต้องมีตัวพิมพ์เล็กอย่างน้อย 1 ตัว')
        
        # ตรวจสอบว่ามีตัวเลข
        if not re.search(r'[0-9]', password_str):
            raise ValidationError('รหัสผ่านต้องมีตัวเลขอย่างน้อย 1 ตัว')
    
    def validate_phone(self, phone):
        """ตรวจสอบรูปแบบเบอร์โทร"""
        if phone.data:
            # ลบขีดกลางและช่องว่าง
            phone_clean = re.sub(r'[-\s]', '', phone.data)
            
            # ตรวจสอบว่าเป็นตัวเลขทั้งหมด
            if not phone_clean.isdigit():
                raise ValidationError('เบอร์โทรต้องเป็นตัวเลขเท่านั้น')
            
            # ตรวจสอบรูปแบบเบอร์ไทย
            if not re.match(r'^(0[689]{1}[0-9]{8}|0[2-7]{1}[0-9]{7})$', phone_clean):
                raise ValidationError('รูปแบบเบอร์โทรไม่ถูกต้อง')