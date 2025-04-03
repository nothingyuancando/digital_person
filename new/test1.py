import requests
# 配置信息
base_url = 'http://localhost:5000'
course_base = f"{base_url}/api/courses"
section_base = f"{base_url}/api/courses/{{course_id}}/sections/"
kp_base = f"{base_url}/api/sections/{{section_id}}/knowledge_points/"
question_base = f"{base_url}/api/sections/{{section_id}}/questions/"

# 测试用ID
test_course_id = "551"
test_section_id = "616"  # 动态获取
test_kp_id = "771"  # 动态获取
test_question_id = "188"  # 动态获取

def setup_module(module):
    """初始化测试数据"""
    # 创建测试课程
    course_data = {'course_id': test_course_id, 'course_name': '测试课程'}
    requests.post(f"{course_base}/", json=course_data)

def teardown_module(module):
    """清理测试数据"""
    # 删除测试课程及其关联数据
    requests.delete(f"{course_base}/{test_course_id}")

def test_section_flow():
    global test_section_id
    print("\n========== 章节路由测试 ==========")

    #1. 创建章节
    print("\n1. 测试创建章节")
    section_data = {'section_name': '测试章节','section_id': test_section_id}
    response = requests.post(
        section_base.format(course_id=test_course_id),
        json=section_data
    )
    assert response.status_code == 201
    test_section_id = response.json()['data']['section_id']
    print("创建章节ID:", test_section_id)

    # 2. 获取所有章节
    print("\n2. 获取课程所有章节")
    response = requests.get(section_base.format(course_id=test_course_id))
    assert response.status_code == 200
    assert len(response.json()['data']) > 0
    print("章节数:", len(response.json()['data']))

    # 3. 获取单个章节
    print("\n3. 获取指定章节详情")
    response = requests.get(
        f"{section_base.format(course_id=test_course_id)}{test_section_id}"
    )
    assert response.status_code == 200
    assert response.json()['data']['section_name'] == '测试章节'

    # 4. 更新章节
    print("\n4. 更新章节信息")
    update_data = {'section_name': '更新后的章节'}
    response = requests.put(
        f"{section_base.format(course_id=test_course_id)}{test_section_id}",
        json=update_data
    )
    assert response.status_code == 200
    # 验证更新
    response = requests.get(
        f"{section_base.format(course_id=test_course_id)}{test_section_id}"
    )
    assert response.json()['data']['section_name'] == '更新后的章节'

    #5. 测试跨课程移动
    print("\n5. 测试跨课程移动（异常场景）")
    new_course = "invalid_course_999"
    update_data = {'course_id': new_course}
    response = requests.put(
        f"{section_base.format(course_id=test_course_id)}{test_section_id}",
        json=update_data
    )
    assert response.status_code == 404
#"GET /api/sections/616/knowledge_points/771 HTTP/1.1" 200 -
#"GET /api/sections/616/knowledge_points/771 HTTP/1.1" 500 -

def test_knowledge_point_flow():
    global test_section_id, test_kp_id
    print("\n========== 知识点路由测试 ==========")

    # 1. 创建知识点
    print("\n1. 创建知识点")
    kp_data = {
        'point_id': test_kp_id,
        'title': '测试知识点',
        'content': '这是测试内容'
    }
    response = requests.post(
        kp_base.format(section_id=test_section_id),
        json=kp_data
    )
    assert response.status_code == 201
    test_kp_id = response.json()['data']['point_id']
    print("知识点ID:", test_kp_id)

    # 2. 获取知识点详情
    print("\n2. 获取知识点详情")
    response = requests.get(
        f"{kp_base.format(section_id=test_section_id)}{test_kp_id}"
    )
    assert response.status_code == 200
    assert response.json()['data']['title'] == '测试知识点'

    # 3. 获取章节下所有知识点
    print("\n3. 获取章节知识点列表")
    response = requests.get(
        f"{kp_base.format(section_id=test_section_id)}"
    )
    assert response.status_code == 200
    assert len(response.json()['data']) > 0

    # 4. 更新知识点
    print("\n4. 更新知识点内容")
    update_data = {'title': '更新后的标题', 'content': '更新后的内容'}
    response = requests.put(
        f"{kp_base.format(section_id=test_section_id)}{test_kp_id}",
        json=update_data
    )
    assert response.status_code == 200
    # 验证更新
    response = requests.get(
        f"{kp_base.format(section_id=test_section_id)}{test_kp_id}"
    )
    assert response.json()['data']['title'] == '更新后的标题'

    # 5. 测试跨章节移动
    print("\n5. 测试跨章节移动（异常场景）")
    update_data = {'section_id': 999999}
    response = requests.put(
        f"{kp_base.format(section_id=test_section_id)}{test_kp_id}",
        json=update_data
    )
    assert response.status_code == 404

def test_question_flow():
    global test_section_id, test_question_id
    print("\n========== 问题路由测试 ==========")

    # 1. 创建问题
    print("\n1. 创建问题")
    question_data = {
        'question_id': test_question_id,
        'question': '测试问题内容',
        'answer': '标准答案'

    }
    response = requests.post(
        question_base.format(section_id=test_section_id),
        json=question_data
    )
    assert response.status_code == 201
    test_question_id = response.json()['data']['question_id']
    print("问题ID:", test_question_id)

    # 2. 获取问题详情
    print("\n2. 获取问题详情")

    response = requests.get(
        f"{question_base.format(section_id=test_section_id)}{test_question_id}"
    )
    assert response.status_code == 200
    assert response.json()['data']['question'] == '测试问题内容'

   # 3. 获取章节下所有问题
    print("\n3. 获取章节问题列表")
    response = requests.get(
        f"{question_base.format(section_id=test_section_id)}"
    )
    print(response.status_code)
    assert response.status_code == 200
    assert len(response.json()['data']) > 0

    # 4. 更新问题
    print("\n4. 更新问题内容")
    update_data = {'question': '更新后的问题内容','answer': 'new answer'}
    response = requests.put(
        f"{question_base.format(section_id=test_section_id)}{test_question_id}",
        json=update_data
    )
    assert response.status_code == 200
    # 验证更新

    response = requests.get(
        f"{question_base.format(section_id=test_section_id)}{test_question_id}"
    )
    print(response.json())
    assert response.json()['data']['question'] == '更新后的问题内容'

    # 5. 测试级联删除
    print("\n5. 测试级联删除")
    delete_response = requests.delete(
        f"{section_base.format(course_id=test_course_id)}{test_section_id}"
    )
    assert delete_response.status_code == 200
    # 验证关联数据删除
    kp_response = requests.get(
        f"{kp_base.format(section_id=test_section_id)}{test_kp_id}"
    )
    assert kp_response.status_code == 404
    question_response = requests.get(
        f"{question_base.format(section_id=test_section_id)}{test_question_id}"
    )
    assert question_response.status_code == 404