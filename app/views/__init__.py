"""
视图/路由模块
"""
from app.views.index import index_bp
from app.views.attendance import attendance_bp
from app.views.docs import docs_bp
from app.views.auth import auth_bp

__all__ = ['index_bp', 'attendance_bp', 'docs_bp', 'auth_bp']

