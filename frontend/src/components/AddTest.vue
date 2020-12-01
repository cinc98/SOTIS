<template>
  <v-container>
    <h2>{{ getSubjectName }} - Test</h2>
    <v-textarea
      label="Test name"
      auto-grow
      outlined
      v-model="testName"
      rows="1"
    ></v-textarea>
    <v-card class="question-card" v-for="(obj, indx) in questions" :key="indx">
      <v-row>
        <v-col align="center">
          <h2>Question No.{{ indx + 1 }}</h2>
          <v-textarea
            class="textarea-question"
            auto-grow
            outlined
            v-model="obj.text"
            rows="1"
            row-height="15"
          ></v-textarea>
          <v-card max-width="90%">
            <v-container row v-for="(a, inde) in obj.answers" :key="inde">
              <v-textarea
                :label="'Answer No.' + (inde + 1)"
                auto-grow
                outlined
                v-model="obj.answers[inde].text"
                rows="1"
                row-height="15"
              ></v-textarea>
              <v-radio-group v-model="obj.answers[inde].is_true" row>
                <v-radio label="False" color="error"></v-radio>
                <v-radio label="True" color="success"></v-radio>
              </v-radio-group>
            </v-container>
            <v-btn icon outlined @click="addAnswer(obj)">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-card>
        </v-col>
      </v-row>
    </v-card>
    <v-btn icon outlined @click="addQuestion()">
      <v-icon>mdi-plus</v-icon>
    </v-btn>
    <v-btn @click="addTest()"> Add Test </v-btn>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "AddTest",
  data() {
    return {
      questions: [{ text: "", answers: [{ text: "", is_true: null }] }],
      testName: "",
    };
  },
  methods: {
    addQuestion() {
      this.questions.push({
        text: "",
        answers: [{ text: "", is_true: null }],
      });
    },
    addAnswer(obj) {
      obj.answers.push({ text: "", is_true: null });
    },
    addTest() {
      axios
        .post(
          "http://localhost:5000/create-test",
          {
            author: this.$store.state.loggedUser.username,
            test_name: this.testName,
            subject_name: this.getSubjectName,
            questions: this.questions,
          },
          {
            headers: {
              Authorization: sessionStorage.getItem("token"),
            },
          }
        )
        .then((response) => {
          alert(response.data.message);
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
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.question-card {
  margin-bottom: 3%;
}

.textarea-question {
  max-width: 90%;
}
</style>
