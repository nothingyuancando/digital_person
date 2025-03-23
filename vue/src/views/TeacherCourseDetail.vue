<template>
  <div class="course-info">
    <h1 class="section-title">{{ course.name }}</h1>
    <div class="container">
      <!-- 课程信息展示区域 -->
      <div class="course-header">
        <div class="course-image-wrapper">
          <img :src="course.image" alt="course image" class="course-image" />
        </div>
        <div class="course-details">
          <!-- 管理课程按钮 -->
          <button class="btn manage-btn" @click="openModal">管理课程</button>
          <p class="description">{{ course.description }}</p>
          <p class="teacher-info">授课老师：{{ course.teacher }}</p>
        </div>
      </div>

      

      <!-- 知识图谱图片展示 -->
      <div class="knowledge-graph-image" v-if="knowledgeGraphImage">
        <h2 class="graph-title">知识图谱</h2>
        <img :src="knowledgeGraphImage" alt="知识图谱" class="kg-dynamic-image" />
      </div>

      <!-- 知识点列表展示 -->
      <div class="knowledge-points">
        <h3 class="list-title">知识点列表</h3>
        <ul class="kp-list">
          <li v-for="(point, index) in knowledgePoints" :key="index">
            <strong>{{ point.title }}</strong>：{{ point.content }}
            <span class="kp-actions">
              <button v-if="point.evaluated" class="btn evaluated-btn" @click="goToAnalysisReport">已评估</button>
              <button v-else class="btn evaluate-btn" @click="goToDigitalPerson">去评估</button>
            </span>
          </li>
        </ul>
      </div>

      <!-- 模态框 -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal-content">
          <h2>管理课程</h2>
          <form @submit.prevent="updateCourse">
            <div class="form-group">
              <label>课程名称：</label>
              <input type="text" v-model="newCourse.name" class="input-field" />
            </div>

            <div class="form-group">
              <label>授课老师：</label>
              <input type="text" v-model="newCourse.teacher" class="input-field" />
            </div>

            <div class="form-group">
              <label>课程简介：</label>
              <textarea v-model="newCourse.description" class="input-field textarea"></textarea>
            </div>

            <div class="form-group">
              <label>课程图片：</label>
              <input type="file" @change="handleFileUpload" class="input-field" />
            </div>

            <div class="modal-actions">
              <button type="submit" class="btn">保存更改</button>
              <button type="button" class="btn btn-secondary" @click="closeModal">取消</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      course: {},
      knowledgeGraphImage: require('@/assets/数据结构.jpg'),
      knowledgePoints: [
        {
          title: "二叉树的基本概念",
          content: "二叉树是一种树形数据结构，其特点在于每个节点最多有两个子节点。",
          evaluated: true
        },
        {
          title: "二叉树的遍历方式",
          content: "遍历二叉树有前序、中序、后序和层序等方式，不同遍历方式适用于不同场景。",
          evaluated: false
        }
      ],
      showModal: false,
      newCourse: {}
    };
  },
  methods: {
    fetchCourse() {
      this.course = {
        id: this.$route.params.id,
        name: "数据结构基础",
        teacher: "张老师",
        description: "本课程介绍数据结构的基本概念、常用算法以及实际应用案例。",
        image: require('@/assets/数据结构.jpg')
      };
    },
    openModal() {
      this.newCourse = { ...this.course }; // 复制当前课程信息
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    updateCourse() {
      this.course = { ...this.newCourse }; // 更新课程信息
      this.closeModal();
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.newCourse.image = URL.createObjectURL(file);
      }
    },
    goToAnalysisReport() {
      this.$router.push('/analysis');
    },
    goToDigitalPerson() {
      this.$router.push('/digitalPerson');
    }
  },
  created() {
    this.fetchCourse();
  }
};
</script>

<style scoped>
.course-info {
  max-width: 1000px;
  margin: 0 auto;
}
.container {
  max-width: 1000px;
  margin: 30px auto;
  padding: 30px;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
.section-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #2c3e50;
  border-bottom: 2px solid #42b983;
  padding-bottom: 10px;
}
.course-header {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}
.course-image-wrapper {
  flex: 1;
}
.course-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
}
.course-details {
  flex: 2;
}
.description,
.teacher-info {
  font-size: 16px;
  color: #606c7c;
  text-align: left;
  margin-bottom: 10px;
}
.knowledge-graph-image {
  text-align: center;
  margin-bottom: 30px;
}
.graph-title {
  font-size: 22px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 15px;
}
.kg-dynamic-image {
  max-width: 100%;
  height: auto;
  border: 1px solid #eee;
  border-radius: 8px;
}
.knowledge-points {
  margin-top: 20px;
}
.list-title {
  font-size: 20px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 10px;
}
.kp-list {
  list-style-type: none;
  padding-left: 0;
}
.kp-actions {
  margin-left: auto;
}
.kp-list li {
  font-size: 16px;
  color: #606c7c;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  text-align: left;
}
.kp-actions button {
  margin-left: 10px;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}
.btn.evaluated-btn {
  background: #42b983;
  color: #fff;
}
.btn.evaluated-btn:hover {
  background: #369c71;
}
.btn.evaluate-btn {
  background: #f39c12;
  color: #fff;
}
.btn.evaluate-btn:hover {
  background: #e67e22;
}
.manage-btn {
  display: block;
  margin-left: 0;
  margin-top: 20px;
  padding: 8px 16px;
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}
.manage-btn:hover {
  background: #3aa876; 
}


.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}
.modal-content {
  background: #fff;
  padding: 30px;
  border-radius: 10px;
  width: 500px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}
.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}
.form-group label {
  width: 100px;
  font-weight: bold;
  text-align: right;
  margin-right: 10px;
}
.input-field {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}
.textarea {
  height: 80px;
  resize: none;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
.btn-secondary {
  background: #ccc;
  color: #333;
}
.btn-secondary:hover {
  background: #999;
}
</style>
