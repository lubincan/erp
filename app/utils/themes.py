"""
主题管理工具
"""
import json
from flask import session

# 预定义主题
THEMES = {
    'default': {
        'name': '默认紫色',
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'button_primary': '#667eea',
        'button_hover': '#764ba2',
        'accent': '#667eea',
        'shadow': 'rgba(0,0,0,0.3)'
    },
    'ocean': {
        'name': '海洋蓝',
        'background': 'linear-gradient(135deg, #2196F3 0%, #21CBF3 100%)',
        'button_primary': '#2196F3',
        'button_hover': '#21CBF3',
        'accent': '#2196F3',
        'shadow': 'rgba(33, 150, 243, 0.3)'
    },
    'sunset': {
        'name': '日落橙',
        'background': 'linear-gradient(135deg, #ff6b6b 0%, #feca57 100%)',
        'button_primary': '#ff6b6b',
        'button_hover': '#feca57',
        'accent': '#ff6b6b',
        'shadow': 'rgba(255, 107, 107, 0.3)'
    },
    'forest': {
        'name': '森林绿',
        'background': 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
        'button_primary': '#11998e',
        'button_hover': '#38ef7d',
        'accent': '#11998e',
        'shadow': 'rgba(17, 153, 142, 0.3)'
    },
    'midnight': {
        'name': '午夜黑',
        'background': 'linear-gradient(135deg, #232526 0%, #414345 100%)',
        'button_primary': '#414345',
        'button_hover': '#232526',
        'accent': '#414345',
        'shadow': 'rgba(65, 67, 69, 0.3)'
    },
    'cherry': {
        'name': '樱花粉',
        'background': 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
        'button_primary': '#ff9a9e',
        'button_hover': '#fecfef',
        'accent': '#ff9a9e',
        'shadow': 'rgba(255, 154, 158, 0.3)'
    }
}

def get_current_theme():
    """获取当前主题"""
    return session.get('theme', 'default')

def set_theme(theme_name):
    """设置当前主题"""
    if theme_name in THEMES:
        session['theme'] = theme_name
        session.modified = True  # 确保session被保存
        return True
    return False

def get_theme_css(theme_name):
    """获取主题的CSS变量"""
    theme = THEMES.get(theme_name, THEMES['default'])
    return f"""
    :root {{
        --theme-background: {theme['background']};
        --theme-button-primary: {theme['button_primary']};
        --theme-button-hover: {theme['button_hover']};
        --theme-accent: {theme['accent']};
        --theme-shadow: {theme['shadow']};
    }}
    """

def get_all_themes():
    """获取所有主题列表"""
    return THEMES