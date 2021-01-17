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
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "TestReview",
  data() {
    return {
      test: { name: "", questions: [] },
      disableAll: false,
    };
  },
  computed: {
    getSubjectName() {
      return this.$store.state.subjectTest;
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
              `http://localhost:5000/student-answers/${this.$store.state.testName}`,
              {
                headers: {
                  Authorization: sessionStorage.getItem("token"),
                },
              }
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