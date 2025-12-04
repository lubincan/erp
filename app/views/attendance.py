"""
打卡相关路由
"""
from flask import Blueprint, request, render_template_string, redirect, url_for, session
from flask_cors import cross_origin
from datetime import datetime, date
import json
from app import db
from app.models import User, AttendanceRecord
from app.utils.helpers import json_response, error_response, login_required
from app.utils.themes import get_current_theme, get_all_themes, set_theme

attendance_bp = Blueprint('attendance', __name__, url_prefix='/api/attendance')

@attendance_bp.route('/', methods=['GET'])
@cross_origin()
def attendance_page():
    """打卡页面"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('auth.login'))

    # 检查今日是否已签到
    today = date.today()
    today_record = AttendanceRecord.query.filter_by(
        user_id=user.id,
        attendance_date=today
    ).first()

    # 获取当前主题
    current_theme = get_current_theme()
    themes = get_all_themes()
    theme_options = ''.join([f'<option value="{theme}">{themes[theme]["name"]}</option>' for theme in themes])

    html = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>员工打卡 - ERP系统</title>
        <style>
            :root {
                --theme-background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                --theme-button-primary: #667eea;
                --theme-button-hover: #764ba2;
                --theme-accent: #667eea;
                --theme-shadow: rgba(0,0,0,0.3);
            }

            body {
                font-family: 'Microsoft YaHei', Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: var(--theme-background);
                min-height: 100vh;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px var(--theme-shadow);
                position: relative;
                border: 2px solid var(--theme-accent);
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background: linear-gradient(135deg, var(--theme-accent), var(--theme-button-primary));
                border-radius: 10px;
                color: white;
                box-shadow: 0 5px 15px var(--theme-shadow);
            }
            .header h1 {
                margin: 0;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .user-info {
                background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,249,250,0.9));
                padding: 25px;
                border-radius: 12px;
                margin-bottom: 30px;
                text-align: center;
                border: 2px solid var(--theme-accent);
                box-shadow: 0 5px 15px var(--theme-shadow);
            }
            .clock-button {
                display: block;
                width: 200px;
                height: 200px;
                margin: 20px auto;
                border: none;
                border-radius: 50%;
                font-size: 24px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
                color: white;
                border: 4px solid var(--theme-accent);
                box-shadow: 0 8px 25px var(--theme-shadow);
            }
            .clock-in {
                background: linear-gradient(45deg, var(--theme-button-primary), var(--theme-button-hover));
            }
            .clock-out {
                background: linear-gradient(45deg, #e74c3c, #c0392b);
            }
            .clock-button:hover {
                transform: scale(1.1);
                box-shadow: 0 8px 30px var(--theme-shadow);
                border-color: var(--theme-button-hover);
            }
            .status {
                text-align: center;
                margin: 20px 0;
                padding: 15px;
                border-radius: 8px;
                font-weight: bold;
            }
            .status.clock-in {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .status.clock-out {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .nav {
                display: flex;
                justify-content: center;
                gap: 15px;
                margin: 20px 0;
                flex-wrap: wrap;
            }
            .nav a {
                display: inline-block;
                padding: 12px 25px;
                background: var(--theme-button-primary);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                transition: all 0.3s;
                border: 2px solid var(--theme-accent);
                font-weight: bold;
                box-shadow: 0 4px 15px var(--theme-shadow);
            }
            .nav a:hover {
                background: var(--theme-button-hover);
                transform: translateY(-2px);
                box-shadow: 0 6px 20px var(--theme-shadow);
            }
            .back-link {
                display: inline-block;
                margin: 20px 0;
                color: var(--theme-accent);
                text-decoration: none;
                font-weight: bold;
                font-size: 1.1em;
                transition: all 0.3s;
            }
            .back-link:hover {
                color: var(--theme-button-primary);
                transform: translateX(5px);
            }
            .info {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-top: 30px;
            }
            .info h2 {
                color: #333;
                margin-top: 0;
            }
            .info p {
                line-height: 1.6;
                color: #666;
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
            <div style="position: absolute; top: 20px; right: 20px;">
                <select id="themeSelector" onchange="switchTheme(this.value)"
                    style="padding: 10px 15px; border-radius: 8px; border: 2px solid var(--theme-accent);
                           background: white; color: #333; font-weight: bold; cursor: pointer;
                           box-shadow: 0 3px 10px var(--theme-shadow); transition: all 0.3s;"
                    onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 5px 15px var(--theme-shadow)'"
                    onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 3px 10px var(--theme-shadow)'">
                    <option value="">切换主题</option>
                    """ + theme_options + """
                </select>
            </div>
            <div class="nav">
                <a href="/api/attendance/">员工打卡</a>
                <a href="/api/auth/profile">个人资料</a>
                <a href="/api/docs" target="_blank">Swagger API文档</a>
                <a href="/api/attendance/records?user_id=""" + str(user.id) + """" target="_blank">查看打卡记录</a>
                <a href="/api/auth/logout" style="background: #dc3545;">退出登录</a>
            </div>
            <div class="header">
                <h1>👤 员工打卡系统</h1>
                <p>欢迎使用ERP考勤管理系统</p>
            </div>
            <div class="user-info">
                <h2>员工信息</h2>
                <p><strong>姓名：</strong>""" + (user.name if user.name else '') + """</p>
                <p><strong>用户名：</strong>""" + (user.username if user.username else '') + """</p>
                <p><strong>邮箱：</strong>""" + (user.email if user.email else '') + """</p>
                <p><strong>角色：</strong>""" + ('管理员' if user and user.role == 'admin' else '员工') + """</p>
            </div>
            <div class="status">
                """ + ("""
                    <p>今日尚未签到</p>
                """ if not today_record else ("""
                    <p>签到时间：""" + today_record.check_in_time.strftime('%H:%M:%S') + """</p>
                    <p>尚未签退</p>
                """ if not today_record.check_out_time else ("""
                    <p>今日已签到：""" + today_record.check_in_time.strftime('%H:%M:%S') + """</p>
                    <p>今日已签退：""" + today_record.check_out_time.strftime('%H:%M:%S') + """</p>
                    <p>工作时间：""" + str(today_record.work_hours) + """小时</p>
                """))) + """
            </div>
            <div style="text-align: center;">
                """ + ("""
                    <button class="clock-button clock-in" onclick="clockIn()">
                        📝 签到
                    </button>
                """ if not today_record else ("""
                    <button class="clock-button clock-out" onclick="clockOut()">
                        🏃 签退
                    </button>
                """ if today_record and not today_record.check_out_time else """
                    <p style="color: #666; font-size: 18px;">今日打卡已完成</p>
                """)) + """
            </div>
            <div class="info">
                <h2>📋 系统说明</h2>
                <p><strong>当前功能：</strong>员工打卡系统</p>
                <p><strong>默认管理员账户：</strong></p>
                <p>用户名: <code>admin</code> | 密码: <code>admin123</code></p>
                <p><strong>API文档：</strong></p>
                <p>• <a href="/api/docs" target="_blank" style="color: #667eea;">Swagger UI 在线文档</a> - 交互式API文档，支持在线测试</p>
                <p>• <a href="/api/attendance/records" target="_blank" style="color: #667eea;">打卡记录API</a> - 获取打卡记录数据</p>
                <p><strong>使用说明：</strong></p>
                <p>1. 点击"签到"按钮记录上班时间</p>
                <p>2. 点击"签退"按钮记录下班时间</p>
                <p>3. 系统会自动计算工作时间</p>
                <p>4. 可通过右上角切换界面主题</p>
            </div>
            <a href="/" class="back-link">← 返回首页</a>
        </div>
        <script>
            // 用户信息
            const currentUserId = """ + str(user.id if user else 0) + """;
            const currentUserName = '""" + (user.name if user else '') + """';

            // 打卡功能
            async function clockIn() {
                try {
                    const response = await fetch('/api/attendance/clock-in', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ user_id: currentUserId })
                    });

                    const data = await response.json();

                    if (data.success) {
                        alert('签到成功！\\n签到时间：' + data.check_in_time);
                        location.reload();
                    } else {
                        alert('签到失败：' + data.message);
                    }
                } catch (error) {
                    alert('签到失败：' + error.message);
                }
            }

            async function clockOut() {
                try {
                    const response = await fetch('/api/attendance/clock-out', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ user_id: currentUserId })
                    });

                    const data = await response.json();

                    if (data.success) {
                        alert('签退成功！\\n签退时间：' + data.check_out_time + '\\n工作时间：' + data.work_hours + '小时');
                        location.reload();
                    } else {
                        alert('签退失败：' + data.message);
                    }
                } catch (error) {
                    alert('签退失败：' + error.message);
                }
            }

            // 主题切换功能
            function switchTheme(themeName) {
                if (themeName) {
                    fetch('/api/attendance/theme/set', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ theme: themeName })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // 应用主题CSS
                            applyTheme(themeName);
                            // 更新选择器
                            document.getElementById('themeSelector').value = themeName;
                        }
                    })
                    .catch(error => {
                        console.error('主题切换失败:', error);
                    });
                }
            }

            // 应用主题
            function applyTheme(themeName) {
                // 获取主题配置
                const themes = """ + json.dumps(themes) + """;
                const theme = themes[themeName] || themes['default'];

                // 更新CSS变量
                const root = document.documentElement;
                root.style.setProperty('--theme-background', theme.background);
                root.style.setProperty('--theme-button-primary', theme.button_primary);
                root.style.setProperty('--theme-button-hover', theme.button_hover);
                root.style.setProperty('--theme-accent', theme.accent);
                root.style.setProperty('--theme-shadow', theme.shadow);
            }

            // 页面加载时应用当前主题
            document.addEventListener('DOMContentLoaded', function() {
                // 应用当前主题
                applyTheme('""" + current_theme + """');

                // 设置主题选择器
                const select = document.getElementById('themeSelector');
                select.value = '""" + current_theme + """';

                // 这里简化处理，实际应该从API获取
                const selectUser = document.getElementById('user_id');
                selectUser.innerHTML = '<option value="">请选择员工</option>';

                // 自动选择当前用户
                const option = document.createElement('option');
                option.value = currentUserId;
                option.textContent = currentUserName;
                option.selected = true;
                selectUser.appendChild(option);
            });

            // 页面加载时检查打卡状态（已合并到上面的DOMContentLoaded事件中）
        </script>
    </body>
    </html>
    """

    return render_template_string(html)

