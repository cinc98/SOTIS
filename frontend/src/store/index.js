import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    subjectTest: "",
    loggedUser: { roles: [{ name: "" }] },
    testName: ""
  },
  mutations: {
    addSubjectName(state, subject) {
      state.subjectTest = subject;
    },
    addLoggedUser(state, user) {
      state.loggedUser = user;
    },
    addTestName(state, name) {
      state.testName = name;
    },
    deleteLoggedUser(state){
      state.loggedUser = { roles: [{ name: "" }] };
    },
  },
  actions: {},
  modules: {},
});
