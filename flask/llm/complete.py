import json
import os
import math
import time
import PyPDF2
from docx import Document
from openai import OpenAI
from PyAibote import WinBotMain
import re
import dashscope
from puweb.flask.llm.evaluate import evaluate_student_answer

# 配置qwen模型api
client = OpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key="sk-5fb4c90206e84a7b9d88fc91e72fbe44")


def read_file_content(file_path):
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            k = 0
            content = ""
            for page in reader.pages:
                if k < 30:
                    content += page.extract_text() + '\n\n'
                k += 1
            return content
    elif file_path.endswith('.docx'):
        doc_text = ""
        if os.path.exists(file_path):
            paragraphs = Document(file_path).paragraphs
            for paragraph in paragraphs:
                doc_text += paragraph.text + "\n"
        return doc_text
    return None


def split_string(s, length=15000):
    """
    将字符串按指定的长度切分成多段。

    :param s: 要切分的字符串
    :param length: 切分的字符长度，默认为15000
    :return: 切分后的字符串列表
    """
    return [s[i:i + length] for i in range(0, len(s), length)]


def knowledge_extract(text):
    try:
        # 进行文本切分
        text_list = split_string(text)
        knowledges_list = []
        for doc_text in text_list:
            text_length = len(doc_text)
            knowledge_count = math.ceil(text_length / 1000)
            promt = '''梳理抽取出上面这个文件中涉及的学习或培训知识要点；要
            求整理成一个个小的知识要点。知识点要简短精炼，
            特别注意文档中的试题、示例和案例解析内容不要做为知识点，
            每个知识点的content为当前知识点的完整描述，必须是文档的原文片段，
            可能包含多个段落，请按标准json格式返回，格式如下:
            [{"title": "车间（工段、区、队）级岗前安全培训内容",
            "content": "（一） 工作环境及危险因素； （二） 所从事工种可能遭受的职业伤害和伤亡事故； （三） 所从事工种的安全职责、操作技能及强制性标准； （四）自救互救、急救方法、疏散和现场紧急情况的处理； （五）安全设备设施、个人防护用品的使用和维护； （六）本车间（工段、区、队）安全生产状况及规章制度； （七）预防事故和职业危害的措施及应注意的安全事项； （八）有关事故案例； （九）其他需要培训的内容。"}]；
            结果不要返回除json外其它无关内容,至少包含''' + str(knowledge_count) + '''个知识要点'''

            request_text = str(doc_text) + "\n" + promt
            messsage = [
                {"role": "system",
                 "content": "你是一名学校教师或职业培训老师，你需要根据用户输入的教材或培训材料，梳理出文档材料中涉及到哪些知识点内容，这些内容是学生或企业员工需要掌握的培训要点和知识点"
                 },
                {"role": "user",
                 "content": request_text
                 },
            ]

            start_time = time.time()
            completion = client.chat.completions.create(
                model="qwen-plus",
                messages=messsage
            )
            result = completion.choices[0].message.content

            start = result.rindex("[")
            end = result.rindex("]")
            temp_list = result[start:end + 1]
            temp_list = json.loads(temp_list)
            knowledges_list = knowledges_list + temp_list
            end_time = time.time()
            print(f"该部分运行时间为{end_time - start_time}秒")
        return knowledges_list
    except Exception as e:
        print(e)
        print("第一次抽取错误，开始第二次抽取")
        try:
            text_list = split_string(text)
            knowledges_list = []
            for doc_text in text_list:
                promt = '''#注意，你是一名经验丰富的老师，请梳理抽取出上面这个文件中涉及的必考的重要知识点，整理成一个个小的知识要点。知识点要简短精炼，请按json格式返回，格式如下: [{"title": "车间（工段、区、队）级岗前安全培训内容", "content": "（一） 工作环境及危险因素； （二） 所从事工种可能遭受的职业伤害和伤亡事故； （三） 所从事工种的安全职责、操作技能及强制性标准； （四）自救互救、急救方法、疏散和现场紧急情况的处理； （五）安全设备设施、个人防护用品的使用和维护； （六）本车间（工段、区、队）安全生产状况及规章制度； （七）预防事故和职业危害的措施及应注意的安全事项； （八）有关事故案例； （九）其他需要培训的内容。"}]；结果一定不要返回除json外其它无关内容'''
                request_text = str(doc_text) + "\n" + promt
                messsage = [
                    {"role": "system",
                     "content": "你是一名学校教师或职业培训老师，你需要根据用户输入的材料，梳理出文档材料中涉及到哪些核心内容"
                     },
                    {"role": "user",
                     "content": request_text
                     }
                ]
                start_time1 = time.time()
                completion = client.chat.completions.create(
                    model="ep-20250107152728-vkl7w",
                    messages=messsage
                )
                result = completion.choices[0].message.content

                start = result.rindex("[")
                end = result.rindex("]")
                temp_list = result[start:end + 1]
                temp_list = json.loads(temp_list)
                knowledges_list = knowledges_list + temp_list
                end_time1 = time.time()
                print(f"该部分运行时间为{end_time1 - start_time1}秒")
            return knowledges_list
        except Exception as e:
            print(e)
            print("第二次抽取错误")
            return []


