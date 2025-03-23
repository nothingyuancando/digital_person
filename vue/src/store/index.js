// store/index.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    // 这里初始化你的用户角色，示例中设为 'student'
    userRole: 'student'
  },
  mutations: {
    setUserRole(state, role) {
      state.userRole = role;
    }
  },
  actions: {
    updateUserRole({ commit }, role) {
      commit('setUserRole', role);
    }
  },
  modules: {
    // 如果有其他模块可以在这里引入
  }
});
