import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    subjectTest: "",
    loggedUser: { roles: [{ name: "" }] },
  },
  mutations: {
    addSubjectName(state, subject) {
      state.subjectTest = subject;
    },
    addLoggedUser(state, user) {
      state.loggedUser = user;
    },
    deleteLoggedUser(state){
      state.loggedUser = { roles: [{ name: "" }] };
    },
    deleteSubjectName(state) {
      state.subjectTest = "";
    },
  },
  actions: {},
  modules: {},
});
