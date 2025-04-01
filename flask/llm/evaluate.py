import json
import os
import dashscope


#结构化输入
#将问题与参考答案存储到json文件
'''
问题内容
学生回答
标准答案
//所属科目
'''
def generate_questions_from_kg(knowledge_graph):
    questions = []
    for entity in knowledge_graph.entities:
        questions.append({
            "question": f"什么是{entity.name}?",
            "reference_answer": entity.description  # 参考答案
        })
    return questions

#设计大模型评估prompt
evaluation_prompt_template = """
请根据以下信息评估学生的回答：
---
**问题**：{question}
**参考答案**：{reference_answer}
**学生回答**：{student_answer}
---
评估要求：
1. 满分100分，从准确性（60%）、完整性（30%）、语言表达（10%）评分。
2. 指出回答中的错误或遗漏。
3. 用JSON格式返回结果，包含score和feedback字段。

评估结果：
"""
#评估函数
def evaluate_student_answer(question, student_answer, reference_answer):
    #大模型输入
    prompt = evaluation_prompt_template.format(
        question=question,
        reference_answer=reference_answer,
        student_answer=student_answer
    )
    #回答
    messages = [
    {'role': 'system', 'content': prompt}
    #{'role': 'user', 'content': prompt}
    ]
    response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    #api_key=os.getenv('DASHSCOPE_API_KEY'),
    api_key="sk-5fb4c90206e84a7b9d88fc91e72fbe44",
    model="qwen-turbo", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages,
    result_format='message',
    response_format={"type": "json_object"}
    )
    
    # 解析模型输出
    try:
        result = json.loads(response.output.choices[0].message.content)
        return result
    except:
        return {"error": "评估失败，请检查模型输出格式"}
    


