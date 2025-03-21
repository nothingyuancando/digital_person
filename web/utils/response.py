"""
统一响应工具模块
标准化API响应格式
"""

from flask import jsonify

def format_response(success, message, data=None, code=200):
    """统一响应格式"""
    return jsonify({
        "success": success,
        "code": code,
        "message": message,
        "data": data
    }), code

def success_response(data=None, message="操作成功"):
    """成功响应快捷方法"""
    return format_response(True, message, data)

def error_response(message, code=400, data=None):
    """错误响应快捷方法"""
    return format_response(False, message, data, code)