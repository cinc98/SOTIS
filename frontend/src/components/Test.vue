<template>
  <v-container>
    <h1>{{ getSubjectName }} - Test</h1>
    <h2>{{ test.name }}</h2>
    <v-card
      class="question-card"
      v-for="(obj, indx) in test.questions"
      :key="indx"
    >
      <v-row>
        <v-col align="center">
          <h4>Question No.{{ indx + 1 }}</h4>
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
    <v-btn @click="finishTest" :disabled="disableAll"> finish Test </v-btn>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Test",
  data() {
    return {
      test: { name: "", questions: [] },
      disableAll: false,
    };
  },
  methods: {
    finishTest() {
      this.disableAll = true;
      let answers = [];
      for (let [index, question] of this.test.questions.entries()) {
        for (let [ind, answer] of question.answers.entries()) {
          this.test.questions[index].answers[ind].is_true =
            answer.is_true === undefined ? false : answer.is_true;
          answers.push({
            answer_id: answer.id,
            is_true: answer.is_true === undefined ? false : answer.is_true,
          });
        }
      }
      axios
        .post(
          "http://localhost:5000/finish-test",
          {
            student_id: this.$store.state.loggedUser.id,
            answers: answers,
          },
          {
            headers: {
              Authorization: sessionStorage.getItem("token"),
            },
          }
        )
        .then((response) => {
          alert(response.data.message);

          axios
            .get(
              `http://localhost:5000/test-solution/${this.$store.state.testName}`,
              {
                headers: {
                  Authorization: sessionStorage.getItem("token"),
                },
              }
            )
            .then((response) => {
              for (let [i, q] of response.data.test.questions.entries()) {
                for (let [inde, a] of q.answers.entries()) {
               
                  this.test.questions[i].answers[inde].correct_answer =
                    a.is_true;
                  let test1 = this.test
                  this.test = null
                  this.test = test1
                }
              }
            })
            .catch((error) => {
              alert(error);
            });
        })
        .catch((error) => {
          alert(error);
        });
    },
  },
  computed: {
    getSubjectName() {
      return this.$store.state.subjectTest;
    },
  },
  created() {
    axios
      .get(`http://localhost:5000/test/${this.$store.state.testName}`, {
        headers: {
          Authorization: sessionStorage.getItem("token"),
        },
      })
      .then((response) => {
        this.test = response.data.test;
      })
      .catch((error) => {
        alert(error);
      });
  },
};
</script>

<style>
</style>