def question_ask(main_knowledge, n):
    # 将知识点列表转换为字符串
    main_knowledge_str = json.dumps(main_knowledge, ensure_ascii=False, indent=4)
    prompt = f"""
    你是一位知识渊博且专业的大学老师，请你根据用户给的关键知识点来提出{n}个值得对学生的问题.
    每个问题都需要清晰且能引发学生的深入思考，{n}个问题尽量能将所给的知识点考察全面.
    不用展示你的思考过程，直接展示问题即可，同时请把握好与学生提问的语气，应当是和蔼可亲的.
    请按标准json格式返回，格式如下:
    {{
    "学科名称": "数据结构",
    "问题列表": 
    [
            {{
                "问题": "请简述二叉树的定义。",
                "参考答案": "二叉树是一种每个节点最多有两个子节点的树状数据结构。这两个子节点通常被称为左子节点和右子节点。特殊情况下，二叉树可以为空树，即没有任何节点；也可以只有一个根节点；或者每个节点都有左右子节点。"
            }},
            {{
                "问题": "二叉树有哪几种常见的遍历方式？",
                "参考答案": "二叉树常见的遍历方式有三种：前序遍历、中序遍历和后序遍历。前序遍历的顺序是先访问根节点，然后递归地前序遍历左子树，最后递归地前序遍历右子树；中序遍历是先递归地中序遍历左子树，然后访问根节点，最后递归地中序遍历右子树；后序遍历则是先递归地后序遍历左子树，接着递归地后序遍历右子树，最后访问根节点。此外，还有层序遍历，它是按照从上到下、从左到右的顺序依次访问二叉树的节点。"
            }},
            {{
                "问题": "如何判断一棵二叉树是否为二叉搜索树？",
                "参考答案": "二叉搜索树满足对于树中的每个节点，其左子树中的所有节点的值都小于该节点的值，而其右子树中的所有节点的值都大于该节点的值。判断一棵二叉树是否为二叉搜索树，可以采用中序遍历的方法。如果中序遍历得到的节点值序列是升序排列的，那么这棵二叉树就是二叉搜索树；否则，不是二叉搜索树。也可以通过递归的方式，为每个节点设置一个取值范围，若该节点的值在这个范围内，并且其左右子树也都满足相应的取值范围条件，则为二叉搜索树。"
            }},
            {{
                "问题": "在二叉树中插入一个新节点的基本思路是什么？",
                "参考答案": "如果是普通二叉树，插入新节点比较灵活，通常可以选择将新节点插入到第一个遇到的空位置。例如，使用层序遍历，找到第一个空的子节点位置，将新节点插入进去。如果是二叉搜索树，插入新节点时，需要根据节点值的大小关系来确定插入位置。从根节点开始，如果新节点的值小于当前节点的值，则递归地在左子树中寻找插入位置；如果新节点的值大于当前节点的值，则递归地在右子树中寻找插入位置，直到找到一个空位置，将新节点插入。"
            }},
            {{
                "问题": "简述二叉树的高度是如何定义的，以及如何计算。",
                "参考答案": "二叉树的高度（也称为深度）是指从根节点到最远叶子节点的最长路径上的节点数。计算二叉树高度可以使用递归的方法。对于空树，其高度为 0；对于非空树，树的高度等于其左右子树高度的最大值加 1。即可以通过递归计算左子树高度和右子树高度，然后取较大值再加 1 得到整棵树的高度。"
            }}
        ]
    }}
    注意必须要{n}个问题。
    结果不要返回除json外其它无关内容。
    """
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {'role': 'system',
             'content': [
                 {
                     'type': 'text',
                     'text': prompt
                 }
             ]
             },
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': main_knowledge_str
                    }
                ]
            }
        ],
    )
    output = json.loads(completion.model_dump_json())["choices"][0]["message"]["content"]
    output = output.replace("```json", "").replace("```", "").strip()
    try:
        data = json.loads(output)
    except json.decoder.JSONDecodeError:
        print(f"无效的 JSON 字符串: {output}")
        return None, [], []
    subject = data["学科名称"]
    question_list = [item["问题"] for item in data["问题列表"]]
    reference_answer_list = [item["参考答案"] for item in data["问题列表"]]
    return subject, question_list, reference_answer_list