@attendance_bp.route('/clock-in', methods=['POST'])
@login_required
def check_in_time():
    """签到API"""
    if 'user_id' not in session:
        return error_response('请先登录', 401)

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return error_response('用户不存在', 404)

    # 检查今日是否已签到
    today = date.today()
    today_record = AttendanceRecord.query.filter_by(
        user_id=user_id,
        attendance_date=today
    ).first()

    if today_record:
        return error_response('今日已签到', 400)

    # 创建签到记录
    record = AttendanceRecord(
        user_id=user_id,
        attendance_date=today,
        check_in_time=datetime.now()
    )

    db.session.add(record)
    db.session.commit()

    return json_response({
        'success': True,
        'message': '签到成功',
        'check_in_time': record.check_in_time.strftime('%Y-%m-%d %H:%M:%S')
    })

@attendance_bp.route('/clock-out', methods=['POST'])
@login_required
def check_out_time():
    """签退API"""
    if 'user_id' not in session:
        return error_response('请先登录', 401)

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return error_response('用户不存在', 404)

    # 检查今日是否已签到
    today = date.today()
    today_record = AttendanceRecord.query.filter_by(
        user_id=user_id,
        attendance_date=today
    ).first()

    if not today_record:
        return error_response('今日未签到', 400)

    if today_record.check_out_time:
        return error_response('今日已签退', 400)

    # 更新签退时间
    today_record.check_out_time = datetime.now()

    # 计算工作时间
    if today_record.check_in_time:
        time_diff = today_record.check_out_time - today_record.check_in_time
        hours = time_diff.total_seconds() / 3600
        today_record.work_hours = round(hours, 2)

    db.session.commit()

    return json_response({
        'success': True,
        'message': '签退成功',
        'check_out_time': today_record.check_out_time.strftime('%Y-%m-%d %H:%M:%S'),
        'work_hours': today_record.work_hours
    })

