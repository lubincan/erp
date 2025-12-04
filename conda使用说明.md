# Conda环境使用说明

## 快速开始

### Windows系统

#### 1. 配置Conda环境（首次使用）

双击运行 `setup_conda.bat`，或在命令行中执行：
```bash
setup_conda.bat
```

#### 2. 启动项目

双击运行 `start_conda.bat`，或在命令行中执行：
```bash
start_conda.bat
```

### Linux/Mac系统

#### 1. 配置Conda环境（首次使用）

```bash
chmod +x setup_conda.sh
bash setup_conda.sh
```

#### 2. 启动项目

```bash
chmod +x start_conda.sh
bash start_conda.sh
```

## 手动使用Conda环境

### 1. 创建环境（如果还没创建）

```bash
conda env create -f environment.yml
```

### 2. 激活环境

```bash
conda activate erp
```

### 3. 安装/更新依赖

```bash
# 如果使用environment.yml创建的环境，依赖已自动安装
# 如果需要手动安装，可以使用：
pip install -r requirements.txt
```

### 4. 运行项目

```bash
python app.py
```

### 5. 退出环境

```bash
conda deactivate
```

## 环境管理命令

### 查看所有环境
```bash
conda env list
```

### 更新环境
```bash
conda env update -f environment.yml --prune
```

### 删除环境
```bash
conda env remove -n erp
```

### 导出环境配置
```bash
conda env export > environment.yml
```

## 环境信息

- **环境名称**: erp
- **Python版本**: 3.10
- **主要依赖**:
  - Flask 3.0.0
  - Flask-SQLAlchemy 3.1.1
  - Flask-CORS 4.0.0
  - Werkzeug 3.0.1
  - python-dotenv 1.0.0

## 常见问题

### 1. conda命令未找到

**问题**: 提示 `conda: command not found`

**解决**:
- Windows: 确保Anaconda已添加到系统PATH，或使用Anaconda Prompt
- Linux/Mac: 运行 `source ~/anaconda3/bin/activate` 或添加到 `.bashrc`

### 2. 环境创建失败

**问题**: 创建环境时出错

**解决**:
- 检查网络连接
- 尝试使用国内镜像源：
  ```bash
  conda config --add channels conda-forge
  conda config --set show_channel_urls yes
  ```

### 3. 依赖安装失败

**问题**: pip安装依赖时出错

**解决**:
- 使用国内镜像源：
  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

### 4. 环境激活失败

**问题**: `conda activate erp` 失败

**解决**:
- Windows: 使用 `call conda activate erp`
- Linux/Mac: 确保已初始化conda: `eval "$(conda shell.bash hook)"`

## 优势

使用Conda环境的优势：
- ✅ 隔离的项目依赖，不影响系统Python
- ✅ 易于管理和切换不同项目环境
- ✅ 可以指定Python版本
- ✅ 便于团队协作，环境配置统一

## 下一步

环境配置完成后，访问 http://127.0.0.1:5000 使用系统。

