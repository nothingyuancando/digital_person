<template>
  <div id="app">
    <nav>
      <router-link to="/login">登录</router-link>
      <router-link to="/">首页</router-link>
      <router-link to="/student-info">学生信息</router-link>
      <router-link to="/teacherCourseOverview">教师端课程总览</router-link>
      <router-link to="/studentcourseOverview">学生端课程总览</router-link>
      <router-link to="/teacherCourseDetail">教师端课程信息</router-link>
      <router-link to="/studentCourseDetail">学生端课程信息</router-link>
      <router-link to="/digitalPerson">数字人对话</router-link>
      <router-link to="/grade">等级分数</router-link>
      <router-link to="/conversation">对话记录</router-link>
      <router-link to="/analysis">分析报告</router-link>
      <router-link to="/history">历史记录</router-link>
    </nav>
    <div class="container">
      <router-view/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background-color: #f5f7fa;
}

body {
  margin: 0;
  padding: 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
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
  text-decoration: none;
}

.btn:hover {
  background: #3aa876;
}

.btn-secondary {
  background: #606c7c;
}

.btn-secondary:hover {
  background: #4e5a69;
}

.section-title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: left;
  border-bottom: 2px solid #42b983;
  padding-bottom: 10px;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  margin-bottom: 15px;
}

.text-center {
  text-align: center;
}

.text-left {
  text-align: left;
}

.mt-20 {
  margin-top: 20px;
}

.mb-20 {
  margin-bottom: 20px;
}

nav {
  padding: 15px 0;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  margin: 0 10px;
  text-decoration: none;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>