<template>
  <div class="student-info">
    <h1 class="section-title">学生基本信息</h1>
    <div class="card">
      <div v-if="loading" class="loading">
        <p>加载中...</p>
      </div>
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button class="btn" @click="fetchStudentInfo">重试</button>
      </div>
      <div v-else class="info-content">
        <div class="info-item">
          <span class="info-label">学号：</span>
          <span class="info-value">{{ studentInfo.studentId }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">姓名：</span>
          <span class="info-value">{{ studentInfo.name }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">性别：</span>
          <span class="info-value">{{ studentInfo.gender }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">年级：</span>
          <span class="info-value">{{ studentInfo.grade }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">班级：</span>
          <span class="info-value">{{ studentInfo.className }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">专业：</span>
          <span class="info-value">{{ studentInfo.major }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">学院：</span>
          <span class="info-value">{{ studentInfo.college }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentInfo',
  data() {
    return {
      studentInfo: {
        studentId: '',
        name: ''
      },
      loading: true,
      error: null
    }
  },
  created() {
    this.fetchStudentInfo();
  },
  methods: {
    fetchStudentInfo() {
      this.loading = true;
      this.error = null;
      
      // 这里应该调用实际的API接口获取学生信息
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
          
          // 只使用studentInfo部分
          this.studentInfo = apiResponse.data.studentInfo;
          
        
          this.studentInfo.gender = '男';
          this.studentInfo.grade = '2023级';
          this.studentInfo.className = '计算机科学1班';
          this.studentInfo.major = '计算机科学与技术';
          this.studentInfo.college = '信息科学与工程学院';
          
          this.loading = false;
        } catch (err) {
          this.error = '获取学生信息失败，请重试';
          this.loading = false;
        }
      }, 1000);
    }
  }
}
</script>

<style scoped>
.student-info {
  max-width: 1000px;
  margin: 0 auto;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.info-item {
  display: flex;
  text-align: left;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.info-label {
  font-weight: bold;
  width: 100px;
  color: #606c7c;
}

.info-value {
  flex-grow: 1;
}

.loading, .error {
  padding: 20px;
  text-align: center;
}

.error {
  color: #f56c6c;
}
</style> 