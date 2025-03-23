import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'  // 引入 Vuex store

// 导入 element-plus 框架
import ElementPlus from 'element-plus'
import "element-plus/theme-chalk/index.css"

createApp(App)
  .use(store)      // 注册 Vuex store
  .use(router)     // 注册路由
  .use(ElementPlus)
  .mount('#app')
