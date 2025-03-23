<template>
  <div class="conversation-record">
    <h1 class="section-title">对话记录</h1>
    <div class="card">
      <div v-if="loading" class="loading">
        <p>加载中...</p>
      </div>
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button class="btn" @click="fetchConversation">重试</button>
      </div>
      <div v-else class="conversation-content">
        <div class="conversation-info">
          <div class="info-item">
            <span class="info-label">对话主题：</span>
            <span class="info-value">{{ conversationInfo.topic }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">对话时间：</span>
            <span class="info-value">{{ conversationInfo.time }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">对话时长：</span>
            <span class="info-value">{{ conversationInfo.duration }}</span>
          </div>
        </div>
        
        <div class="messages-container">
          <div 
            v-for="(message, index) in conversationInfo.messages" 
            :key="index" 
            :class="['message', message.sender === 'student' ? 'student-message' : 'digital-message']"
          >
            <div class="message-header">
              <span class="sender-name">{{ message.sender === 'student' ? '我' : '数字人' }}</span>
              <span class="message-time">{{ message.time }}</span>
            </div>
            <div class="message-content">
              {{ message.content }}
            </div>
            <div v-if="message.audioUrl" class="audio-control">
              <audio controls :src="message.audioUrl"></audio>
            </div>
          </div>
        </div>
        
        <div class="conversation-actions">
          <button class="btn" @click="exportConversation">导出对话记录</button>
          <button class="btn btn-secondary" @click="goToAnalysis">查看分析报告</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConversationRecord',
  data() {
    return {
      conversationInfo: {
        id: '',
        topic: '',
        time: '',
        duration: '',
        messages: []
      },
      loading: true,
      error: null
    }
  },
  created() {
    this.fetchConversation();
  },
  methods: {
    fetchConversation() {
      this.loading = true;
      this.error = null;
      
      // 这里应该调用实际的API接口获取对话记录
      // //api/history/conversation-detail接口
      
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
              "analysisReport": "学生在对话中表现良好，但对某些算法的理解仍需加强。"
            }
          };
          
          // 转换对话数据格式
          const messages = [];
          for (const entry of apiResponse.data.conversation) {
            // 添加问题（数字人）
            messages.push({
              sender: 'digital',
              content: entry.question,
              time: this.formatTime(apiResponse.data.conversationTime, messages.length),
              audioUrl: null
            });
            
            // 添加回答（学生）
            messages.push({
              sender: 'student',
              content: entry.studentAnswer,
              time: this.formatTime(apiResponse.data.conversationTime, messages.length + 1),
              audioUrl: `https://example.com/audio/student_${entry.conversationId}.mp3` // 模拟音频URL
            });
          }
          
          // 设置对话信息
          this.conversationInfo = {
            id: apiResponse.data.recordId,
            topic: `${apiResponse.data.courseName} - ${apiResponse.data.keyword}`,
            time: this.formatDate(apiResponse.data.conversationTime),
            duration: '15分钟', 
            messages: messages
          };
          
          this.loading = false;
        } catch (err) {
          this.error = '获取对话记录失败，请重试';
          this.loading = false;
        }
      }, 1000);
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', {hour: '2-digit', minute:'2-digit'});
    },
    formatTime(baseTimeString, offset) {
      const date = new Date(baseTimeString);
      date.setMinutes(date.getMinutes() + offset);
      return date.toLocaleTimeString('zh-CN', {hour: '2-digit', minute:'2-digit', second:'2-digit'});
    },
    exportConversation() {
      // 导出对话记录功能
      alert('对话记录导出功能将在这里实现');
    },
    goToAnalysis() {
      // 跳转到分析报告页面
      this.$router.push('/analysis');
    }
  }
}
</script>

<style scoped>
.conversation-record {
  max-width: 1000px;
  margin: 0 auto;
}

.conversation-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.conversation-info {
  margin-bottom: 20px;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
}

.info-item {
  display: flex;
  text-align: left;
  padding: 5px 0;
}

.info-label {
  font-weight: bold;
  width: 100px;
  color: #606c7c;
}

.info-value {
  flex-grow: 1;
}

.messages-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.message {
  max-width: 80%;
  padding: 10px 15px;
  border-radius: 10px;
  position: relative;
}

.student-message {
  align-self: flex-end;
  background-color: #e1f3d8;
  border: 1px solid #c2e7b0;
}

.digital-message {
  align-self: flex-start;
  background-color: #f2f2f2;
  border: 1px solid #e0e0e0;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 12px;
  color: #606c7c;
}

.sender-name {
  font-weight: bold;
}

.message-content {
  text-align: left;
  word-break: break-word;
}

.audio-control {
  margin-top: 10px;
}

.audio-control audio {
  width: 100%;
  height: 30px;
}

.conversation-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.loading, .error {
  padding: 20px;
  text-align: center;
}

.error {
  color: #f56c6c;
}
</style> 