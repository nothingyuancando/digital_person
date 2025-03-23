
// import Vue from 'vue'
// import VueRouter from 'vue-router'
import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import StudentInfo from '../views/StudentInfo.vue'
import GradeDisplay from '../views/GradeDisplay.vue'
import ConversationRecord from '../views/ConversationRecord.vue'
import AnalysisReport from '../views/AnalysisReport.vue'
import HistoryList from '../views/HistoryList.vue'
import DigitalPerson from '../views/DigitalPerson.vue'
import StudentCourseOverview from '../views/StudentCourseOverview.vue'
import TeacherCourseDetail from '../views/TeacherCourseDetail.vue'
import StudentCourseDetail from '../views/StudentCourseDetail.vue'
import TeacherCourseOverview from '../views/TeacherCourseOverview.vue'
// import HistoryDetail from '../views/HistoryDetail.vue'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/student-info',
    name: 'StudentInfo',
    component: StudentInfo
  },
  {
    path: '/studentCourseOverview',
    name: 'StudentCourseOverview',
    component: StudentCourseOverview
  },  
  {
    path: '/teacherCourseOverview',
    name: 'TeacherCourseOverview',
    component: TeacherCourseOverview
  },
  {
    path: '/studentCourseDetail',
    name: 'StudentCourseDetail',
    component: StudentCourseDetail
  },  
  {
    path: '/TeacherCourseDetail',
    name: 'TeacherCourseDetail',
    component: TeacherCourseDetail
  },  
  {
    path: '/digitalPerson',
    name: 'DigitalPerson',
    component: DigitalPerson
  },
  {
    path: '/grade',
    name: 'GradeDisplay',
    component: GradeDisplay
  },
  {
    path: '/conversation',
    name: 'ConversationRecord',
    component: ConversationRecord
  },
  {
    path: '/analysis',
    name: 'AnalysisReport',
    component: AnalysisReport
  },
  {
    path: '/history',
    name: 'HistoryList',
    component: HistoryList
  },
  // {
  //   path: '/history-detail/:id',
  //   name: 'HistoryDetail',
  //   component: HistoryDetail,
  //   props: true
  // }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
