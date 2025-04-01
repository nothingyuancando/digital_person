from flask import Blueprint, request
from services.file_service.file_upload import handle_file_upload, get_processing_status
from utils.response import success_response, error_response

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/course/upload', methods=['POST'])
def upload_file():
    """重构后的文件上传路由"""
    if 'file' not in request.files or 'courseId' not in request.form:
        return error_response("参数缺失", code=400)
    
    try:
        file = request.files['file']
        course_id = request.form['courseId']
        result = handle_file_upload(file, course_id)
        return success_response(data=result, message="文件上传成功")
    
    except ValueError as e:
        return error_response(str(e), code=400)
    except Exception as e:
        return error_response(f"服务器处理错误: {str(e)}", code=500)

@upload_bp.route('/course/process-status', methods=['GET'])
def check_process_status():
    """重构后的进度查询路由"""
    process_id = request.args.get('processId')
    if not process_id:
        return error_response("缺少processId参数", code=400)
    
    try:
        status_data = get_processing_status(process_id)
        return success_response(data=status_data)
    except ValueError as e:
        return error_response(str(e), code=404)
    except Exception as e:
        return error_response(f"查询失败: {str(e)}", code=500)