#学生评分接口

from flask import Blueprint, request
from models import Student, ConversationRecord, ConversationDetail
from utils.response import success_response, error_response

bp = Blueprint('student', __name__, url_prefix='/api/student')

@bp.route('/grade', methods=['GET'])
def get_student_grade():
    student_id = request.args.get('studentId')
    record_id = request.args.get('recordId')

    if not student_id or not record_id:
        return error_response("缺少必要参数", 400)

    # 验证学生存在
    student = Student.query.get(student_id)
    if not student:
        return error_response("学生不存在", 404)

    # 获取对话记录
    record = ConversationRecord.query.get(record_id)
    if not record:
        return error_response("对话记录不存在", 404)

    # 获取对话详情
    details = ConversationDetail.query.filter_by(
        record_id=record_id
    ).order_by(ConversationDetail.conversation_no).all()

    response_data = {
        "studentInfo": {
            "name": student.name,
            "studentId": student.student_id
        },
        "averageScore": float(record.average_score),
        "grade": record.grade,
        "conversation": [{
            "conversationId": str(detail.detail_id),
            "question": detail.question,
            "studentAnswer": detail.student_answer,
            "referenceAnswer": detail.reference_answer,
            "score": float(detail.score) if detail.score else None
        } for detail in details],
        "analysisReport": record.analysis_report
    }

    return success_response(response_data)