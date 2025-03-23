<template>
    <div class="course-info">
      <h1 class="section-title">课程总览</h1>
      <!-- 控制面板 -->
      <div class="control-panel">
        <button class="btn" @click="showModal = true">新增课程</button>
        <div class="search-container">
          <input type="text" v-model="searchTerm" placeholder="搜索课程" class="input-field search-input" />
          <button class="btn" @click="searchCourses">搜索</button>
        </div>
      </div>
  
      <div class="container overview-container">
        <div class="course-card" v-for="(course) in filteredCourses" :key="course.id">
          <img :src="course.image" alt="course image" class="course-image" />
          <h3 class="course-name">{{ course.name }}</h3>
          <div class="course-actions">
            <button class="btn" @click="goToCourse(course)">查看</button>
            <button class="btn btn-gray" @click="deleteCourse(course.id)">删除</button>
          </div>
        </div>
      </div>
  
      <!-- 模态框 -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal-content">
          <h2>新增课程</h2>
          <form @submit.prevent="addCourse">
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
              <button type="submit" class="btn">添加课程</button>
              <button type="button" class="btn btn-secondary" @click="closeModal">取消</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
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
        ],
        showModal: false,
        newCourse: { name: "", teacher: "", description: "", image: "" },
        searchTerm: ""
      };
    },
    computed: {
      filteredCourses() {
        return this.searchTerm.trim() ? this.courses.filter(course => course.name.includes(this.searchTerm)) : this.courses;
      }
    },
    methods: {
      goToCourse(course) {
        this.$router.push({ path: "/teacherCourseDetail", query: { id: course.id } });
      },
      addCourse() {
        if (!this.newCourse.name || !this.newCourse.teacher) {
          alert("课程名称和老师不能为空");
          return;
        }
        this.courses.push({
          id: this.courses.length + 1,
          name: this.newCourse.name,
          teacher: this.newCourse.teacher,
          description: this.newCourse.description,
          image: this.newCourse.image || require('@/assets/数据结构.jpg')
        });
        this.closeModal();
      },
      closeModal() {
        this.showModal = false;
        this.newCourse = { name: "", teacher: "", description: "", image: "" };
      },
      searchCourses() {
        console.log("搜索课程：", this.searchTerm);
      },
      handleFileUpload(e) {
        if (e.target.files[0]) {
          this.newCourse.image = URL.createObjectURL(e.target.files[0]);
        }
      },
      deleteCourse(courseId) {
        this.courses = this.courses.filter(course => course.id !== courseId);
      }
    }
  };
  </script>
  
  <style scoped>

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
  .overview-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
  }
  .course-info {
    max-width: 1000px;
    margin: 0 auto;
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
  
  .btn:hover {
    background: #3aa876;
  }
  .btn-gray {
    background: #ccc;
    color: #333;
  }
  .btn-gray:hover {
    background: #999;
  }
  
  .course-card {
    width: 250px;
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 10px;
    background: #f9f9f9;
    text-align: center;
    cursor: pointer;
    transition: box-shadow 0.3s;
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
  
  /* 新增：课程卡片中的操作按钮 */
  .course-actions {
    margin-top: 15px;
    display: flex;
    justify-content: space-between;
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
  
  .modal-content h2 {
    margin-top: 0;
    margin-bottom: 20px;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
    text-align: center;
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
  