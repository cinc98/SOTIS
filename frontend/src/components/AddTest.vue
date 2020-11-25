<template>
  <v-container>
    <v-card class="question-card" v-for="(obj, indx) in questions" :key="indx">
      <v-row>
        <v-col align="center">
          <h2>Question No.{{ indx + 1 }}</h2>
          <v-textarea
            class="textarea-question"
            auto-grow
            outlined
            v-model="obj.question"
            rows="1"
            row-height="15"
          ></v-textarea>
          <v-card max-width="90%">
            <v-container row v-for="(a, inde) in obj.answers" :key="inde">
              <v-textarea
                :label="'Answer No.' + (inde + 1)"
                auto-grow
                outlined
                v-model="obj.answers[inde]"
                rows="1"
                row-height="15"
              ></v-textarea>
              <v-radio-group row>
                <v-radio label="True" color="success"></v-radio>
                <v-radio label="False" color="error"></v-radio>
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
export default {
  name: "AddTest",
  data: () => ({
    success: true,
    questions: [{ question: "", answers: [] }],
  }),
  methods: {
    addQuestion() {
      this.questions.push({ question: "", answers: [] });
    },
    addAnswer(obj, answer) {
      obj.answers.push(answer);
    },
    addTest() {
      console.log(this.questions);
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
