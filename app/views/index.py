"""
首页路由
"""
from flask import Blueprint, render_template_string, redirect, url_for, session
from app.models import User

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    """首页"""
    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect('/api/auth/login')

    user = User.query.get(session['user_id'])
    if not user:
        return redirect('/api/auth/login')

    html = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ERP系统 - 员工打卡</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Microsoft YaHei', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
                max-width: 800px;
                width: 100%;
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 30px;
                font-size: 32px;
            }
            .nav {
                display: flex;
                gap: 10px;
                margin-bottom: 30px;
                flex-wrap: wrap;
            }
            .nav a {
                flex: 1;
                padding: 15px 20px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 10px;
                text-align: center;
                transition: all 0.3s;
                min-width: 150px;
            }
            .nav a:hover {
                background: #764ba2;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .info {
                background: #f5f5f5;
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
            }
            .info h2 {
                color: #667eea;
                margin-bottom: 15px;
            }
            .info p {
                line-height: 1.8;
                color: #666;
                margin-bottom: 10px;
            }
            .info code {
                background: #e0e0e0;
                padding: 2px 6px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏢 ERP企业资源规划系统</h1>
            <div style="text-align: center; margin-bottom: 20px;">
                <span style="color: white; font-size: 16px;">欢迎您，{{ user.name }} ({{ user.username }})</span>
            </div>
            <div class="nav">
                <a href="/api/attendance/">员工打卡</a>
                <a href="/api/auth/profile">个人资料</a>
                <a href="/api/docs" target="_blank">Swagger API文档</a>
                <a href="/api/attendance/records?user_id={{ user.id }}" target="_blank">查看打卡记录</a>
                <a href="/api/auth/logout" style="background: #dc3545;">退出登录</a>
            </div>
            <div class="info">
                <h2>📋 系统说明</h2>
                <p><strong>当前功能：</strong>员工打卡系统</p>
                <p><strong>默认管理员账户：</strong></p>
                <p>用户名: <code>admin</code> | 密码: <code>admin123</code></p>
                <p><strong>API文档：</strong></p>
                <p>• <a href="/api/docs" target="_blank" style="color: #667eea;">Swagger UI 在线文档</a> - 交互式API文档，支持在线测试</p>
                <p><strong>API接口：</strong></p>
                <p>• 上班打卡: <code>POST /api/attendance/checkin?user_id={{ user.id }}</code></p>
                <p>• 下班打卡: <code>POST /api/attendance/checkout?user_id={{ user.id }}</code></p>
                <p>• 查询记录: <code>GET /api/attendance/records?user_id={{ user.id }}</code></p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, user=user)


@index_bp.route('/attendance')
def attendance_redirect():
    """打卡页面重定向"""
    from app.views.attendance import attendance_page
    return attendance_page()

