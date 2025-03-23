<template>
  <div class="analysis-report">
    <h1 class="section-title">分析报告</h1>
    <div class="card">
      <div v-if="loading" class="loading">
        <p>加载中...</p>
      </div>
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button class="btn" @click="fetchAnalysisReport">重试</button>
      </div>
      <div v-else class="report-content">
        <div class="report-header">
          <div class="topic">{{ report.topic }}</div>
          <div class="date">评估日期：{{ report.date }}</div>
        </div>
        
        <div class="report-summary">
          <h3>总体评价</h3>
          <div class="summary-content">{{ report.summary }}</div>
          
          <div class="score-overview">
            <div class="score-item">
              <div class="score-label">总分</div>
              <div class="score-value">{{ report.totalScore }}</div>
            </div>
            <div class="score-item" v-for="(score, index) in report.categoryScores" :key="index">
              <div class="score-label">{{ score.category }}</div>
              <div class="score-value">{{ score.score }}</div>
            </div>
          </div>
        </div>
        
        <div class="knowledge-points">
          <h3>知识点掌握情况</h3>
          <div class="knowledge-grid">
            <div class="knowledge-item" v-for="(point, index) in report.knowledgePoints" :key="index">
              <div class="knowledge-name">{{ point.name }}</div>
              <div class="knowledge-level" :class="'level-' + getLevelClass(point.masteryLevel)">
                {{ point.masteryLevel }}
              </div>
              <div class="knowledge-comment">{{ point.comment }}</div>
            </div>
          </div>
        </div>
        
        <div class="strengths-weaknesses">
          <div class="strengths">
            <h3>优点</h3>
            <ul>
              <li v-for="(strength, index) in report.strengths" :key="index">
                {{ strength }}
              </li>
            </ul>
          </div>
          
          <div class="weaknesses">
            <h3>需要改进的地方</h3>
            <ul>
              <li v-for="(weakness, index) in report.weaknesses" :key="index">
                {{ weakness }}
              </li>
            </ul>
          </div>
        </div>
        
        <div class="language-analysis">
          <h3>语言表达能力分析</h3>
          <div class="language-metrics">
            <div class="metric" v-for="(metric, index) in report.languageMetrics" :key="index">
              <div class="metric-name">{{ metric.name }}</div>
              <div class="metric-progress">
                <div class="progress-bar">
                  <div 
                    class="progress-bar-fill"
                    :style="{ width: metric.value + '%' }"
                    :class="'level-' + getProgressClass(metric.value)"
                  ></div>
                </div>
                <div class="metric-value">{{ metric.value }}%</div>
              </div>
              <div class="metric-comment">{{ metric.comment }}</div>
            </div>
          </div>
        </div>
        
        <div class="suggestions">
          <h3>改进建议</h3>
          <div class="suggestion-items">
            <div class="suggestion" v-for="(suggestion, index) in report.suggestions" :key="index">
              <div class="suggestion-icon">💡</div>
              <div class="suggestion-content">{{ suggestion }}</div>
            </div>
          </div>
        </div>
        
        <div class="next-steps">
          <h3>下一步学习计划</h3>
          <div class="next-steps-content">
            <p>{{ report.nextSteps }}</p>
          </div>
        </div>
        
        <div class="report-actions">
          <button class="btn" @click="exportReport">导出报告</button>
          <button class="btn btn-secondary" @click="goToConversation">查看对话记录</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AnalysisReport',
  data() {
    return {
      report: {
        topic: '',
        date: '',
        summary: '',
        totalScore: 0,
        categoryScores: [],
        knowledgePoints: [],
        strengths: [],
        weaknesses: [],
        languageMetrics: [],
        suggestions: [],
        nextSteps: ''
      },
      loading: true,
      error: null
    }
  },
  created() {
    this.fetchAnalysisReport();
  },
  methods: {
    fetchAnalysisReport() {
      this.loading = true;
      this.error = null;
      
      // 这里应该调用实际的API接口获取分析报告
      // /api/student/grade接口
      
      // 使用接口文档中的示例数据
      setTimeout(() => {
        try {
          // 使用API响应示例中的数据
          const apiResponse = {
            "status": "success",
            "data": {
              "recordId": "rec001",
              "conversationTime": "2025-02-28T14:00:00Z",
              "courseName": "数据结构",
              "keyword": "二叉树的概念",
              "averageScore": "85",
              "grade": "B",
              "conversation": [
                {
                  "conversationId": "001",
                  "question": "二叉树的定义",
                  "studentAnswer": "二叉树是每个节点最多有两个子树的树结构。通常子树被称作左子树和右子树。二叉树常被用于实现二叉搜索树和二叉堆。",
                  "referenceAnswer": "二叉树是一种树形数据结构，其中每个节点最多有两个子节点，通常被称为左子节点和右子节点。二叉树广泛应用于计算机科学的各个领域，尤其在数据存储、搜索和排序算法中。",
                  "score": "80"
                },
                {
                  "conversationId": "002",
                  "question": "二叉树的遍历方式有哪些",
                  "studentAnswer": "二叉树的遍历方式主要有前序遍历、中序遍历和后序遍历。前序是根左右，中序是左根右，后序是左右根。还有层次遍历是按层从左到右遍历。",
                  "referenceAnswer": "二叉树的遍历方式主要有四种：1. 前序遍历（根-左-右）；2. 中序遍历（左-根-右）；3. 后序遍历（左-右-根）；4. 层序遍历（逐层从左到右）。这些遍历方式可以用递归或迭代的方式实现。",
                  "score": "90"
                }
              ],
              "analysisReport": "学生在对话中表现良好，但对某些算法的理解仍需加强。对二叉树的基本概念掌握较好，能够准确描述不同的遍历方法，但在描述二叉树定义时不够全面和精确。建议学生继续加强对数据结构基础概念的学习，尤其是二叉树的应用场景和高级操作。"
            }
          };
          
         
          this.report = {
            topic: `${apiResponse.data.courseName} - ${apiResponse.data.keyword}`,
            date: this.formatDate(apiResponse.data.conversationTime),
            summary: apiResponse.data.analysisReport,
            totalScore: parseFloat(apiResponse.data.averageScore),
            
            
            categoryScores: [
              { category: '概念理解', score: 80 },
              { category: '算法掌握', score: 90 },
              { category: '逻辑表达', score: 85 },
              { category: '准确性', score: 85 }
            ],
            knowledgePoints: [
              { name: '二叉树定义', masteryLevel: '良好', comment: '基本掌握二叉树的定义，但不够全面' },
              { name: '二叉树遍历', masteryLevel: '优秀', comment: '熟练掌握各种遍历方式及其实现' }
            ],
            strengths: [
              '对二叉树的基本概念有清晰的理解',
              '能够准确描述不同的遍历方法',
              '回答简洁明了'
            ],
            weaknesses: [
              '在描述二叉树定义时不够全面和精确',
              '未提及二叉树在实际应用中的场景',
              '对复杂概念的阐述深度不够'
            ],
            languageMetrics: [
              { name: '术语准确性', value: 85, comment: '大部分术语使用准确' },
              { name: '表达流畅性', value: 88, comment: '表达流畅，思路清晰' },
              { name: '逻辑性', value: 90, comment: '逻辑结构良好' },
              { name: '完整性', value: 82, comment: '回答基本完整，但细节可补充' }
            ],
            suggestions: [
              '加强对二叉树基本概念的理解，确保描述更加全面和精确',
              '学习二叉树的更多应用场景，如二叉搜索树、堆等',
              '练习二叉树的相关算法题，提高实际应用能力',
              '尝试实现不同的二叉树遍历方法，包括递归和非递归方式'
            ],
            nextSteps: '建议继续学习二叉树的高级应用，如平衡二叉树、红黑树等，并尝试解决一些经典的二叉树算法问题，提高实际编程能力。'
          };
          
          this.loading = false;
        } catch (err) {
          this.error = '获取分析报告失败，请重试';
          this.loading = false;
        }
      }, 1000);
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN');
    },
    getLevelClass(level) {
      const levelMap = {
        '优秀': 'excellent',
        '良好': 'good',
        '一般': 'average',
        '欠缺': 'poor'
      };
      return levelMap[level] || 'average';
    },
    getProgressClass(value) {
      if (value >= 90) return 'excellent';
      if (value >= 80) return 'good';
      if (value >= 70) return 'average';
      return 'poor';
    },
    exportReport() {
      // 导出报告功能
      alert('导出报告功能将在这里实现');
    },
    goToConversation() {
      // 跳转到对话记录页面
      this.$router.push('/conversation');
    }
  }
}
</script>

