import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import AddTest from "../components/AddTest.vue";
import SubjectsList from "../components/SubjectsList.vue";
import TestsList from "../components/TestsList.vue";
import Test from "../components/Test.vue";
import AddGraph from "../components/AddGraph.vue";
import AddSubject from "../components/AddSubject.vue"
import UsersList from "../components/UsersList.vue"
import AddDomain from "../components/AddDomain.vue"
import DomainsList from "../components/DomainsList.vue"
import KnowledgeSpacesList from "../components/KnowledgeSpacesList.vue"
import GraphView from "../components/GraphView.vue"

Vue.use(VueRouter);

const routes = [
  {
    path: "/home",
    name: "Home",
    component: Home,
    children: [
      {
        path: "/add-test",
        name: "Add test",
        component: AddTest,
      },
      {
        path: "/subjects-list",
        name: "subjectList",
        component: SubjectsList,
      },
      {
        path: "/tests-list",
        name: "TestsList",
        component: TestsList,
      },
      {
        path: "/test",
        name: "Test",
        component: Test,
      },
      {
        path: "/add-knowledge-space",
        name: "AddGraph",
        component: AddGraph,
      },
      {
        path: "/add-subject",
        name: "AddSubject",
        component: AddSubject,
      },
      {
        path: "/users",
        name: "UsersList",
        component: UsersList,
      },
      {
        path: "/add-domain",
        name: "AddDomain",
        component: AddDomain,
      },
      {
        path: "/domains",
        name: "DomainsList",
        component: DomainsList,
      },
      {
        path: "/knowledge-spaces",
        name: "KnowledgeSpacesList",
        component: KnowledgeSpacesList,
      },
      {
        path: "/knowledge-space",
        name: "GraphView",
        component: GraphView,
      },
    ],
  },
  {
    path: "/",
    name: "Login",
    component: Login,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
