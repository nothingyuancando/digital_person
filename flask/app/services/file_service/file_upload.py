from utils.response import error_response

def handle_file_upload(file, course_id):
    """重构后的文件处理服务"""
    if file.filename == '':
        raise ValueError("未选择文件")
    if not allowed_file(file.filename):
        raise ValueError("仅支持PDF/DOCX格式文件")
    
    # ...（原有文件处理逻辑保持不变）...
    
    return {
        "processId": process_id,
        "courseId": course_id,
        "fileName": filename
    }

def get_processing_status(process_id):
    """重构后的状态查询服务"""
    record = CourseFile.query.get(process_id)
    if not record:
        raise ValueError("处理记录不存在")
    
    return {
        "status": record.status,
        "progress": record.progress,
        "createdAt": record.created_at.isoformat(),
        "courseName": record.course.course_name  # 关联查询示例
    }