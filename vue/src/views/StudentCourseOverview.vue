<template>
    <div class="course-info">
      <h1 class="section-title">课程总览</h1>
      <div class="control-panel" >
        <div class="search-container">
          <input type="text" v-model="searchTerm" placeholder="搜索课程" class="input-field search-input" />
          <button class="btn" @click="searchCourses">搜索</button>
        </div>
      </div>
      <div class="container overview-container">
        <div
          class="course-card"
          v-for="(course, index) in courses"
          :key="index"
          @click="goToCourse(course)"
        >
          <img :src="course.image" alt="course image" class="course-image" />
          <h3 class="course-name">{{ course.name }}</h3>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        // 模拟8个课程数据
        courses: [
          {
            id: 1,
            name: "数据结构基础",
            image: require('@/assets/数据结构.jpg'),
            teacher: "张老师",
            description: "本课程介绍数据结构的基本概念、常用算法以及实际应用案例。",
            knowledgeGraph: []
          },
          {
            id: 2,
            name: "算法与数据分析",
            image: require('@/assets/数据结构.jpg'),
            teacher: "李老师",
            description: "本课程讲解常用算法、数据分析技术及实践案例。",
            knowledgeGraph: []
          },
          {
            id: 3,
            name: "计算机网络",
            image: require('@/assets/数据结构.jpg'),
            teacher: "王老师",
            description: "本课程介绍计算机网络基础、协议及网络安全。",
            knowledgeGraph: []
          },
          {
            id: 4,
            name: "操作系统原理",
            image: require('@/assets/数据结构.jpg'),
            teacher: "赵老师",
            description: "讲解操作系统的基本原理、进程管理及内存管理。",
            knowledgeGraph: []
          },
          {
            id: 5,
            name: "数据库系统",
            image: require('@/assets/数据结构.jpg'),
            teacher: "钱老师",
            description: "介绍数据库设计、SQL语句及事务管理。",
            knowledgeGraph: []
          },
          {
            id: 6,
            name: "人工智能导论",
            image: require('@/assets/数据结构.jpg'),
            teacher: "孙老师",
            description: "本课程涵盖人工智能基础、机器学习及深度学习概念。",
            knowledgeGraph: []
          },
          {
            id: 7,
            name: "前端开发实战",
            image: require('@/assets/数据结构.jpg'),
            teacher: "周老师",
            description: "介绍前端开发技术、Vue框架及项目实战。",
            knowledgeGraph: []
          },
          {
            id: 8,
            name: "软件工程与项目管理",
            image: require('@/assets/数据结构.jpg'),
            teacher: "吴老师",
            description: "讲解软件工程原理、敏捷开发及项目管理方法。",
            knowledgeGraph: []
          }
        ]
      };
    },
    methods: {
      goToCourse(course) {
        // 假设全局状态中存储了用户角色
        const role = this.$store.state.userRole; // 'teacher' 或 'student'
        if (role === "teacher") {
          this.$router.push({ name: "TeacherCourseDetail", params: { id: course.id } });
        } else {
          this.$router.push({ name: "StudentCourseDetail", params: { id: course.id } });
        }
      }
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
    /* text-align: center; */
  }
  .overview-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
  }
  .control-panel {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.search-container {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-grow: 1;
    justify-content: center;
}

.search-input {
    width: 400px;
    height: 25px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    margin-top: 16px;
    margin-left: 100px;
}

  
  .btn {
    display: inline-block;
    background: #42b983;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.3s;
    text-align: center;
    width: 120px;
  }
  
  .btn:hover { background: #3aa876; }
  .course-card {
    width: 250px;
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 10px;
    background: #f9f9f9;
    cursor: pointer;
    transition: box-shadow 0.3s ease;
    text-align: center;
  }
  .course-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  .course-image {
    width: 100%;
    height: auto;
    border-radius: 5px;
  }
  .course-name {
    margin-top: 10px;
    font-size: 18px;
    color: #2c3e50;
  }
  </style>
  