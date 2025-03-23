<template>
    <div class="course-info">
      <h1 class="section-title">{{ course.name }}</h1>
      <div class="container">
        <!-- 顶部区域：左侧图片，右侧课程介绍 -->
        <div class="course-header">
          <div class="course-image-wrapper">
            <img :src="course.image" alt="course image" class="course-image" />
          </div>
          <div class="course-details">
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
      ]
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
/* 顶部课程信息区域 */
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
/* 知识图谱图片区域 */
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
/* 知识点列表区域 */
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
  margin-left: auto; /* 将按钮推到最右侧 */
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
</style>
