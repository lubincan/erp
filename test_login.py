#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试登录功能
"""
import requests
import json

def test_login():
    """测试登录功能"""
    base_url = "http://127.0.0.1:5000"

    print("=== ERP系统登录功能测试 ===")

    # 测试登录API
    print("\n1. 测试登录API...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }

    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )

        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ 登录成功! 用户: {data['data']['name']}")
            return data['data']
        else:
            print("❌ 登录失败")
            return None

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保ERP系统正在运行")
        return None
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return None

def test_check_auth():
    """测试认证状态检查"""
    base_url = "http://127.0.0.1:5000"

    print("\n2. 测试认证状态检查...")

    try:
        response = requests.get(f"{base_url}/api/auth/check_auth")

        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")

        if response.status_code == 200:
            print("✅ 认证状态检查正常")
        else:
            print("❌ 认证状态检查失败")

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保ERP系统正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_register():
    """测试用户注册"""
    base_url = "http://127.0.0.1:5000"

    print("\n3. 测试用户注册...")

    # 创建测试用户
    register_data = {
        "username": "testuser",
        "name": "测试用户",
        "email": "test@example.com",
        "password": "test123"
    }

    try:
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )

        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")

        if response.status_code == 200:
            print("✅ 用户注册成功")
        else:
            print("❌ 用户注册失败")

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保ERP系统正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    print("ERP系统登录功能测试")
    print("=" * 50)

    # 测试登录
    user_data = test_login()

    # 测试认证状态检查
    test_check_auth()

    # 测试用户注册
    test_register()

    print("\n" + "=" * 50)
    print("测试完成")

    # 如果登录成功，显示使用说明
    if user_data:
        print(f"\n🎉 登录成功！用户信息:")
        print(f"   用户名: {user_data['username']}")
        print(f"   姓名: {user_data['name']}")
        print(f"   角色: {user_data['role']}")
        print(f"\n📋 使用说明:")
        print(f"   1. 访问 http://127.0.0.1:5000/api/auth/login 进行登录")
        print(f"   2. 访问 http://127.0.0.1:5000/api/attendance/ 进行打卡")
        print(f"   3. 访问 http://127.0.0.1:5000/api/auth/profile 查看个人资料")