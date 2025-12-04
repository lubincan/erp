"""
应用配置文件
"""
import os
from datetime import timedelta


class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 打卡相关配置
    WORK_START_TIME = '09:00'  # 上班时间
    WORK_END_TIME = '18:00'    # 下班时间
    LATE_THRESHOLD_MINUTES = 30  # 迟到阈值（分钟）


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///erp.db'


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///erp.db'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

