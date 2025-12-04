"""
用户认证相关路由
"""
from flask import Blueprint, request, render_template_string, redirect, url_for, session, jsonify
from datetime import datetime
from app import db
from app.models import User
from app.utils.helpers import json_response, error_response

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录页面
    """
    if request.method == 'POST':
        # 处理登录请求
        username = request.form.get('username') or request.json.get('username')
        password = request.form.get('password') or request.json.get('password')

        if not username or not password:
            return error_response('请输入用户名和密码', 400)

        # 查询用户
        user = User.query.filter_by(username=username).first()

        if not user:
            return error_response('用户名或密码错误', 401)

        if user.status != 'active':
            return error_response('账户已被禁用', 403)

        # 简单密码验证（实际应用中应该使用密码哈希验证）
        if user.password != password:
            return error_response('用户名或密码错误', 401)

        # 登录成功，创建会话
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role

        # 记录登录时间
        user.last_login = datetime.now()
        db.session.commit()

        return json_response({
            'user_id': user.id,
            'username': user.username,
            'name': user.name,
            'role': user.role
        }, '登录成功')

    # GET请求，显示登录页面
    html = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ERP系统 - 用户登录</title>
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
            .login-container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
                width: 100%;
                max-width: 400px;
            }
            .login-header {
                text-align: center;
                margin-bottom: 30px;
            }
            .login-header h1 {
                color: #333;
                font-size: 32px;
                margin-bottom: 10px;
            }
            .login-header p {
                color: #666;
                font-size: 14px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-group label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: bold;
                font-size: 14px;
            }
            .form-group input {
                width: 100%;
                padding: 12px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 16px;
                transition: all 0.3s;
            }
            .form-group input:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            .login-btn {
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
            }
            .login-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            }
            .login-btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            .error-message {
                background: #f8d7da;
                color: #721c24;
                padding: 10px 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                border: 1px solid #f5c6cb;
                display: none;
            }
            .success-message {
                background: #d4edda;
                color: #155724;
                padding: 10px 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                border: 1px solid #c3e6cb;
                display: none;
            }
            .register-link {
                text-align: center;
                margin-top: 20px;
            }
            .register-link a {
                color: #667eea;
                text-decoration: none;
                font-size: 14px;
            }
            .register-link a:hover {
                text-decoration: underline;
            }
            .footer {
                text-align: center;
                margin-top: 30px;
                color: #666;
                font-size: 12px;
            }
            .loading {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-right: 10px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="login-header">
                <h1>🏢 ERP系统</h1>
                <p>企业资源规划管理系统</p>
            </div>

            <div id="errorMessage" class="error-message"></div>
            <div id="successMessage" class="success-message"></div>

            <form id="loginForm">
                <div class="form-group">
                    <label for="username">用户名</label>
                    <input type="text" id="username" name="username" required placeholder="请输入用户名">
                </div>

                <div class="form-group">
                    <label for="password">密码</label>
                    <input type="password" id="password" name="password" required placeholder="请输入密码">
                </div>

                <button type="submit" id="loginBtn" class="login-btn">
                    <span id="btnText">登录</span>
                </button>
            </form>

            <div class="register-link">
                <a href="/api/auth/register">还没有账号？点击注册</a>
            </div>

            <div class="footer">
                <p>默认管理员：admin / admin123</p>
                <p>© 2024 ERP系统</p>
            </div>
        </div>

        <script>
            const loginForm = document.getElementById('loginForm');
            const loginBtn = document.getElementById('loginBtn');
            const btnText = document.getElementById('btnText');
            const errorMessage = document.getElementById('errorMessage');
            const successMessage = document.getElementById('successMessage');

            function showMessage(message, type = 'error') {
                errorMessage.style.display = 'none';
                successMessage.style.display = 'none';

                if (type === 'error') {
                    errorMessage.textContent = message;
                    errorMessage.style.display = 'block';
                } else {
                    successMessage.textContent = message;
                    successMessage.style.display = 'block';
                }

                // 3秒后自动隐藏
                setTimeout(() => {
                    errorMessage.style.display = 'none';
                    successMessage.style.display = 'none';
                }, 3000);
            }

            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();

                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;

                if (!username || !password) {
                    showMessage('请输入用户名和密码');
                    return;
                }

                // 显示加载状态
                loginBtn.disabled = true;
                btnText.innerHTML = '<span class="loading"></span>登录中...';

                try {
                    const response = await fetch('/api/auth/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: new URLSearchParams({
                            username: username,
                            password: password
                        })
                    });

                    const data = await response.json();

                    if (data.code === 200) {
                        showMessage('登录成功，正在跳转...', 'success');
                        // 1秒后跳转到打卡页面
                        setTimeout(() => {
                            window.location.href = '/api/attendance/';
                        }, 1000);
                    } else {
                        showMessage(data.message || '登录失败');
                    }
                } catch (error) {
                    showMessage('网络错误，请稍后重试');
                } finally {
                    // 恢复按钮状态
                    loginBtn.disabled = false;
                    btnText.textContent = '登录';
                }
            });

            // 回车键提交
            document.getElementById('password').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    loginForm.dispatchEvent(new Event('submit'));
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    用户注册页面
    """
    if request.method == 'POST':
        # 处理注册请求
        username = request.form.get('username') or request.json.get('username')
        password = request.form.get('password') or request.json.get('password')
        name = request.form.get('name') or request.json.get('name')
        email = request.form.get('email') or request.json.get('email')

        if not all([username, password, name]):
            return error_response('请填写必填字段', 400)

        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return error_response('用户名已存在', 400)

        # 创建新用户
        user = User(
            username=username,
            password=password,  # 实际应用中应该加密
            name=name,
            email=email or '',
            role='employee'  # 默认为员工角色
        )

        try:
            db.session.add(user)
            db.session.commit()

            return json_response({
                'user_id': user.id,
                'username': user.username,
                'name': user.name
            }, '注册成功')

        except Exception as e:
            db.session.rollback()
            return error_response(f'注册失败: {str(e)}', 500)

    # GET请求，显示注册页面
    html = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ERP系统 - 用户注册</title>
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
            .register-container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
                width: 100%;
                max-width: 500px;
            }
            .register-header {
                text-align: center;
                margin-bottom: 30px;
            }
            .register-header h1 {
                color: #333;
                font-size: 32px;
                margin-bottom: 10px;
            }
            .register-header p {
                color: #666;
                font-size: 14px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-group label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: bold;
                font-size: 14px;
            }
            .form-group input {
                width: 100%;
                padding: 12px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 16px;
                transition: all 0.3s;
            }
            .form-group input:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            .register-btn {
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
            }
            .register-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            }
            .register-btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            .error-message {
                background: #f8d7da;
                color: #721c24;
                padding: 10px 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                border: 1px solid #f5c6cb;
                display: none;
            }
            .success-message {
                background: #d4edda;
                color: #155724;
                padding: 10px 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                border: 1px solid #c3e6cb;
                display: none;
            }
            .login-link {
                text-align: center;
                margin-top: 20px;
            }
            .login-link a {
                color: #667eea;
                text-decoration: none;
                font-size: 14px;
            }
            .login-link a:hover {
                text-decoration: underline;
            }
            .loading {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-right: 10px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="register-container">
            <div class="register-header">
                <h1>🏢 ERP系统</h1>
                <p>用户注册</p>
            </div>

            <div id="errorMessage" class="error-message"></div>
            <div id="successMessage" class="success-message"></div>

            <form id="registerForm">
                <div class="form-group">
                    <label for="username">用户名 *</label>
                    <input type="text" id="username" name="username" required placeholder="请输入用户名">
                </div>

                <div class="form-group">
                    <label for="name">姓名 *</label>
                    <input type="text" id="name" name="name" required placeholder="请输入真实姓名">
                </div>

                <div class="form-group">
                    <label for="email">邮箱</label>
                    <input type="email" id="email" name="email" placeholder="请输入邮箱地址">
                </div>

                <div class="form-group">
                    <label for="password">密码 *</label>
                    <input type="password" id="password" name="password" required placeholder="请输入密码">
                </div>

                <div class="form-group">
                    <label for="confirm_password">确认密码 *</label>
                    <input type="password" id="confirm_password" name="confirm_password" required placeholder="请再次输入密码">
                </div>

                <button type="submit" id="registerBtn" class="register-btn">
                    <span id="btnText">注册</span>
                </button>
            </form>

            <div class="login-link">
                <a href="/api/auth/login">已有账号？点击登录</a>
            </div>
        </div>

        <script>
            const registerForm = document.getElementById('registerForm');
            const registerBtn = document.getElementById('registerBtn');
            const btnText = document.getElementById('btnText');
            const errorMessage = document.getElementById('errorMessage');
            const successMessage = document.getElementById('successMessage');

            function showMessage(message, type = 'error') {
                errorMessage.style.display = 'none';
                successMessage.style.display = 'none';

                if (type === 'error') {
                    errorMessage.textContent = message;
                    errorMessage.style.display = 'block';
                } else {
                    successMessage.textContent = message;
                    successMessage.style.display = 'block';
                }

                // 3秒后自动隐藏
                setTimeout(() => {
                    errorMessage.style.display = 'none';
                    successMessage.style.display = 'none';
                }, 3000);
            }

            registerForm.addEventListener('submit', async (e) => {
                e.preventDefault();

                const username = document.getElementById('username').value;
                const name = document.getElementById('name').value;
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                const confirmPassword = document.getElementById('confirm_password').value;

                if (!username || !name || !password || !confirmPassword) {
                    showMessage('请填写所有必填字段');
                    return;
                }

                if (password !== confirmPassword) {
                    showMessage('两次输入的密码不一致');
                    return;
                }

                if (password.length < 6) {
                    showMessage('密码长度至少6位');
                    return;
                }

                // 显示加载状态
                registerBtn.disabled = true;
                btnText.innerHTML = '<span class="loading"></span>注册中...';

                try {
                    const response = await fetch('/api/auth/register', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: new URLSearchParams({
                            username: username,
                            name: name,
                            email: email,
                            password: password
                        })
                    });

                    const data = await response.json();

                    if (data.code === 200) {
                        showMessage('注册成功，正在跳转到登录页面...', 'success');
                        // 2秒后跳转到登录页面
                        setTimeout(() => {
                            window.location.href = '/api/auth/login';
                        }, 2000);
                    } else {
                        showMessage(data.message || '注册失败');
                    }
                } catch (error) {
                    showMessage('网络错误，请稍后重试');
                } finally {
                    // 恢复按钮状态
                    registerBtn.disabled = false;
                    btnText.textContent = '注册';
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


@auth_bp.route('/logout')
def logout():
    """
    用户登出
    """
    # 清除会话
    session.clear()

    # 返回登录页面
    return redirect('/api/auth/login')


@auth_bp.route('/profile')
def profile():
    """
    用户个人资料页面
    """
    # 检查用户是否登录
    if 'user_id' not in session:
        return redirect('/api/auth/login')

    user = User.query.get(session['user_id'])
    if not user:
        return redirect('/api/auth/login')

    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ERP系统 - 个人资料</title>
        <style>
            body {{
                font-family: 'Microsoft YaHei', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            .profile-container {{
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
                width: 100%;
                max-width: 600px;
            }}
            .profile-header {{
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #f0f0f0;
            }}
            .profile-header h1 {{
                color: #333;
                font-size: 32px;
                margin-bottom: 10px;
            }}
            .profile-info {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .info-item {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }}
            .info-item label {{
                display: block;
                color: #666;
                font-size: 14px;
                margin-bottom: 5px;
            }}
            .info-item span {{
                display: block;
                color: #333;
                font-size: 16px;
                font-weight: bold;
            }}
            .btn-group {{
                display: flex;
                gap: 15px;
                justify-content: center;
            }}
            .btn {{
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
                text-decoration: none;
                display: inline-block;
            }}
            .btn-primary {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            .btn-primary:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            }}
            .btn-secondary {{
                background: #6c757d;
                color: white;
            }}
            .btn-secondary:hover {{
                background: #5a6268;
                transform: translateY(-2px);
            }}
        </style>
    </head>
    <body>
        <div class="profile-container">
            <div class="profile-header">
                <h1>👤 个人资料</h1>
                <p>欢迎您，{user.name}！</p>
            </div>

            <div class="profile-info">
                <div class="info-item">
                    <label>用户名</label>
                    <span>{user.username}</span>
                </div>
                <div class="info-item">
                    <label>姓名</label>
                    <span>{user.name}</span>
                </div>
                <div class="info-item">
                    <label>邮箱</label>
                    <span>{user.email or '未填写'}</span>
                </div>
                <div class="info-item">
                    <label>角色</label>
                    <span>{{'管理员' if user.role == 'admin' else '员工'}}</span>
                </div>
                <div class="info-item">
                    <label>状态</label>
                    <span>{{'激活' if user.status == 'active' else '禁用'}}</span>
                </div>
                <div class="info-item">
                    <label>注册时间</label>
                    <span>{user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else '未知'}</span>
                </div>
            </div>

            <div class="btn-group">
                <a href="/api/attendance/" class="btn btn-primary">返回打卡页面</a>
                <a href="/api/auth/logout" class="btn btn-secondary">退出登录</a>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, user=user)


@auth_bp.route('/check_auth')
def check_auth():
    """
    检查用户认证状态
    """
    if 'user_id' not in session:
        return error_response('未登录', 401)

    user = User.query.get(session['user_id'])
    if not user or user.status != 'active':
        return error_response('用户不存在或已被禁用', 403)

    return json_response({
        'user_id': user.id,
        'username': user.username,
        'name': user.name,
        'role': user.role
    })