@attendance_bp.route('/records')
@login_required
def get_records():
    """获取打卡记录"""
    if 'user_id' not in session:
        return error_response('请先登录', 401)

    user_id = session['user_id']
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # 获取用户ID（管理员可以查看所有记录）
    if request.args.get('user_id'):
        target_user_id = request.args.get('user_id', type=int)
        if session.get('user_role') != 'admin':
            return error_response('无权限查看其他用户记录', 403)
    else:
        target_user_id = user_id

    # 查询记录
    records = AttendanceRecord.query.filter_by(user_id=target_user_id)\
        .order_by(AttendanceRecord.date.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    result = []
    for record in records.items:
        result.append({
            'id': record.id,
            'date': record.date.strftime('%Y-%m-%d'),
            'check_in_time': record.check_in_time.strftime('%H:%M:%S') if record.check_in_time else None,
            'check_out_time': record.check_out_time.strftime('%H:%M:%S') if record.check_out_time else None,
            'work_hours': record.work_hours,
            'status': record.get_status()
        })

    return json_response({
        'success': True,
        'records': result,
        'total': records.total,
        'pages': records.pages,
        'current_page': page,
        'per_page': per_page
    })


# 主题管理API
@attendance_bp.route('/theme/set', methods=['POST'])
@login_required
def set_theme_route():
    """设置主题"""
    if 'user_id' not in session:
        return error_response('请先登录', 401)

    data = request.get_json()
    theme_name = data.get('theme')

    if not theme_name:
        return error_response('请选择主题', 400)

    # 验证主题是否存在
    from app.utils.themes import get_all_themes
    themes = get_all_themes()

    if theme_name not in themes:
        return error_response('主题不存在', 400)

    # 设置主题
    success = set_theme(theme_name)

    # 调试信息
    print(f"Session after set_theme: {dict(session)}")
    print(f"Session modified: {session.modified}")

    return json_response({
        'success': success,
        'message': '主题切换成功' if success else '主题切换失败',
        'theme': theme_name
    })


@attendance_bp.route('/theme/current')
@login_required
def get_current_theme_route():
    """获取当前主题"""
    if 'user_id' not in session:
        return error_response('请先登录', 401)

    current_theme = get_current_theme()
    from app.utils.themes import get_all_themes
    themes = get_all_themes()

    return json_response({
        'success': True,
        'current_theme': current_theme,
        'themes': themes
    })