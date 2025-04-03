# -*- coding: utf-8 -*-  # 添加文件编码声明
import requests
import json
def test_add_stu():
    base_url = 'http://localhost:5000/'
    test_id = 'stu2024001'
    print("1. 测试创建学生...")
    print("")
    create_data = {
        'student_id': test_id,
        'name': '张三'
    }
    response = requests.post(f"{base_url}/api/students/", json=create_data)
    print(f"响应状态: {response.status_code}")
    print(f"响应内容: {response.json()}")
    pass

# 配置信息
base_url = 'http://localhost:5000'
course_base = f"{base_url}/api/courses"
conv_base = f"{base_url}/api/conversations"
student_base = f"{base_url}/api/students"

# 测试用ID
test_course_id = "cos_2024001"
test_student_id = "stu_2024001"
test_record_id = "rec_2024001"


def test_courses():
    print("\n========== 课程路由测试 ==========")

    # 先创建依赖的学生
    print("\n0. 创建依赖学生...")
    student_data = {'student_id': test_student_id, 'name': '测试学生'}
    response = requests.post(f"{student_base}/", json=student_data)
    print(f"创建学生状态: {response.status_code}")

    # 1. 测试创建课程
    print("\n1. 测试创建课程")
    course_data = {
        'course_id': test_course_id,
        'course_name': '人工智能导论',
        'description': 'AI基础课程'
    }
    response = requests.post(f"{course_base}/", json=course_data)
    print(f"创建响应: {response.status_code}, 内容: {response.json()}")

    # 2. 测试重复创建
    print("\n2. 测试重复创建")
    response = requests.post(f"{course_base}/", json=course_data)
    print(f"重复创建响应: {response.status_code}")

    # 3. 获取单个课程
    print("\n3. 获取指定课程")
    response = requests.get(f"{course_base}/{test_course_id}")
    print(f"获取响应: {response.status_code}")
    print("课程详情:", json.dumps(response.json(), indent=2, ensure_ascii=False))

    # 4. 更新课程
    print("\n4. 更新课程信息")
    update_data = {
        'course_name': '高级人工智能',
        'description': '研究生级别课程'
    }
    response = requests.put(f"{course_base}/{test_course_id}", json=update_data)
    print(f"更新响应: {response.status_code}")

    # 验证更新
    response = requests.get(f"{course_base}/{test_course_id}")
    updated_name = response.json()['data']['course_name']
    print(f"更新验证: 课程名称是否变为'高级人工智能': {updated_name == '高级人工智能'}")

    # 5. 获取所有课程
    print("\n5. 获取所有课程")
    response = requests.get(f"{course_base}/")
    print(f"响应记录数: {len(response.json()['data'])}")

    # 6. 删除课程
    print("\n6. 删除课程")
    response = requests.delete(f"{course_base}/{test_course_id}")
    print(f"删除响应: {response.status_code}")

    # 7. 删除不存在课程
    print("\n7. 删除不存在课程")
    response = requests.delete(f"{course_base}/invalid_id")
    print(f"响应状态: {response.status_code}")


def test_conversations():
    print("\n========== 对话路由测试 ==========")

    # 创建前置依赖
    print("\n0. 创建依赖数据...")
    requests.post(f"{student_base}/", json={'student_id': test_student_id, 'name': '测试学生'})
    requests.post(f"{course_base}/", json={'course_id': test_course_id, 'course_name': '测试课程'})

    # 1. 创建对话记录
    print("\n1. 创建对话记录")
    conv_data = {
        'record_id': test_record_id,
        'student_id': test_student_id,
        'course_id': test_course_id,
        'keyword': '机器学习',
        'details': [
            {'question': '什么是过拟合？', 'score': 85},
            {'question': '正则化的作用', 'score': 90}
        ]
    }
    response = requests.post(f"{conv_base}/", json=conv_data)
    print(f"创建响应: {response.status_code}, 返回数据: {response.json()}")

    # 2. 获取对话详情
    print("\n2. 获取对话详情")
    response = requests.get(f"{conv_base}/{test_record_id}")
    print(f"响应状态: {response.status_code}")
    print("详情数据:", json.dumps(response.json(), indent=2, ensure_ascii=False))

    # 3. 更新对话记录
    print("\n3. 更新对话记录")
    update_data = {
        'keyword': '深度学习',
        'analysis_report': '需要加强实践环节',
        'details': [
            {'question': '什么是过拟合？', 'score': 88},
            {'question': '正则化的作用', 'score': 92}
        ]
    }
    response = requests.put(f"{conv_base}/{test_record_id}", json=update_data)
    print(f"更新响应: {response.status_code}")

    # 4. 获取所有对话
    print("\n4. 获取所有对话")
    response = requests.get(f"{conv_base}/")
    print(f"找到{len(response.json()['data'])}条记录")

    # 5. 删除对话
    print("\n5. 删除对话记录")
    response = requests.delete(f"{conv_base}/{test_record_id}")
    print(f"删除响应: {response.status_code}")

    # 清理测试数据
    requests.delete(f"{course_base}/{test_course_id}")
    requests.delete(f"{student_base}/{test_student_id}")
