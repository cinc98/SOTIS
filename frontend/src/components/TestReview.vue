<template>
  <v-container>
    <h2>{{ test.name }}</h2>
    <v-card
      class="question-card"
      v-for="(obj, indx) in test.questions"
      :key="indx"
    >
      <v-row>
        <v-col align="center">
          <h4>Question No.{{ indx + 1 }} (1b)</h4>
          <h3>{{ obj.text }}</h3>
          <v-card max-width="90%">
            <v-container
              align="center"
              row
              v-for="(a, inde) in obj.answers"
              :key="inde"
            >
              <v-checkbox
                v-model="obj.answers[inde].is_true"
                :label="obj.answers[inde].text"
                :disabled="disableAll"
                :class="
                  obj.answers[inde].correct_answer === undefined
                    ? ''
                    : obj.answers[inde].correct_answer
                    ? 'green'
                    : 'red'
                "
              ></v-checkbox>
            </v-container>
          </v-card>
        </v-col>
      </v-row>
    </v-card>
    <v-btn class="primary" @click="seeState(test.name)">State</v-btn>
    <graph-view
      v-bind:dialogToggle="this.toggleDialogClick"
      v-bind:show="this.dialogToggle"
      v-bind:nodes="this.nodes"
      v-bind:links="this.links"
    />
  </v-container>
</template>

<script>
import axios from "axios";
import GraphView from "./GraphView.vue";

export default {
  name: "TestReview",
  data() {
    return {
      test: { name: "", questions: [] },
      disableAll: false,
      dialogToggle: false,
      nodes: [],
      links: [],
    };
  },
  components: {
    GraphView,
  },
  methods: {
    toggleDialogClick() {
      this.dialogToggle = !this.dialogToggle;
    },
    seeState(testName) {
      axios
        .get(
          `http://localhost:5000/all-states/${this.user.username}/${testName}`,
          {
            headers: {
              Authorization: sessionStorage.getItem("token"),
            },
          }
        )
        .then((response) => {
          this.nodes = response.data.knowledge_space.problems;
          this.links = response.data.knowledge_space.links;
          this.$store.commit("addKsTitle", response.data.knowledge_space.title);
          this.dialogToggle = !this.dialogToggle;
          for (let [i, n] of this.nodes.entries()) {
            if(n.id === parseInt(response.data.state.state, 2)){
              this.nodes[i]._color="green"
            }
          }
        })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
  },
  computed: {
    getSubjectName() {
      return this.$store.state.subjectTest;
    },
    user() {
      if (this.$store.state.loggedUser.roles[0].name == "STUDENT")
        return this.$store.state.loggedUser;
      else return this.$store.state.student;
    },
  },
  created() {
    this.disableAll = true;

    axios
      .get(`http://localhost:5000/test/${this.$store.state.testName}`, {
        headers: {
          Authorization: sessionStorage.getItem("token"),
        },
      })
      .then((response) => {
        this.test = response.data.test;
        this.test.questions = this.test.questions.sort(
          (first, second) =>
            parseInt(first.problem.weight) - parseInt(second.problem.weight)
        );

        axios
          .all([
            axios.get(
              `http://localhost:5000/test-solution/${this.$store.state.testName}`,
              {
                headers: {
                  Authorization: sessionStorage.getItem("token"),
                },
              }
            ),
            axios.get(
              `http://localhost:5000/student-answers/${this.user.username}/${this.$store.state.testName}`
            ),
          ])
          .then(
            axios.spread((data1, data2) => {
              let sortedQuestion = data1.data.test.questions.sort(
                (first, second) =>
                  parseInt(first.problem.weight) -
                  parseInt(second.problem.weight)
              );
              for (let [i, q] of sortedQuestion.entries()) {
                for (let [inde, a] of q.answers.entries()) {
                  this.test.questions[i].answers[inde].correct_answer =
                    a.is_true;
                  this.test.questions[i].answers[inde].is_true =
                    data2.data.answers[a.id];
                  let test1 = this.test;
                  this.test = null;
                  this.test = test1;
                }
              }
            })
          );
      })
      .catch((error) => {
        alert(error);
      });
  },
};
</script>

<style>
</style>