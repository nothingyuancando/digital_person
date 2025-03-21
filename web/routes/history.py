#历史记录接口

from flask import Blueprint, request
from models import ConversationRecord, Course
from utils.response import success_response, error_response
from sqlalchemy import or_

bp = Blueprint('history', __name__, url_prefix='/api/history')

@bp.route('/conversations', methods=['GET'])
def get_conversation_list():
    # 参数处理
    student_id = request.args.get('studentId')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)

    if not student_id:
        return error_response("缺少学生ID参数", 400)

    # 分页查询
    query = ConversationRecord.query.filter_by(student_id=student_id)
    pagination = query.paginate(page=page, per_page=page_size)

    records = []
    for record in pagination.items:
        course = Course.query.get(record.course_id)
        records.append({
            "recordId": record.record_id,
            "conversationTime": record.conversation_time.isoformat(),
            "courseName": course.course_name if course else "",
            "keyword": record.keyword
        })

    return success_response({
        "totalRecords": pagination.total,
        "records": records
    })

@bp.route('/search', methods=['GET'])
def search_conversations():
    # 参数处理
    student_id = request.args.get('studentId')
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)

    if not student_id or not keyword:
        return error_response("缺少必要参数", 400)

    # 构建查询条件
    query = ConversationRecord.query.filter(
        ConversationRecord.student_id == student_id,
        or_(
            ConversationRecord.keyword.ilike(f"%{keyword}%"),
            Course.course_name.ilike(f"%{keyword}%")
        )
    ).join(Course)

    # 分页处理
    pagination = query.paginate(page=page, per_page=page_size)

    records = []
    for record in pagination.items:
        records.append({
            "recordId": record.record_id,
            "conversationTime": record.conversation_time.isoformat(),
            "courseName": record.course.course_name,
            "keyword": record.keyword
        })

    return success_response({
        "totalRecords": pagination.total,
        "records": records
    })

@bp.route('/conversation-detail', methods=['GET'])
def get_conversation_detail():
    record_id = request.args.get('recordId')
    if not record_id:
        return error_response("缺少记录ID参数", 400)

    record = ConversationRecord.query.get(record_id)
    if not record:
        return error_response("记录不存在", 404)

    details = ConversationDetail.query.filter_by(
        record_id=record_id
    ).order_by(ConversationDetail.conversation_no).all()

    course = Course.query.get(record.course_id)

    response_data = {
        "recordId": record.record_id,
        "conversationTime": record.conversation_time.isoformat(),
        "courseName": course.course_name if course else "",
        "keyword": record.keyword,
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