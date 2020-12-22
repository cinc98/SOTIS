<template>
  <v-container>
    <h2>{{ getSubjectName }} - Test</h2>

    <v-row>
      <v-col>
        <v-autocomplete
          v-model="selectedKS"
          :items="knowledgeSpaces"
          @change="getKS"
          item-text="title"
          item-value="id"
          dense
          chips
          small-chips
          label="Knowledge Space"
          solo
        ></v-autocomplete>
      </v-col>
      <v-col>
        <v-btn
          class="ma-2"
          id="seeGraph"
          outlined
          color="deep-purple accent-4"
          @click="seeGraph()"
          :disabled="selectedKS === null"
        >
          see graph
        </v-btn></v-col
      >
    </v-row>

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
            label="Question text"
            outlined
            v-model="obj.text"
            rows="1"
            row-height="15"
          ></v-textarea>
          <v-autocomplete
            class="textarea-question"
            v-model="obj.problem"
            :items="nodes"
            item-text="name"
            item-value="id"
            dense
            chips
            small-chips
            label="Problem"
            solo
          ></v-autocomplete>
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
            <v-btn id="btnAddAnswer" icon outlined @click="addAnswer(obj)">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-card>
        </v-col>
      </v-row>
    </v-card>
    <v-row>
      <v-col align="center">
        <v-btn icon outlined @click="addQuestion()">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-btn class="primary" @click="addTest()" :disabled="selectedKS === null">
        Add Test
      </v-btn>
    </v-row>

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
  name: "AddTest",
  data() {
    return {
      questions: [
        { text: "", problem: "", answers: [{ text: "", is_true: null }] },
      ],
      testName: "",
      knowledgeSpaces: [],
      selectedKS: null,
      dialogToggle: false,
      nodes: [],
      links: [],
    };
  },
  components: {
    GraphView,
  },
  watch: {
    getProblems(newValue, oldValue) {
      for (let v of newValue.entries()) {
        if (v[1] !== "") {
          this.nodes.find((n) => n.id === v[1]).disabled = true;
        }
        if (oldValue.length === newValue.length) {
          if (newValue[v[0]] !== oldValue[v[0]] && oldValue[v[0]] !== "") {
            this.nodes.find((n) => n.id === oldValue[v[0]]).disabled = false;
          }
        }
      }
    },
  },
  methods: {
    toggleDialogClick() {
      this.dialogToggle = !this.dialogToggle;
    },
    addQuestion() {
      this.questions.push({
        text: "",
        problem: "",
        answers: [{ text: "", is_true: null }],
      });
    },
    addAnswer(obj) {
      obj.answers.push({ text: "", is_true: null });
    },
    getKS(value) {
      axios
        .get(`http://localhost:5000/ks-id/${value}`, {
          headers: {
            Authorization: sessionStorage.getItem("token"),
          },
        })
        .then((response) => {
          this.nodes = response.data.knowledge_space.problems;
          this.links = response.data.knowledge_space.links;
          this.$store.commit("addKsTitle", response.data.knowledge_space.title);
        })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    seeGraph() {
      this.dialogToggle = !this.dialogToggle;
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
  created() {
    axios
      .get(`http://localhost:5000/ks-subject/${this.getSubjectName}`, {
        headers: {
          Authorization: sessionStorage.getItem("token"),
        },
      })
      .then((response) => {
        this.knowledgeSpaces = response.data.knowledge_spaces;
      })
      .catch((error) => {
        alert(error.response.data.message);
      });
  },
  computed: {
    getSubjectName() {
      return this.$store.state.subjectTest;
    },
    getProblems() {
      return this.questions.map((question) => question.problem);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.question-card {
  margin-bottom: 3%;
}
#seeGraph {
  margin-top: 1px !important;
}
.textarea-question {
  max-width: 90%;
}
#btnAddAnswer {
  margin-bottom: 10px;
}
</style>
