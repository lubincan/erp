# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码仓库中工作时提供指导。

## 项目概述

这是一个基于 Flask 的 ERP（企业资源规划）系统，目前专注于员工考勤管理。该系统计划发展为包含库存、采购、销售和财务管理模块的完整 ERP 系统。

## 开发命令

### 启动应用程序
```bash
# 直接 Python 执行
python app.py

# 使用 shell 脚本（检查依赖并安装）
./start.sh

# 使用 conda 环境（推荐用于可重现的环境）
./setup_conda.sh  # 一次性设置
conda activate erp
python app.py
```

### 默认配置
- **主机**: 0.0.0.0（网络可访问）
- **端口**: 5000
- **调试模式**: True（开发环境）
- **数据库**: SQLite (`instance/erp.db`)
- **默认管理员**: `admin / admin123`

### 依赖项
使用以下命令安装依赖：
```bash
pip install -r requirements.txt
```

主要依赖：
- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- Flask-CORS==4.0.0
- flasgger==0.9.7.1（用于 API 文档）

## 架构概述

### 应用结构
应用遵循 Flask 的应用工厂模式，使用模块化的蓝图：

```
app/
├── __init__.py          # 应用工厂
├── config.py            # 配置设置
├── models/              # SQLAlchemy 模型
│   ├── user.py          # 用户模型
│   └── attendance.py    # 考勤记录模型
├── views/               # 路由处理器
│   ├── index.py         # 首页
│   ├── attendance.py    # 考勤 API
│   ├── auth.py          # 认证
│   └── docs.py          # API 文档
└── utils/               # 工具函数
    └── helpers.py       # 辅助函数
```

### 关键架构模式

1. **应用工厂模式**: 应用在 `app/__init__.py` 中使用 `create_app()` 创建
2. **蓝图架构**: 使用 Flask 蓝图进行模块化路由：
   - `index_bp` - 首页
   - `attendance_bp` - 考勤 API (/api/attendance)
   - `auth_bp` - 认证 (/api/auth)
   - `docs_bp` - API 文档

3. **MVC 类结构**：
   - **模型**: `app/models/` - 使用 SQLAlchemy 的数据层
   - **视图**: `app/views/` - 路由处理器和网页
   - **控制器**: 嵌入在视图中（Flask 方式）

### 数据库架构

#### 用户表
- 基本用户信息（用户名、密码、姓名、邮箱、电话）
- 角色和状态管理
- 最后登录跟踪

#### 考勤记录表
- 签到/签出时间戳
- 工作时间计算
- 状态确定（迟到、早退等）
- 按日期组织

## 当前实现状态

### 已完成功能 ✅
1. **用户管理**
   - 用户注册和登录
   - 基于角色的访问（管理员/员工）
   - 会话认证

2. **考勤系统**
   - 签到/签出功能
   - 工作时间计算
   - 状态跟踪（正常、迟到、早退等）
   - 带分页的历史记录查询

3. **Web 界面**
   - 简洁、响应式 UI
   - 实时状态更新
   - 用户友好的表单

4. **API 文档**
   - 完整的 Swagger UI 文档
   - 交互式 API 测试
   - 代码示例

### 计划功能 🎯
根据 `plan.md`，系统计划发展为完整的 ERP，包括：
- 库存管理
- 采购系统
- 销售管理
- 财务模块
- 高级报表

## API 文档

系统提供 RESTful API 端点，Swagger 文档可在以下位置访问：
- 开发环境: `http://localhost:5000/apidocs/`
- 生产环境: `/apidocs/`

主要 API 端点：
- `/api/auth/login` - 用户登录
- `/api/auth/logout` - 用户登出
- `/api/attendance/clock-in` - 签到
- `/api/attendance/clock-out` - 签到
- `/api/attendance/records` - 获取考勤记录

## 开发工作流

### 环境设置
1. 确保 Python 3.10+ 已安装
2. （可选）使用 Conda 进行环境管理：
   ```bash
   conda env create -f environment.yml
   conda activate erp
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 运行应用程序：
   ```bash
   python app.py
   ```

### 代码组织
- 遵循 Flask 蓝图进行模块化组织
- 使用 SQLAlchemy 进行数据库操作
- 实现适当的错误处理和验证
- 使用 `app/utils/helpers.py` 中的现有辅助函数

### 测试
目前没有实现正式的测试框架。`app/test.py` 文件包含排序算法示例供参考。

## 配置

应用程序配置在 `app/config.py` 中管理，具有环境特定设置：
- 数据库 URI 配置
- 密钥管理
- 考勤相关设置（工作时间、迟到阈值）

## 安全考虑

- 基本的基于会话的认证（计划：JWT）
- 密码以明文存储（需要改进）
- 没有可见的 CSRF 保护（计划增强）
- 通过 SQLAlchemy ORM 进行 SQL 注入保护

## 数据库说明

- 默认数据库是 SQLite (`instance/erp.db`)
- 数据库文件未在 Git 中跟踪（被 .gitignore 排除）
- 对于生产环境，考虑使用 PostgreSQL 或 MySQL（如要求中所述）

## 重要文件

- `app.py` - 应用程序入口点
- `app/config.py` - 配置设置
- `app/__init__.py` - 应用工厂
- `requirements.txt` - Python 依赖
- `environment.yml` - Conda 环境规范
- `plan.md` - 详细开发路线图
- `README.md` - 项目文档（中文）