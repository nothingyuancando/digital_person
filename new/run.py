# -*- coding: utf-8 -*-  # 添加文件编码声明
from app.__init__ import create_app
from test2 import test_add_stu,test_conversations,test_details,test_courses
app = create_app()




@app.route('/')
def hello_world():
    test_add_stu()
    test_courses()
    test_conversations()
    test_details()
    try:
        #setup_module(None)
        #test_section_flow()
        #test_knowledge_point_flow()
        # test_question_flow()
        pass
    finally:
        #teardown_module(None)
        pass

    return 'hhh'

if __name__ == '__main__':


    app.run()
