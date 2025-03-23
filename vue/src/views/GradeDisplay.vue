<template>
  <div class="grade-display">
    <h1 class="section-title">等级分数</h1>
    <div class="card">
      <div v-if="loading" class="loading">
        <p>加载中...</p>
      </div>
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button class="btn" @click="fetchGradeInfo">重试</button>
      </div>
      <div v-else class="grade-content">
        <div class="grade-circle">
          <div class="score">{{ gradeInfo.score }}</div>
          <div class="level">{{ gradeInfo.level }}</div>
        </div>
        
        <div class="grade-details">
          <div class="detail-item">
            <span class="detail-label">评估日期：</span>
            <span class="detail-value">{{ gradeInfo.evaluationDate }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">对话主题：</span>
            <span class="detail-value">{{ gradeInfo.topic }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">评估人：</span>
            <span class="detail-value">{{ gradeInfo.evaluator }}</span>
          </div>
        </div>

        <div class="grade-description">
          <h3>等级说明</h3>
          <div class="grade-table">
            <div class="grade-row header">
              <div class="grade-cell">等级</div>
              <div class="grade-cell">分数范围</div>
              <div class="grade-cell">说明</div>
            </div>
            <div class="grade-row" v-for="(grade, index) in gradeStandards" :key="index">
              <div class="grade-cell">{{ grade.level }}</div>
              <div class="grade-cell">{{ grade.range }}</div>
              <div class="grade-cell">{{ grade.description }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GradeDisplay',
  data() {
    return {
      gradeInfo: {
        score: 0,
        level: '',
        evaluationDate: '',
        topic: '',
        evaluator: ''
      },
      gradeStandards: [
        { level: 'A+', range: '95-100', description: '优秀，完全掌握所学知识' },
        { level: 'A', range: '90-94', description: '优秀，掌握绝大部分知识' },
        { level: 'B+', range: '85-89', description: '良好，掌握大部分知识' },
        { level: 'B', range: '80-84', description: '良好，基本掌握知识要点' },
        { level: 'C+', range: '75-79', description: '一般，需要加强部分知识点' },
        { level: 'C', range: '70-74', description: '一般，对知识点理解有欠缺' },
        { level: 'D', range: '60-69', description: '及格，知识掌握较弱' },
        { level: 'F', range: '0-59', description: '不及格，需要重新学习' }
      ],
      loading: true,
      error: null
    }
  },
  created() {
    this.fetchGradeInfo();
  },
  methods: {
    fetchGradeInfo() {
      this.loading = true;
      this.error = null;
      
      // 这里应该调用实际的API接口获取等级分数信息
      // /api/student/grade接口
      
      // 使用接口文档中的示例数据
      setTimeout(() => {
        try {
          // 使用API响应示例中的数据
          const apiResponse = {
            "status": "success",
            "data": {
              "studentInfo": {
                "name": "张三",
                "studentId": "S1001"
              },
              "averageScore": 85,
              "grade": "B",
              "conversation": [
                {
                  "conversationId": "001",
                  "question": "二叉树的定义",
                  "studentAnswer": "...",
                  "referenceAnswer": "...",
                  "score": "80"
                },
                {
                  "conversationId": "002",
                  "question": "二叉树的遍历方式有哪些",
                  "studentAnswer": "...",
                  "referenceAnswer": "...",
                  "score": "90"
                }
              ],
              "analysisReport": "学生在对话中表现良好，但对某些算法的理解仍需加强。"
            }
          };
          
          // 提取等级分数信息
          this.gradeInfo = {
            score: apiResponse.data.averageScore,
            level: apiResponse.data.grade,
            evaluationDate: '2025-02-28', // 根据历史记录接口中的示例日期
            topic: '数据结构 - 二叉树', // 根据历史记录接口中的示例主题
            evaluator: '数字人助教'  
          };
          
          this.loading = false;
        } catch (err) {
          this.error = '获取等级分数信息失败，请重试';
          this.loading = false;
        }
      }, 1000);
    }
  }
}
</script>

<style scoped>
.grade-display {
  max-width: 1000px;
  margin: 0 auto;
}

.grade-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

.grade-circle {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  background: linear-gradient(135deg, #42b983, #2c974b);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  box-shadow: 0 4px 12px rgba(66, 185, 131, 0.3);
}

.score {
  font-size: 48px;
  font-weight: bold;
  line-height: 1;
}

.level {
  font-size: 36px;
  font-weight: bold;
  margin-top: 10px;
}

.grade-details {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.detail-item {
  display: flex;
  text-align: left;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.detail-label {
  font-weight: bold;
  width: 120px;
  color: #606c7c;
}

.detail-value {
  flex-grow: 1;
}

.grade-description {
  width: 100%;
  margin-top: 20px;
}

.grade-description h3 {
  text-align: left;
  margin-bottom: 15px;
  color: #2c3e50;
}

.grade-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.grade-row {
  display: flex;
  border-bottom: 1px solid #eee;
}

.grade-row.header {
  background-color: #f8f8f8;
  font-weight: bold;
}

.grade-cell {
  padding: 10px;
  flex: 1;
}

.grade-cell:first-child {
  flex: 0 0 60px;
}

.grade-cell:nth-child(2) {
  flex: 0 0 100px;
}

.loading, .error {
  padding: 20px;
  text-align: center;
}

.error {
  color: #f56c6c;
}
</style> 