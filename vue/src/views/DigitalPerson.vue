<template>
  <div class="digital-person">
    <!-- 保留标题 -->
    <h1 class="section-title">数字人对话</h1>

    <!-- 开始对话按钮，点击后会消失 -->
    <div v-if="!isChatStarted" class="start-btn-container">
      <button class="start-btn" @click="startChat">开始对话</button>
    </div>

    <!-- 如果聊天已开始，显示聊天窗口 -->
    <div v-if="isChatStarted" class="chat-container">
      <div class="chat-layout">
        <div class="virtual-human">
          <h2 class="chat-title">数字人对话</h2>
          <div class="avatar">[数字人窗口]</div>
          <!-- 新增数字人状态信息 -->
          <div class="virtual-status">
            <span class="status-indicator"></span>
            <span class="status-text">在线</span>
          </div>
        </div>
        <div class="chat-history">
          <h3 class="history-title">对话记录</h3>
          <div class="chat-content">
            <ul>
            <li v-for="(msg, index) in chatHistory" :key="index" class="chat-message">
              <div class="message-meta">
                <span class="sender">{{ msg.sender }}</span>
                <span class="timestamp">{{ msg.time }}</span>
              </div>
              <div class="message-content">{{ msg.content }}</div>
            </li>
          </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isChatStarted: false, // 是否开始对话
      chatHistory: [],
      userMessage: "",
      questions: [
        "请简述二叉树的定义，并解释满二叉树和完全二叉树的区别。",
        "二叉树有哪几种常见的遍历方式？每种遍历方式的特点是什么？",
        "如何通过遍历结果来判断一棵二叉树是否为二叉搜索树？",
        "假设你有一棵二叉树，如何设计一个算法来计算它的高度？",
        "在实际应用中，为什么选择不同的遍历方式会影响二叉树的操作效率？请举例说明。"
      ],
      answers: [
        '嗯，二叉树是一种每个节点最多有两个子节点的树形数据结构。这两个子节点通常被称为左子节点和右子节点。',
        '嗯，二叉树的常见遍历方式有前序遍历、中序遍历、后序遍历和层次遍历等，每种遍历方式的特点不同。',
        '嗯，判断一棵二叉树是否为二叉搜索树，通常通过中序遍历来判断，如果遍历结果是严格升序的，那么它就是二叉搜索树。',
        '嗯，这道题我会，二叉树的高度可以通过递归方式来计算，遍历每个子树的最大深度。',
        '呃，不同的遍历方式会影响访问节点的顺序，从而影响算法的效率，像中序遍历常用于搜索二叉树。'
      ]
    };
  },
  methods: {
    startChat() {
      this.isChatStarted = true;
      this.initiateConversation();
    },
    initiateConversation() {
      // 先添加问题列表作为初始对话
      const now = new Date().toLocaleTimeString();
      this.questions.forEach((question, index) => {
        this.chatHistory.push({
          sender: "数字人",
          time: now,
          content: question
        });
        this.chatHistory.push({
          sender: "你",
          time: now,
          content: this.answers[index]
        });
      });
    }
  }
};
</script>

<style scoped>
.digital-person {
  max-width: 1000px;
  margin: 0 auto;
}

.section-title {
  text-align: left;
  font-size: 28px;
  margin-top: 20px;
  color: #333;
}

.start-btn-container {
  display: flex;
  justify-content: flex-start;
  margin-top: 20px;
}

.start-btn {
  padding: 12px 20px;
  background-color: #42b983;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.start-btn:hover {
  background-color: #36a372;
}

/* 聊天窗口部分 */
.chat-container {
  max-width: 1000px;
  height: 600px;
  margin: 30px auto;
  padding: 30px;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  transition: box-shadow 0.3s ease;
}

.chat-container:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.chat-layout {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.virtual-human {
  flex: 1;
  min-width: 440px;
  background-color: #f9f9f9;
  padding: 25px;
  border: 1px solid #eee;
  border-radius: 10px;
  text-align: center;
  position: relative;
  transition: background-color 0.3s ease;
  height: 550px;
}

.virtual-human:hover {
  background-color: #f0f8ff;
}

.chat-title {
  margin-bottom: 20px;
  font-size: 22px;
  color: #2c3e50;
}

.avatar {
  height: 450px;
  background-color: #e6f7ff;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  margin: 0 auto 15px auto;
  width: 100%;
  font-size: 20px;
  color: #1890ff;

}

.virtual-status {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
}

.status-indicator {
  width: 10px;
  height: 10px;
  background-color: #52c41a;
  border-radius: 50%;
  margin-right: 8px;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.3); }
  100% { transform: scale(1); }
}

.status-text {
  font-size: 14px;
  color: #2c3e50;
}

.chat-history {
  flex: 1;
  min-width: 200px;
  background-color: #f9f9f9;
  padding: 25px;
  border: 1px solid #eee;
  border-radius: 10px;
  height: 550px;
}

.chat-content {
  flex: 1;
  min-width: 200px;
  background-color: #f9f9f9;
  padding: 25px;
  border: 1px solid #eee;
  border-radius: 10px;
  max-height: 400px;
  overflow-y: auto; /* 可滚动 */
}

.history-title {
  font-size: 20px;
  margin-bottom: 20px;
  color: #2c3e50;
  text-align: left;
}

.chat-message {
  padding: 12px;
  border-bottom: 1px solid #eee;
  font-size: 15px;
  line-height: 1.6;
  color: #606c7c;
  transition: background-color 0.2s ease;
}

.chat-message:hover {
  background-color: #f5f5f5;
}

.chat-message:last-child {
  border-bottom: none;
}

.message-meta {
  font-size: 12px;
  margin-bottom: 6px;
  color: #999;
  display: flex;
  justify-content: space-between;
}

.sender {
  font-weight: bold;
  color: #2c3e50;
}

.timestamp {
  font-style: italic;
}

.message-content {
  text-align: left;
}

@media (max-width: 768px) {
  .chat-layout {
    flex-direction: column;
  }

  .virtual-human,
  .chat-history {
    min-width: 100%;
  }
}
</style>
