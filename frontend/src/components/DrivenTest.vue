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
          <h4>Question No.{{ questionNum }}</h4>
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
              ></v-checkbox>
            </v-container>
          </v-card>
        </v-col>
      </v-row>
    </v-card>
    <v-btn @click="nextQuestion"> Next question </v-btn>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "DrivenTest",
  data() {
    return {
      test: { name: "", questions: [] },
      disableAll: false,
      questionNum: 1,
      probabilities: null,
      asked_questions: null,
    };
  },
  methods: {
    nextQuestion() {
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
          axios
            .post(`http://localhost:5000/test/next-question`, {
              test: this.test,
              probabilities: this.probabilities,
              asked_questions: this.asked_questions,
            })
            .then((response) => {
              if (response.data.test !== undefined) {
                this.test = response.data.test;
                this.probabilities = response.data.probabilities;
                this.asked_questions = response.data.asked_questions;

              }else{
                alert("gotov test")
                console.log(response.data.probabilities);
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
      .get(
        `http://localhost:5000/test/first-question/${this.$store.state.testName}`,
        {
          headers: {
            Authorization: sessionStorage.getItem("token"),
          },
        }
      )
      .then((response) => {
        this.test = response.data.test;
        this.probabilities = response.data.probabilities;
        this.asked_questions = response.data.asked_questions;

      })
      .catch((error) => {
        alert(error);
      });
  },
};
</script>

<style>
</style>