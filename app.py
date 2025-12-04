"""
ERP系统启动文件
"""
from app import create_app

app = create_app('development')

if __name__ == '__main__':
    print("=" * 50)
    print("ERP系统启动中...")
    print("访问地址: http://127.0.0.1:5000")
    print("默认管理员: admin / admin123")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)

