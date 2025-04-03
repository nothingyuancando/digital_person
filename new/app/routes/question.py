# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from app.models.db_manager import DatabaseManager

question_bp = Blueprint('questions', __name__, url_prefix='/api/sections/<string:section_id>/questions')

@question_bp.route('/', methods=['POST'])
def create_question(section_id):
    data = request.json

    try:
        question = DatabaseManager.create_question(
            question_id=data['question_id'],
            section_id=section_id,
            question_text=data['question'],
            answer_text=data['answer']
        )
        return jsonify({
            'code': 201,
            'data': {
                'question_id': question.question_id,
                'question': question.question
            }
        }), 201
    except Exception as e:
        return jsonify({'code': 400, 'msg': str(e)}), 400

@question_bp.route('/<string:question_id>', methods=['GET'])
def get_question(section_id,question_id):

    try:

        question = DatabaseManager.get_question(question_id)

        if not question:
            return jsonify({'code': 404, 'msg': '问题不存在'}), 404
        return jsonify({
            'code': 200,
            'data': {
                'question_id': question.question_id,
                'section_id': question.section_id,
                'question': question.question,
                'answer':question.answer,
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@question_bp.route('/', methods=['GET'])
def get_questions_by_section(section_id):
    try:

        question = DatabaseManager.get_questions_by_section(section_id)

        if not question:
            return jsonify({'code': 404, 'msg': '问题不存在'}), 404
        return jsonify({
            'code': 200,
            'data': [{
                'question_id': q.question_id,
                'section_id':q.section_id,
                'question': q.question,
                'answer':q.answer,
            } for q in question]
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500


@question_bp.route('/<string:question_id>', methods=['PUT'])
def update_question(section_id, question_id):
    """更新问题内容（支持跨章节移动）"""
    data = request.json

    try:
        # 验证问题存在性
        question = DatabaseManager.get_question(question_id)
        if not question or question.section_id != section_id:
            return jsonify({'code': 404, 'msg': '问题不存在'}), 404

        # 验证新章节存在性（如果修改章节）
        new_section_id = data.get('section_id', section_id)
        if new_section_id != section_id and not DatabaseManager.get_section(new_section_id):
            return jsonify({'code': 404, 'msg': '目标章节不存在'}), 404

        # 执行更新
        print(data.get('question'))
        updated = DatabaseManager.update_question(
            question_id=question_id,
            question=data.get('question'),
            section_id=new_section_id,
            answer=data.get('answer')
        )

        return jsonify({
            'code': 200,
            'data': {
                'question_id': updated.question_id,
                'new_section_id': new_section_id
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500


@question_bp.route('/<string:question_id>', methods=['DELETE'])
def delete_question(section_id, question_id):
    """级联删除问题及关联答案"""
    try:
        question = DatabaseManager.get_question(question_id)
        if not question or question.section_id != section_id:
            return jsonify({'code': 404, 'msg': '问题不存在'}), 404

        success = DatabaseManager.delete_question(question_id)
        return jsonify({
            'code': 200,
            'data': {
                'deleted_question': question_id,
                'related_answers': len(question.answers)
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500