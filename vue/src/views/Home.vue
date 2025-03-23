<template>
  <div class="home">
    <div class="welcome-section">
      <h1>教育对话评估系统</h1>
      <p class="subtitle">基于人工智能的学生对话评估与分析平台</p>
    </div>
    
    <div class="features-container">
      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>学习分析</h3>
        <p>通过AI分析您的对话内容，评估您的知识掌握情况，提供详细的学习状况报告。</p>
        <router-link to="/grade" class="btn">查看我的成绩</router-link>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">💬</div>
        <h3>对话记录</h3>
        <p>查看您与数字人助教的完整对话内容，回顾学习过程，加深知识理解。</p>
        <router-link to="/conversation" class="btn">查看对话记录</router-link>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">📝</div>
        <h3>评估报告</h3>
        <p>获取详细的学习评估报告，了解自己的优势和不足，针对性地改进学习方法。</p>
        <router-link to="/analysis" class="btn">查看评估报告</router-link>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">📚</div>
        <h3>历史记录</h3>
        <p>浏览历史学习记录，追踪学习进度，见证自己的进步和成长。</p>
        <router-link to="/history" class="btn">查看历史记录</router-link>
      </div>
    </div>
    
    <div class="student-profile-summary card">
      <div class="profile-header">
        <h2>我的学习概况</h2>
        <router-link to="/student-info" class="btn-small">详细信息</router-link>
      </div>
      
      <div class="profile-content">
        <div class="profile-info">
          <div class="info-item">
            <span class="info-label">姓名：</span>
            <span class="info-value">{{ studentInfo.name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">学号：</span>
            <span class="info-value">{{ studentInfo.studentId }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">班级：</span>
            <span class="info-value">{{ studentInfo.className }}</span>
          </div>
        </div>
        
        <div class="profile-stats">
          <div class="stat-item">
            <div class="stat-value">{{ stats.totalConversations }}</div>
            <div class="stat-label">总对话次数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.highestScore }}</div>
            <div class="stat-label">最高分数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.averageScore }}</div>
            <div class="stat-label">平均分数</div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="recent-activity card">
      <div class="activity-header">
        <h2>最近活动</h2>
        <router-link to="/history" class="btn-small">查看全部</router-link>
      </div>
      
      <div class="activity-list">
        <div class="activity-item" v-for="activity in recentActivities" :key="activity.id">
          <div class="activity-date">{{ activity.date }}</div>
          <div class="activity-content">
            <div class="activity-title">{{ activity.title }}</div>
            <div class="activity-score">
              <span class="score-badge" :class="getScoreClass(activity.score)">
                {{ activity.score }}
              </span>
            </div>
          </div>
          <div class="activity-actions">
            <router-link :to="`/history-detail/${activity.id}?tab=conversation`" class="action-link">查看</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      studentInfo: {
        name: "张三",
        studentId: "S1001",
        className: "计算机科学1班"
      },
      stats: {
        totalConversations: 25,
        highestScore: 90,
        averageScore: 85
      },
      recentActivities: [
        {
          id: "rec001",
          date: "2025-02-28",
          title: "数据结构 - 二叉树基本概念",
          score: 85
        },
        {
          id: "rec002",
          date: "2025-02-27",
          title: "数据结构 - 二叉树遍历方式",
          score: 90
        },
        {
          id: "rec003",
          date: "2025-02-26",
          title: "数据结构 - 关于二叉树遍历方式的讨论",
          score: 80
        }
      ]
    }
  },
  methods: {
    getScoreClass(score) {
      if (score >= 90) return 'score-a';
      if (score >= 80) return 'score-b';
      if (score >= 70) return 'score-c';
      if (score >= 60) return 'score-d';
      return 'score-f';
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 1000px;
  margin: 0 auto;
}

.welcome-section {
  margin-bottom: 30px;
  text-align: center;
}

.welcome-section h1 {
  font-size: 32px;
  color: #2c3e50;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 18px;
  color: #606c7c;
}

.features-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.feature-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 40px;
  margin-bottom: 15px;
}

.feature-card h3 {
  margin-bottom: 10px;
  color: #2c3e50;
}

.feature-card p {
  color: #606c7c;
  margin-bottom: 20px;
  line-height: 1.5;
}

.student-profile-summary {
  margin-bottom: 30px;
}

.profile-header, .activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.profile-header h2, .activity-header h2 {
  font-size: 20px;
  color: #2c3e50;
  margin: 0;
}

.btn-small {
  padding: 5px 10px;
  font-size: 12px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  transition: background 0.3s;
}

.btn-small:hover {
  background: #3aa876;
}

.profile-content {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.profile-info {
  flex: 1;
  min-width: 250px;
}

.info-item {
  display: flex;
  text-align: left;
  padding: 8px 0;
}

.info-label {
  font-weight: bold;
  width: 80px;
  color: #606c7c;
}

.profile-stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  text-align: center;
  min-width: 80px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #42b983;
}

.stat-label {
  font-size: 12px;
  color: #606c7c;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.activity-date {
  width: 100px;
  color: #606c7c;
}

.activity-content {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.activity-title {
  font-weight: bold;
}

.score-badge {
  display: inline-block;
  min-width: 36px;
  padding: 2px 8px;
  border-radius: 12px;
  text-align: center;
  font-weight: bold;
}

.score-a {
  background-color: #e1f3d8;
  color: #52c41a;
}

.score-b {
  background-color: #e6f7ff;
  color: #1890ff;
}

.score-c {
  background-color: #fff7e6;
  color: #faad14;
}

.score-d {
  background-color: #fff1f0;
  color: #ff4d4f;
}

.score-f {
  background-color: #fff1f0;
  color: #ff4d4f;
}

.activity-actions {
  width: 80px;
  text-align: right;
}

.action-link {
  color: #42b983;
  text-decoration: none;
}

.action-link:hover {
  text-decoration: underline;
}
</style> 