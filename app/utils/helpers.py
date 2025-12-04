"""
辅助工具函数
"""
from datetime import datetime, date
from functools import wraps
from flask import request, jsonify, session
from app.models import User


def json_response(data=None, message='success', code=200):
    """统一JSON响应格式"""
    return jsonify({
        'code': code,
        'message': message,
        'data': data
    }), code


def error_response(message='error', code=400):
    """错误响应"""
    return jsonify({
        'code': code,
        'message': message,
        'data': None
    }), code


def login_required(f):
    """登录验证装饰器（简化版，实际应该使用JWT）"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从session中获取user_id
        if 'user_id' not in session:
            return error_response('请先登录', 401)

        user_id = session['user_id']
        user = User.query.get(user_id)
        if not user:
            return error_response('用户不存在', 404)

        if user.status != 'active':
            return error_response('用户已被禁用', 403)

        # 将用户对象添加到请求上下文
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function

