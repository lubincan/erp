"""
ERP系统应用初始化
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
import os

# 初始化扩展
db = SQLAlchemy()
cors = CORS()


def create_app(config_name='development'):
    """
    应用工厂函数
    """
    app = Flask(__name__)
    
    # 配置
    if config_name == 'development':
        # 开发环境配置
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'DATABASE_URL', 
            'sqlite:///erp.db'
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = True
    else:
        # 生产环境配置
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = False
    
    # 初始化扩展
    db.init_app(app)
    cors.init_app(app)
    
    # 配置Swagger文档
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "ERP系统 API 文档",
            "description": "ERP企业资源规划系统 - 员工打卡管理API文档",
            "version": "1.0.0",
            "contact": {
                "name": "ERP系统",
                "url": "http://127.0.0.1:5000"
            }
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "tags": [
            {
                "name": "打卡管理",
                "description": "员工打卡相关API接口"
            }
        ]
    }
    
    # 初始化Swagger
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # 注册蓝图
    from app.views import attendance_bp, index_bp, docs_bp, auth_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(docs_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
        # 初始化默认管理员账户
        from app.models import User
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password='admin123',  # 实际应用中应该加密
                name='系统管理员',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
    
    return app

