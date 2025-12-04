"""
API文档页面
"""
from flask import Blueprint, render_template_string

docs_bp = Blueprint('docs', __name__)


@docs_bp.route('/docs')
@docs_bp.route('/api/docs')
def api_docs():
    """API文档页面"""
    html = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ERP系统 - API文档</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
                background: #f5f7fa;
                color: #333;
                line-height: 1.6;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .header h1 {
                font-size: 32px;
                margin-bottom: 10px;
            }
            .header p {
                opacity: 0.9;
                font-size: 16px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 30px 20px;
            }
            .nav {
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .nav a {
                color: #667eea;
                text-decoration: none;
                margin-right: 20px;
                font-weight: 500;
            }
            .nav a:hover {
                text-decoration: underline;
            }
            .api-section {
                background: white;
                border-radius: 10px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .api-section h2 {
                color: #667eea;
                font-size: 24px;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #e0e0e0;
            }
            .api-endpoint {
                margin-bottom: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            .method {
                display: inline-block;
                padding: 5px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
                margin-right: 10px;
            }
            .method.get {
                background: #61affe;
                color: white;
            }
            .method.post {
                background: #49cc90;
                color: white;
            }
            .method.put {
                background: #fca130;
                color: white;
            }
            .method.delete {
                background: #f93e3e;
                color: white;
            }
            .endpoint-url {
                font-family: 'Courier New', monospace;
                font-size: 16px;
                color: #333;
                margin: 10px 0;
            }
            .description {
                color: #666;
                margin: 15px 0;
                line-height: 1.8;
            }
            .params-table {
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                background: white;
            }
            .params-table th,
            .params-table td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #e0e0e0;
            }
            .params-table th {
                background: #f8f9fa;
                font-weight: 600;
                color: #333;
            }
            .params-table td {
                color: #666;
            }
            .params-table code {
                background: #f0f0f0;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
            .example {
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 20px;
                border-radius: 8px;
                margin: 15px 0;
                overflow-x: auto;
            }
            .example pre {
                margin: 0;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                line-height: 1.5;
            }
            .example .comment {
                color: #75715e;
            }
            .example .string {
                color: #e6db74;
            }
            .example .number {
                color: #ae81ff;
            }
            .response {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                border-left: 4px solid #49cc90;
            }
            .response h4 {
                color: #49cc90;
                margin-bottom: 10px;
            }
            .response pre {
                background: white;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                margin-top: 10px;
            }
            .badge {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 12px;
                font-weight: 500;
                margin-left: 10px;
            }
            .badge.required {
                background: #f93e3e;
                color: white;
            }
            .badge.optional {
                background: #61affe;
                color: white;
            }
            .toc {
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .toc h3 {
                color: #667eea;
                margin-bottom: 15px;
            }
            .toc ul {
                list-style: none;
            }
            .toc li {
                margin: 8px 0;
            }
            .toc a {
                color: #333;
                text-decoration: none;
                padding: 5px 10px;
                display: block;
                border-radius: 5px;
                transition: background 0.3s;
            }
            .toc a:hover {
                background: #f0f0f0;
                color: #667eea;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="container">
                <h1>📚 ERP系统 API 文档</h1>
                <p>完整的RESTful API接口文档，包含请求参数、响应格式和示例代码</p>
            </div>
        </div>
        
        <div class="container">
            <div class="nav">
                <a href="/">🏠 首页</a>
                <a href="/attendance">⏰ 打卡页面</a>
                <a href="/docs">📚 API文档</a>
            </div>
            
            <div class="toc">
                <h3>📑 目录</h3>
                <ul>
                    <li><a href="#attendance">打卡管理 API</a></li>
                    <li><a href="#checkin">上班打卡</a></li>
                    <li><a href="#checkout">下班打卡</a></li>
                    <li><a href="#today">查询今日打卡</a></li>
                    <li><a href="#records">查询历史记录</a></li>
                </ul>
            </div>
            
            <div class="api-section" id="attendance">
                <h2>打卡管理 API</h2>
                <p class="description">所有打卡相关的API接口，包括上班打卡、下班打卡和记录查询功能。</p>
            </div>
            
            <div class="api-section" id="checkin">
                <div class="api-endpoint">
                    <span class="method post">POST</span>
                    <span class="endpoint-url">/api/attendance/checkin</span>
                    <h3 style="margin-top: 15px; color: #333;">上班打卡</h3>
                    <p class="description">记录员工上班打卡时间，系统会自动判断是否迟到（超过9:30算迟到）。</p>
                    
                    <h4 style="margin-top: 20px; color: #333;">请求参数</h4>
                    <table class="params-table">
                        <thead>
                            <tr>
                                <th>参数名</th>
                                <th>类型</th>
                                <th>位置</th>
                                <th>必填</th>
                                <th>说明</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code>user_id</code></td>
                                <td>integer</td>
                                <td>Query / Body</td>
                                <td><span class="badge required">必填</span></td>
                                <td>员工用户ID</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <h4 style="margin-top: 20px; color: #333;">请求示例</h4>
                    <div class="example">
                        <pre><span class="comment"># 使用Query参数</span>
curl -X POST "http://127.0.0.1:5000/api/attendance/checkin?user_id=1"

<span class="comment"># 使用JSON Body</span>
curl -X POST "http://127.0.0.1:5000/api/attendance/checkin" \\
  -H "Content-Type: application/json" \\
  -d '{"user_id": 1}'</pre>
                    </div>
                    
                    <h4 style="margin-top: 20px; color: #333;">响应示例</h4>
                    <div class="response">
                        <h4>成功响应 (200)</h4>
                        <pre>{
  "code": 200,
  "message": "打卡成功",
  "data": {
    "record": {
      "id": 1,
      "user_id": 1,
      "user_name": "系统管理员",
      "attendance_date": "2024-01-15",
      "check_in_time": "2024-01-15 09:05:23",
      "check_out_time": null,
      "work_hours": 0.0,
      "status": "normal",
      "status_text": "正常",
      "remark": null,
      "created_at": "2024-01-15 09:05:23"
    },
    "message": "上班打卡成功"
  }
}</pre>
                    </div>
                    
                    <div class="response" style="border-left-color: #f93e3e;">
                        <h4 style="color: #f93e3e;">错误响应 (400)</h4>
                        <pre>{
  "code": 400,
  "message": "今天已经打过上班卡了",
  "data": null
}</pre>
                    </div>
                </div>
            </div>
            
            <div class="api-section" id="checkout">
                <div class="api-endpoint">
                    <span class="method post">POST</span>
                    <span class="endpoint-url">/api/attendance/checkout</span>
                    <h3 style="margin-top: 15px; color: #333;">下班打卡</h3>
                    <p class="description">记录员工下班打卡时间，系统会自动计算工作时长并判断是否早退。</p>
                    
                    <h4 style="margin-top: 20px; color: #333;">请求参数</h4>
                    <table class="params-table">
                        <thead>
                            <tr>
                                <th>参数名</th>
                                <th>类型</th>
                                <th>位置</th>
                                <th>必填</th>
                                <th>说明</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code>user_id</code></td>
                                <td>integer</td>
                                <td>Query / Body</td>
                                <td><span class="badge required">必填</span></td>
                                <td>员工用户ID</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <h4 style="margin-top: 20px; color: #333;">请求示例</h4>
                    <div class="example">
                        <pre>curl -X POST "http://127.0.0.1:5000/api/attendance/checkout?user_id=1"</pre>
                    </div>
                    
                    <h4 style="margin-top: 20px; color: #333;">响应示例</h4>
                    <div class="response">
                        <h4>成功响应 (200)</h4>
                        <pre>{
  "code": 200,
  "message": "打卡成功",
  "data": {
    "record": {
      "id": 1,
      "user_id": 1,
      "user_name": "系统管理员",
      "attendance_date": "2024-01-15",
      "check_in_time": "2024-01-15 09:05:23",
      "check_out_time": "2024-01-15 18:10:45",
      "work_hours": 9.09,
      "status": "normal",
      "status_text": "正常",
      "remark": null,
      "created_at": "2024-01-15 09:05:23"
    },
    "message": "下班打卡成功"
  }
}</pre>
                    </div>
                    
                    <div class="response" style="border-left-color: #f93e3e;">
                        <h4 style="color: #f93e3e;">错误响应 (400)</h4>
                        <pre>{
  "code": 400,
  "message": "请先打上班卡",
  "data": null
}</pre>
                    </div>
                </div>
            </div>
            
            <div class="api-section" id="today">
                <div class="api-endpoint">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/api/attendance/today</span>
                    <h3 style="margin-top: 15px; color: #333;">查询今日打卡记录</h3>
                    <p class="description">查询指定员工今天的打卡记录，包括上班时间、下班时间、工作时长和状态。</p>
                    
                    <h4 style="margin-top: 20px; color: #333;">请求参数</h4>
                    <table class="params-table">
                        <thead>
                            <tr>
                                <th>参数名</th>
                                <th>类型</th>
                                <th>位置</th>
                                <th>必填</th>
                                <th>说明</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code>user_id</code></td>
                                <td>integer</td>
                                <td>Query</td>
                                <td><span class="badge required">必填</span></td>
                                <td>员工用户ID</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <h4 style="margin-top: 20px; color: #333;">请求示例</h4>
                    <div class="example">
                        <pre>curl "http://127.0.0.1:5000/api/attendance/today?user_id=1"</pre>
                    </div>
                    
                    <h4 style="margin-top: 20px; color: #333;">响应示例</h4>
                    <div class="response">
                        <h4>成功响应 (200)</h4>
                        <pre>{
  "code": 200,
  "message": "success",
  "data": {
    "record": {
      "id": 1,
      "user_id": 1,
      "user_name": "系统管理员",
      "attendance_date": "2024-01-15",
      "check_in_time": "2024-01-15 09:05:23",
      "check_out_time": "2024-01-15 18:10:45",
      "work_hours": 9.09,
      "status": "normal",
      "status_text": "正常",
      "remark": null,
      "created_at": "2024-01-15 09:05:23"
    },
    "has_checkin": true,
    "has_checkout": true
  }
}</pre>
                    </div>
                </div>
            </div>
            
            <div class="api-section" id="records">
                <div class="api-endpoint">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/api/attendance/records</span>
                    <h3 style="margin-top: 15px; color: #333;">查询历史打卡记录</h3>
                    <p class="description">查询历史打卡记录，支持按用户、日期范围筛选，支持分页查询。</p>
                    
                    <h4 style="margin-top: 20px; color: #333;">请求参数</h4>
                    <table class="params-table">
                        <thead>
                            <tr>
                                <th>参数名</th>
                                <th>类型</th>
                                <th>位置</th>
                                <th>必填</th>
                                <th>说明</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code>user_id</code></td>
                                <td>integer</td>
                                <td>Query</td>
                                <td><span class="badge optional">可选</span></td>
                                <td>员工用户ID，不传则查询所有员工</td>
                            </tr>
                            <tr>
                                <td><code>start_date</code></td>
                                <td>string</td>
                                <td>Query</td>
                                <td><span class="badge optional">可选</span></td>
                                <td>开始日期，格式：YYYY-MM-DD</td>
                            </tr>
                            <tr>
                                <td><code>end_date</code></td>
                                <td>string</td>
                                <td>Query</td>
                                <td><span class="badge optional">可选</span></td>
                                <td>结束日期，格式：YYYY-MM-DD</td>
                            </tr>
                            <tr>
                                <td><code>page</code></td>
                                <td>integer</td>
                                <td>Query</td>
                                <td><span class="badge optional">可选</span></td>
                                <td>页码，默认：1</td>
                            </tr>
                            <tr>
                                <td><code>per_page</code></td>
                                <td>integer</td>
                                <td>Query</td>
                                <td><span class="badge optional">可选</span></td>
                                <td>每页数量，默认：20</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <h4 style="margin-top: 20px; color: #333;">请求示例</h4>
                    <div class="example">
                        <pre><span class="comment"># 查询所有记录（分页）</span>
curl "http://127.0.0.1:5000/api/attendance/records?page=1&per_page=20"

<span class="comment"># 查询指定员工的记录</span>
curl "http://127.0.0.1:5000/api/attendance/records?user_id=1"

<span class="comment"># 按日期范围查询</span>
curl "http://127.0.0.1:5000/api/attendance/records?start_date=2024-01-01&end_date=2024-01-31"

<span class="comment"># 组合查询</span>
curl "http://127.0.0.1:5000/api/attendance/records?user_id=1&start_date=2024-01-01&end_date=2024-01-31&page=1&per_page=10"</pre>
                    </div>
                    
                    <h4 style="margin-top: 20px; color: #333;">响应示例</h4>
                    <div class="response">
                        <h4>成功响应 (200)</h4>
                        <pre>{
  "code": 200,
  "message": "success",
  "data": {
    "records": [
      {
        "id": 1,
        "user_id": 1,
        "user_name": "系统管理员",
        "attendance_date": "2024-01-15",
        "check_in_time": "2024-01-15 09:05:23",
        "check_out_time": "2024-01-15 18:10:45",
        "work_hours": 9.09,
        "status": "normal",
        "status_text": "正常",
        "remark": null,
        "created_at": "2024-01-15 09:05:23"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 100,
      "pages": 5
    }
  }
}</pre>
                    </div>
                </div>
            </div>
            
            <div class="api-section">
                <h2>📝 状态说明</h2>
                <table class="params-table">
                    <thead>
                        <tr>
                            <th>状态值</th>
                            <th>说明</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>normal</code></td>
                            <td>正常打卡</td>
                        </tr>
                        <tr>
                            <td><code>late</code></td>
                            <td>迟到（超过9:30）</td>
                        </tr>
                        <tr>
                            <td><code>early_leave</code></td>
                            <td>早退</td>
                        </tr>
                        <tr>
                            <td><code>late_early_leave</code></td>
                            <td>迟到且早退</td>
                        </tr>
                        <tr>
                            <td><code>absent</code></td>
                            <td>缺勤（未打上班卡）</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="api-section">
                <h2>🔧 使用Python requests示例</h2>
                <div class="example">
                    <pre><span class="comment"># 上班打卡</span>
<span class="string">import</span> requests

response = requests.post(
    <span class="string">"http://127.0.0.1:5000/api/attendance/checkin"</span>,
    params={<span class="string">"user_id"</span>: <span class="number">1</span>}
)
print(response.json())

<span class="comment"># 下班打卡</span>
response = requests.post(
    <span class="string">"http://127.0.0.1:5000/api/attendance/checkout"</span>,
    params={<span class="string">"user_id"</span>: <span class="number">1</span>}
)
print(response.json())

<span class="comment"># 查询今日记录</span>
response = requests.get(
    <span class="string">"http://127.0.0.1:5000/api/attendance/today"</span>,
    params={<span class="string">"user_id"</span>: <span class="number">1</span>}
)
print(response.json())

<span class="comment"># 查询历史记录</span>
response = requests.get(
    <span class="string">"http://127.0.0.1:5000/api/attendance/records"</span>,
    params={
        <span class="string">"user_id"</span>: <span class="number">1</span>,
        <span class="string">"start_date"</span>: <span class="string">"2024-01-01"</span>,
        <span class="string">"end_date"</span>: <span class="string">"2024-01-31"</span>,
        <span class="string">"page"</span>: <span class="number">1</span>,
        <span class="string">"per_page"</span>: <span class="number">20</span>
    }
)
print(response.json())</pre>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

