"""
打卡相关路由
"""
from flask import Blueprint, request, render_template_string, redirect, url_for, session
from datetime import datetime, date
from app import db
from app.models import User, AttendanceRecord
from app.utils.helpers import json_response, error_response, login_required

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/checkin', methods=['POST'])
def check_in():
    """
    上班打卡
    ---
    tags:
      - 打卡管理
    summary: 员工上班打卡
    description: 记录员工上班打卡时间，系统会自动判断是否迟到（超过9:30算迟到）
    parameters:
      - name: user_id
        in: query
        type: integer
        required: true
        description: 员工用户ID
        example: 1
    responses:
      200:
        description: 打卡成功
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 200
            message:
              type: string
              example: 打卡成功
            data:
              type: object
              properties:
                record:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    user_id:
                      type: integer
                      example: 1
                    user_name:
                      type: string
                      example: 系统管理员
                    attendance_date:
                      type: string
                      example: "2024-01-15"
                    check_in_time:
                      type: string
                      example: "2024-01-15 09:05:23"
                    check_out_time:
                      type: string
                      example: null
                    work_hours:
                      type: number
                      example: 0.0
                    status:
                      type: string
                      example: normal
                    status_text:
                      type: string
                      example: 正常
      400:
        description: 请求错误（如已打卡、参数缺失等）
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 400
            message:
              type: string
              example: 今天已经打过上班卡了
            data:
              type: null
    """
    try:
        user_id = request.args.get('user_id') or (request.json.get('user_id') if request.json else None)
        
        if not user_id:
            return error_response('请提供用户ID', 400)
        
        user = User.query.get(user_id)
        if not user:
            return error_response('用户不存在', 404)
        
        if user.status != 'active':
            return error_response('用户已被禁用', 403)
        
        today = date.today()
        # 查找今天的打卡记录
        record = AttendanceRecord.query.filter_by(
            user_id=user_id,
            attendance_date=today
        ).first()
        
        if record and record.check_in_time:
            return error_response('今天已经打过上班卡了', 400)
        
        # 创建或更新打卡记录
        if not record:
            record = AttendanceRecord(
                user_id=user_id,
                attendance_date=today
            )
            db.session.add(record)
        
        record.check_in_time = datetime.now()
        record.check_status()
        db.session.commit()
        
        return json_response({
            'record': record.to_dict(),
            'message': '上班打卡成功'
        }, '打卡成功')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'打卡失败: {str(e)}', 500)


@attendance_bp.route('/checkout', methods=['POST'])
def check_out():
    """
    下班打卡
    ---
    tags:
      - 打卡管理
    summary: 员工下班打卡
    description: 记录员工下班打卡时间，系统会自动计算工作时长并判断是否早退
    parameters:
      - name: user_id
        in: query
        type: integer
        required: true
        description: 员工用户ID
        example: 1
    responses:
      200:
        description: 打卡成功
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 200
            message:
              type: string
              example: 打卡成功
            data:
              type: object
              properties:
                record:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    user_id:
                      type: integer
                      example: 1
                    work_hours:
                      type: number
                      example: 9.09
                    status:
                      type: string
                      example: normal
      400:
        description: 请求错误（如未打上班卡、已打卡等）
    """
    try:
        user_id = request.args.get('user_id') or (request.json.get('user_id') if request.json else None)
        
        if not user_id:
            return error_response('请提供用户ID', 400)
        
        user = User.query.get(user_id)
        if not user:
            return error_response('用户不存在', 404)
        
        if user.status != 'active':
            return error_response('用户已被禁用', 403)
        
        today = date.today()
        # 查找今天的打卡记录
        record = AttendanceRecord.query.filter_by(
            user_id=user_id,
            attendance_date=today
        ).first()
        
        if not record or not record.check_in_time:
            return error_response('请先打上班卡', 400)
        
        if record.check_out_time:
            return error_response('今天已经打过下班卡了', 400)
        
        record.check_out_time = datetime.now()
        record.check_status()
        db.session.commit()
        
        return json_response({
            'record': record.to_dict(),
            'message': '下班打卡成功'
        }, '打卡成功')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'打卡失败: {str(e)}', 500)


