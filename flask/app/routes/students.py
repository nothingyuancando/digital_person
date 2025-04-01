from flask import Blueprint, request, jsonify
from puweb.new.app.services.dbmanage.db_manager_plus import DatabaseManager

student_bp = Blueprint('students', __name__, url_prefix='/api/students')


@student_bp.route('/', methods=['POST'])
def create_student():
    data = request.json
    try:
        student = DatabaseManager.create_student(
            student_id=data['student_id'],
            name=data['name']
        )
        return jsonify({
            'code': 200,
            'data': {
                'student_id': student.student_id,
                'name': student.name
            }
        }), 201
    except Exception as e:
        return jsonify({'code': 400, 'msg': str(e)}), 400


@student_bp.route('/<string:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        student = DatabaseManager.get_student(student_id)
        if not student:
            return jsonify({'code': 404, 'msg': 'ѧ��������'}), 404

        return jsonify({
            'code': 200,
            'data': {
                'student_id': student.student_id,
                'name': student.name
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500


@student_bp.route('/<string:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    try:
        student = DatabaseManager.get_student(student_id)
        if not student:
            return jsonify({'code': 404, 'msg': 'ѧ��������'}), 404

        student.update(**data)
        return jsonify({'code': 200, 'msg': '���³ɹ�'})
    except Exception as e:
        return jsonify({'code': 400, 'msg': str(e)}), 400


@student_bp.route('/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        student = DatabaseManager.get_student(student_id)
        if not student:
            return jsonify({'code': 404, 'msg': 'ѧ��������'}), 404

        student.delete()
        return jsonify({'code': 200, 'msg': 'ɾ���ɹ�'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

