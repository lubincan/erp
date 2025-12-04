# ERP企业资源规划系统

## 项目概述

本项目是一个基于Python开发的企业资源规划（ERP）系统，旨在帮助企业实现业务流程的数字化管理，提高运营效率和管理水平。

## 技术栈

- **后端框架**: Flask / Django
- **数据库**: PostgreSQL / MySQL
- **前端**: HTML5 + CSS3 + JavaScript (可选Vue.js/React)
- **ORM**: SQLAlchemy / Django ORM
- **认证**: JWT Token
- **API**: RESTful API

## 功能需求

### 1. 用户管理模块
- 用户注册、登录、登出
- 用户信息管理（增删改查）
- 密码加密存储
- 用户角色管理（管理员、普通用户、财务、采购、销售等）
- 用户权限控制

### 2. 权限管理模块
- 基于角色的访问控制（RBAC）
- 菜单权限管理
- 功能权限管理
- 数据权限控制

### 3. 库存管理模块
- 商品信息管理（商品编码、名称、规格、单位、价格等）
- 仓库管理（多仓库支持）
- 库存查询（实时库存、库存预警）
- 入库管理（采购入库、退货入库、调拨入库）
- 出库管理（销售出库、退货出库、调拨出库）
- 库存盘点
- 库存调拨
- 库存报表统计

### 4. 采购管理模块
- 供应商管理（供应商信息、联系方式、信用等级）
- 采购订单管理（创建、审核、执行、完成）
- 采购入库管理
- 采购退货管理
- 采购统计分析（采购金额、采购趋势、供应商评价）

### 5. 销售管理模块
- 客户管理（客户信息、联系方式、信用等级）
- 销售订单管理（创建、审核、发货、完成）
- 销售出库管理
- 销售退货管理
- 销售统计分析（销售额、销售趋势、客户分析）

### 6. 财务管理模块
- 应收款管理（客户应收、收款记录）
- 应付款管理（供应商应付、付款记录）
- 收支流水记录
- 财务报表（利润表、资产负债表、现金流量表）
- 成本核算

### 7. 报表统计模块
- 销售报表（日报、月报、年报）
- 采购报表
- 库存报表
- 财务报表
- 自定义报表查询
- 数据可视化（图表展示）

### 8. 系统设置模块
- 基础数据配置（单位、币种、税率等）
- 系统参数设置
- 操作日志记录
- 数据备份与恢复

## 非功能需求

### 性能要求
- 系统响应时间 < 2秒
- 支持并发用户数 ≥ 100
- 数据库查询优化

### 安全要求
- 用户密码加密存储（bcrypt）
- API接口认证（JWT Token）
- SQL注入防护
- XSS攻击防护
- 操作日志记录

### 可用性要求
- 系统可用性 ≥ 99%
- 数据备份机制
- 异常处理机制

### 可维护性要求
- 代码规范统一
- 模块化设计
- 完善的注释和文档
- 单元测试覆盖

## 数据库设计

### 核心数据表
- users（用户表）
- roles（角色表）
- permissions（权限表）
- products（商品表）
- warehouses（仓库表）
- inventory（库存表）
- suppliers（供应商表）
- customers（客户表）
- purchase_orders（采购订单表）
- sales_orders（销售订单表）
- purchase_invoices（采购发票表）
- sales_invoices（销售发票表）
- accounts_receivable（应收款表）
- accounts_payable（应付款表）
- transactions（交易流水表）

## 开发环境要求

- Python 3.8+
- PostgreSQL 12+ / MySQL 8.0+
- Git
- IDE: VSCode / PyCharm

## 项目结构

```
erp/
├── app/                    # 应用主目录
│   ├── __init__.py        # 应用初始化
│   ├── models/            # 数据模型
│   ├── views/             # 视图/路由
│   ├── services/          # 业务逻辑层
│   ├── utils/             # 工具函数
│   ├── middleware/        # 中间件
│   └── config.py          # 配置文件
├── migrations/            # 数据库迁移文件
├── tests/                 # 测试文件
├── requirements.txt       # 依赖包
├── .env                   # 环境变量
├── .gitignore            # Git忽略文件
├── README.md             # 项目说明
└── plan.md               # 开发计划
```

## 安装与运行

### 1. 克隆项目
```bash
git clone <repository-url>
cd erp
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
复制 `.env.example` 为 `.env` 并配置数据库连接等信息

### 5. 初始化数据库
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. 运行项目
```bash
python app.py
# 或
flask run
```

## API文档

系统提供RESTful API接口，API文档将在开发完成后补充。

## 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证。

## 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。