<style scoped>
.analysis-report {
  max-width: 1000px;
  margin: 0 auto;
}

.report-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.report-header {
  text-align: center;
  margin-bottom: 20px;
}

.topic {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}

.date {
  color: #606c7c;
  font-size: 14px;
}

.report-summary, .knowledge-points, .strengths-weaknesses,
.language-analysis, .suggestions, .next-steps {
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.report-summary h3, .knowledge-points h3, .strengths-weaknesses h3,
.language-analysis h3, .suggestions h3, .next-steps h3 {
  text-align: left;
  margin-bottom: 15px;
  color: #2c3e50;
}

.summary-content {
  text-align: left;
  line-height: 1.6;
}

.score-overview {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  flex-wrap: wrap;
}

.score-item {
  text-align: center;
  margin: 10px;
}

.score-label {
  color: #606c7c;
  font-size: 14px;
  margin-bottom: 5px;
}

.score-value {
  font-size: 24px;
  font-weight: bold;
  color: #42b983;
}

.knowledge-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.knowledge-item {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  text-align: left;
}

.knowledge-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.knowledge-level {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 10px;
}

.level-excellent {
  background-color: #e1f3d8;
  color: #52c41a;
}

.level-good {
  background-color: #e6f7ff;
  color: #1890ff;
}

.level-average {
  background-color: #fff7e6;
  color: #fa8c16;
}

.level-poor {
  background-color: #fff1f0;
  color: #f5222d;
}

.knowledge-comment {
  font-size: 14px;
  color: #606c7c;
}

.strengths-weaknesses {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.strengths, .weaknesses {
  flex: 1;
  min-width: 300px;
}

.strengths ul, .weaknesses ul {
  text-align: left;
  padding-left: 20px;
}

.strengths li, .weaknesses li {
  margin-bottom: 10px;
  line-height: 1.4;
}

.language-metrics {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.metric {
  text-align: left;
}

.metric-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.metric-progress {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.progress-bar {
  flex-grow: 1;
  height: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 5px;
}

.metric-value {
  font-weight: bold;
  min-width: 40px;
}

.metric-comment {
  font-size: 14px;
  color: #606c7c;
}

.suggestion-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.suggestion {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  text-align: left;
}

.suggestion-icon {
  font-size: 20px;
}

.suggestion-content {
  flex-grow: 1;
  line-height: 1.4;
}

.next-steps-content {
  text-align: left;
  line-height: 1.6;
}

.report-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.loading, .error {
  padding: 20px;
  text-align: center;
}

.error {
  color: #f56c6c;
}
</style> 