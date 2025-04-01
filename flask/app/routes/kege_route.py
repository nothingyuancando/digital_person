from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from services.kege_service import process_uploaded_file
from ..models import Task
from ..extensions import db

bp = Blueprint('upload', __name__, url_prefix='/api')

@bp.route('/upload', methods=['POST'])
def upload_file():
    # 文件上传验证
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "未选择文件"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "空文件名"}), 400
    
    # 创建任务记录
    new_task = Task(status='uploading', progress=0)
    db.session.add(new_task)
    db.session.commit()

    try:
        # 异步处理文件
        process_uploaded_file.delay(file, new_task.id)
        return jsonify({
            "status": "processing",
            "task_id": new_task.id,
            "message": "文件已接收，开始处理"
        }), 202
    except Exception as e:
        new_task.status = 'failed'
        db.session.commit()
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/progress/<int:task_id>')
def get_progress(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({
        "status": task.status,
        "progress": task.progress,
        "details": task.message
    })