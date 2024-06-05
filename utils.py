from flask import request, jsonify
from functools import wraps


# 定义装饰器函数
def validate_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # 从请求中获取 token
        token = request.headers.get("check-token")
        # 检查 token 的有效性
        if token == "1C168F31197B4C4F":
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Invalid token"}), 401

    return wrapper