# # 设计大模型评估prompt
# evaluation_prompt_template = """
# 请根据以下信息评估学生的回答：
# ---
# **问题**：{question}
# **参考答案**：{reference_answer}
# **学生回答**：{student_answer}
# ---
# 评估要求：
# 1. 满分100分，从准确性（60%）、完整性（30%）、语言表达（10%）评分。
# 2. 指出回答中的错误或遗漏。
# 3. 用JSON格式返回结果，包含score和feedback字段。
#
# 评估结果：
# """
#
#
# # 评估函数
# def evaluate_student_answer(question, student_answer, reference_answer):
#     prompt = evaluation_prompt_template.format(
#         question=question,
#         reference_answer=reference_answer,
#         student_answer=student_answer
#     )
#     messages = [{'role': 'system', 'content': prompt}]
#     response = dashscope.Generation.call(
#         # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
#         # api_key=os.getenv('DASHSCOPE_API_KEY'),
#         api_key="sk-5fb4c90206e84a7b9d88fc91e72fbe44",
#         model="qwen-turbo",
#         # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
#         messages=messages,
#         result_format='message',
#         response_format={"type": "json_object"}
#     )
#
#     try:
#         result = json.loads(response.choices[0].message.content)
#         return result
#     except:
#         return {"error": "评估失败，请检查模型输出格式"}


class CustomWinScript(WinBotMain):
    Log_Level = "DEBUG"
    Log_Storage = True
    subject = ""
    question_list = []
    reference_answer_list = []
    student_answer_list = []

    def script_main(self):
        result = self.init_speech_service(
            "CmwzTb35WSvnOYEPoY9wC12ExtiNJkI37VJlc9itceLmM6osBYstJQQJ99BAACYeBjFXJ3w3AAAYACOG1fhO", "eastus")
        print(result)

        result = self.init_metahuman("D:/proj/humanModel2", 0.5, 0.5, False, False)
        print(result)

        result = self.show_speech_text(0, "Arial", 30, 128, 255, 0, False, False)
        print(result)

        try:
            for i in range(len(self.question_list)):
                result = self.metahuman_speech("D:/proj/voice/1.mp3",
                                               self.question_list[i], "zh-cn", "zh-cn-XiaochenNeural",
                                               0, True, 0, "General")
                print(f"问题 {i + 1}: {self.question_list[i]}")

                print("请说出您的答案...")
                while True:
                    try:
                        answer = self.microphone_to_text("zh-cn")
                        if answer and answer.strip() != "":
                            print(f"记录到的回答: {answer}")
                            self.student_answer_list.append(answer)
                            break
                        else:
                            print("未检测到回答，请重新作答...")
                            time.sleep(1)
                    except Exception as e:
                        print(f"录音出错，请重试: {str(e)}")
                        time.sleep(1)

                print(f"已记录第 {i + 1} 个问题的回答")
                time.sleep(2)

            print("所有问题已回答完毕！")
            print("答案列表：", self.student_answer_list)

            # 评估每个学生回答
            evaluation_results = []
            for i in range(len(self.question_list)):
                result = evaluate_student_answer(self.question_list[i], self.student_answer_list[i], self.reference_answer_list[i])
                evaluation_results.append(result)

            print("评估结果：")
            print(json.dumps(evaluation_results, ensure_ascii=False, indent=4))

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            self.close_driver_local()


if __name__ == "__main__":
    file_path = "探索数据结构中的二叉树.docx"
    text = read_file_content(file_path)
    if text:
        knowledges = knowledge_extract(text)
        print("抽取的知识点：")
        print(json.dumps(knowledges, ensure_ascii=False, indent=4))

        n = 5
        subject, question_list, reference_answer_list = question_ask(knowledges, n)

        print("问题及参考答案：")
        print("学科名称:", subject)
        print("问题列表:", json.dumps(question_list, ensure_ascii=False, indent=4))
        print("参考答案列表:", json.dumps(reference_answer_list, ensure_ascii=False, indent=4))

        CustomWinScript.subject = subject
        CustomWinScript.question_list = question_list
        CustomWinScript.reference_answer_list = reference_answer_list

        CustomWinScript.execute("0.0.0.0", 9999, Debug=True)
