"""
用户模型
"""
from app import db
from datetime import datetime


class User(db.Model):
    """用户表"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名')
    password = db.Column(db.String(255), nullable=False, comment='密码')
    name = db.Column(db.String(100), nullable=False, comment='姓名')
    email = db.Column(db.String(100), comment='邮箱')
    phone = db.Column(db.String(20), comment='手机号')
    role = db.Column(db.String(20), default='employee', comment='角色：admin-管理员, employee-员工')
    status = db.Column(db.String(10), default='active', comment='状态：active-激活, inactive-禁用')
    last_login = db.Column(db.DateTime, comment='最后登录时间')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关联关系
    attendance_records = db.relationship('AttendanceRecord', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'status': self.status,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