@attendance_bp.route('/records', methods=['GET'])
def get_records():
    """
    查询历史打卡记录
    ---
    tags:
      - 打卡管理
    summary: 查询历史打卡记录
    description: 查询历史打卡记录，支持按用户、日期范围筛选，支持分页查询
    parameters:
      - name: user_id
        in: query
        type: integer
        required: false
        description: 员工用户ID，不传则查询所有员工
        example: 1
      - name: start_date
        in: query
        type: string
        required: false
        description: 开始日期，格式：YYYY-MM-DD
        example: "2024-01-01"
      - name: end_date
        in: query
        type: string
        required: false
        description: 结束日期，格式：YYYY-MM-DD
        example: "2024-01-31"
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: 页码
        example: 1
      - name: per_page
        in: query
        type: integer
        required: false
        default: 20
        description: 每页数量
        example: 20
    responses:
      200:
        description: 查询成功
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 200
            message:
              type: string
              example: success
            data:
              type: object
              properties:
                records:
                  type: array
                  items:
                    type: object
                pagination:
                  type: object
                  properties:
                    page:
                      type: integer
                      example: 1
                    per_page:
                      type: integer
                      example: 20
                    total:
                      type: integer
                      example: 100
                    pages:
                      type: integer
                      example: 5
    """
    try:
        user_id = request.args.get('user_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = AttendanceRecord.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if start_date:
            query = query.filter(AttendanceRecord.attendance_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        
        if end_date:
            query = query.filter(AttendanceRecord.attendance_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        
        # 按日期倒序排列
        query = query.order_by(AttendanceRecord.attendance_date.desc(), AttendanceRecord.check_in_time.desc())
        
        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        records = pagination.items
        
        return json_response({
            'records': [record.to_dict() for record in records],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        })
    
    except Exception as e:
        return error_response(f'查询失败: {str(e)}', 500)


@attendance_bp.route('/today', methods=['GET'])
def get_today_record():
    """
    查询今日打卡记录
    ---
    tags:
      - 打卡管理
    summary: 查询今日打卡记录
    description: 查询指定员工今天的打卡记录，包括上班时间、下班时间、工作时长和状态
    parameters:
      - name: user_id
        in: query
        type: integer
        required: true
        description: 员工用户ID
        example: 1
    responses:
      200:
        description: 查询成功
        schema:
          type: object
          properties:
            code:
              type: integer
              example: 200
            message:
              type: string
              example: success
            data:
              type: object
              properties:
                record:
                  type: object
                  nullable: true
                has_checkin:
                  type: boolean
                  example: true
                has_checkout:
                  type: boolean
                  example: true
    """
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return error_response('请提供用户ID', 400)
        
        today = date.today()
        record = AttendanceRecord.query.filter_by(
            user_id=user_id,
            attendance_date=today
        ).first()
        
        if not record:
            return json_response({
                'record': None,
                'has_checkin': False,
                'has_checkout': False
            })
        
        return json_response({
            'record': record.to_dict(),
            'has_checkin': record.check_in_time is not None,
            'has_checkout': record.check_out_time is not None
        })
    
    except Exception as e:
        return error_response(f'查询失败: {str(e)}', 500)


@attendance_bp.route('/')
def attendance_page():
    """打卡页面"""
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
        <title>员工打卡</title>
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
                max-width: 600px;
                width: 100%;
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 30px;
                font-size: 32px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: bold;
            }
            input, select {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s;
            }
            input:focus, select:focus {
                outline: none;
                border-color: #667eea;
            }
            .btn-group {
                display: flex;
                gap: 15px;
                margin-top: 30px;
            }
            button {
                flex: 1;
                padding: 15px;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
            }
            .btn-checkin {
                background: #4CAF50;
                color: white;
            }
            .btn-checkin:hover {
                background: #45a049;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
            }
            .btn-checkout {
                background: #f44336;
                color: white;
            }
            .btn-checkout:hover {
                background: #da190b;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(244, 67, 54, 0.3);
            }
            .btn-query {
                background: #2196F3;
                color: white;
            }
            .btn-query:hover {
                background: #0b7dda;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(33, 150, 243, 0.3);
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
                display: none;
            }
            .result.success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .result.error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .result.show {
                display: block;
            }
            .record-info {
                margin-top: 20px;
                padding: 15px;
                background: #f5f5f5;
                border-radius: 8px;
            }
            .record-info h3 {
                color: #667eea;
                margin-bottom: 10px;
            }
            .record-info p {
                margin: 5px 0;
                color: #666;
            }
            .back-link {
                display: block;
                text-align: center;
                margin-top: 20px;
                color: #667eea;
                text-decoration: none;
            }
            .back-link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⏰ 员工打卡</h1>
            <div class="form-group">
                <label for="user_id">选择员工：</label>
                <select id="user_id">
                    <option value="">请选择员工</option>
                </select>
            </div>
            <div class="btn-group">
                <button class="btn-checkin" onclick="checkIn()">上班打卡</button>
                <button class="btn-checkout" onclick="checkOut()">下班打卡</button>
                <button class="btn-query" onclick="queryToday()">查询今日</button>
            </div>
            <div id="result" class="result"></div>
            <div id="recordInfo" class="record-info" style="display: none;">
                <h3>今日打卡信息</h3>
                <div id="recordContent"></div>
            </div>
            <div style="text-align: center; margin-top: 20px;">
                <a href="/api/auth/profile" class="btn-profile" style="display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-right: 10px;">个人资料</a>
                <a href="/api/auth/logout" class="btn-logout" style="display: inline-block; padding: 10px 20px; background: #dc3545; color: white; text-decoration: none; border-radius: 5px;">退出登录</a>
            </div>
            <a href="/" class="back-link">← 返回首页</a>
        </div>
        <script>
            // 用户信息
            const currentUserId = {{ user.id }};
            const currentUserName = '{{ user.name }}';

            // 加载员工列表
            async function loadUsers() {
                try {
                    // 这里简化处理，实际应该从API获取
                    const select = document.getElementById('user_id');
                    select.innerHTML = '<option value="">请选择员工</option>';

                    // 自动选择当前用户
                    const option = document.createElement('option');
                    option.value = currentUserId;
                    option.textContent = `${currentUserName} (${'{{ user.username }}'})`;
                    option.selected = true;
                    select.appendChild(option);
                } catch (error) {
                    console.error('加载员工列表失败:', error);
                }
            }
            
            function showResult(message, isSuccess = true) {
                const result = document.getElementById('result');
                result.textContent = message;
                result.className = 'result show ' + (isSuccess ? 'success' : 'error');
                setTimeout(() => {
                    result.classList.remove('show');
                }, 3000);
            }
            
            async function checkIn() {
                const userId = document.getElementById('user_id').value;
                if (!userId) {
                    showResult('请先选择员工', false);
                    return;
                }
                
                try {
                    const response = await fetch(`/api/attendance/checkin?user_id=${userId}`, {
                        method: 'POST'
                    });
                    const data = await response.json();
                    if (data.code === 200) {
                        showResult('上班打卡成功！', true);
                        queryToday();
                    } else {
                        showResult(data.message || '打卡失败', false);
                    }
                } catch (error) {
                    showResult('打卡失败: ' + error.message, false);
                }
            }
            
            async function checkOut() {
                const userId = document.getElementById('user_id').value;
                if (!userId) {
                    showResult('请先选择员工', false);
                    return;
                }
                
                try {
                    const response = await fetch(`/api/attendance/checkout?user_id=${userId}`, {
                        method: 'POST'
                    });
                    const data = await response.json();
                    if (data.code === 200) {
                        showResult('下班打卡成功！', true);
                        queryToday();
                    } else {
                        showResult(data.message || '打卡失败', false);
                    }
                } catch (error) {
                    showResult('打卡失败: ' + error.message, false);
                }
            }
            
            async function queryToday() {
                const userId = document.getElementById('user_id').value;
                if (!userId) {
                    showResult('请先选择员工', false);
                    return;
                }
                
                try {
                    const response = await fetch(`/api/attendance/today?user_id=${userId}`);
                    const data = await response.json();
                    if (data.code === 200) {
                        const recordInfo = document.getElementById('recordInfo');
                        const recordContent = document.getElementById('recordContent');
                        
                        if (data.data.record) {
                            const record = data.data.record;
                            recordContent.innerHTML = `
                                <p><strong>打卡日期：</strong>${record.attendance_date}</p>
                                <p><strong>上班时间：</strong>${record.check_in_time || '未打卡'}</p>
                                <p><strong>下班时间：</strong>${record.check_out_time || '未打卡'}</p>
                                <p><strong>工作时长：</strong>${record.work_hours || 0} 小时</p>
                                <p><strong>状态：</strong>${record.status_text}</p>
                            `;
                            recordInfo.style.display = 'block';
                        } else {
                            recordContent.innerHTML = '<p>今日尚未打卡</p>';
                            recordInfo.style.display = 'block';
                        }
                    }
                } catch (error) {
                    showResult('查询失败: ' + error.message, false);
                }
            }
            
            // 页面加载时初始化
            loadUsers();
        </script>
    </body>
    </html>
    """
    return render_template_string(html, user=user)