def test_details():
    print("\n========== 对话详情路由测试 ==========")
    detail_base = f"{base_url}/api/details"
    test_detail_id = None  # 用于保存测试详情的ID

    # 创建前置依赖
    print("\n0. 创建依赖数据...")
    record_data = {
        'record_id': test_record_id,
        'student_id': test_student_id,
        'course_id': test_course_id,
        'details': []
    }
    requests.post(f"{student_base}/", json={'student_id': test_student_id, 'name': '测试学生'})
    requests.post(f"{course_base}/", json={'course_id': test_course_id, 'course_name': '测试课程'})
    requests.post(f"{conv_base}/", json=record_data)

    try:
        # 1. 测试创建详情
        print("\n1. 测试创建对话详情")
        detail_data = {
            'record_id': test_record_id,
            'conversation_no': 1,
            'question': '什么是机器学习？',
            'student_answer': '让计算机学习数据规律',
            'score': 85.5
        }
        response = requests.post(f"{detail_base}/", json=detail_data)
        print(f"创建响应: {response.status_code}, 内容: {response.json()}")
        test_detail_id = response.json()['data']['detail_id']

        # 2. 测试无效创建（缺少必填字段）
        print("\n2. 测试缺少必填字段")
        invalid_data = {'record_id': test_record_id}
        response = requests.post(f"{detail_base}/", json=invalid_data)
        print(f"响应状态: {response.status_code}, 错误信息: {response.json()['msg']}")

        # 3. 获取单个详情
        print("\n3. 获取对话详情")
        response = requests.get(f"{detail_base}/{test_detail_id}")
        print(f"响应状态: {response.status_code}")
        print("详情数据:", json.dumps(response.json(), indent=2, ensure_ascii=False))

        # 4. 更新详情
        print("\n4. 更新对话详情")
        update_data = {
            'score': 90.0,
            'reference_answer': '通过数据训练模型'
        }
        response = requests.put(f"{detail_base}/{test_detail_id}", json=update_data)
        print(f"更新响应: {response.status_code}")

        # 验证更新
        response = requests.get(f"{detail_base}/{test_detail_id}")
        updated_score = response.json()['data']['score']
        print(f"更新验证: 分数是否变为90 → {updated_score == 90}")

        # 5. 测试无效更新（错误类型）
        print("\n5. 测试无效类型更新")
        invalid_update = {'conversation_no': 'invalid_number'}
        response = requests.put(f"{detail_base}/{test_detail_id}", json=invalid_update)
        print(f"响应状态: {response.status_code}")

        # # 6. 获取关联详情列表
        # print("\n6. 获取关联详情列表")
        # response = requests.get(f"{conv_base}/{test_record_id}/details")
        # print(f"找到{len(response.json()['data'])}条详情记录")

        # 7. 删除详情
        print("\n7. 删除对话详情")
        response = requests.delete(f"{detail_base}/{test_detail_id}")
        print(f"删除响应: {response.status_code}")

        # 8. 删除不存在详情
        print("\n8. 删除不存在详情")
        response = requests.delete(f"{detail_base}/999999")
        print(f"响应状态: {response.status_code}")

    finally:
        # 清理测试数据
        print("\n清理测试数据...")
        if test_detail_id:
            requests.delete(f"{detail_base}/{test_detail_id}")
        requests.delete(f"{conv_base}/{test_record_id}")
        requests.delete(f"{course_base}/{test_course_id}")
        requests.delete(f"{student_base}/{test_student_id}")