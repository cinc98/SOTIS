<template>
  <v-container>
    <h1>Knowledge Spaces</h1>
    <v-simple-table>
      <template>
        <thead>
          <tr>
            <th class="text-left">Title</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="k in knowledgeSpaces" :key="k.id">
            <td>{{ k.title }}</td>
            <th>
              <v-btn
                class="ma-2"
                outlined
                color="deep-purple accent-4"
                @click="seeGraph(k.title)"
              >
                see graph
              </v-btn>
            </th>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
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
  name: "KnowledgeSpacesList",
  data() {
    return {
      knowledgeSpaces: null,
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
      this.nodes = [];
      this.links = [];
    },
    seeGraph(title) {
      this.$store.commit("addKsTitle", title);
      axios
        .get(`http://localhost:5000/ks/${title}`, {
          headers: {
            Authorization: sessionStorage.getItem("token"),
          },
        })
        .then((response) => {
          this.nodes = response.data.knowledge_space.problems;
          this.links = response.data.knowledge_space.links;
        })
        .catch((error) => {
          this.$router.push("/");
        });
      this.dialogToggle = !this.dialogToggle;
    },
  },
  created() {
    axios
      .get(`http://localhost:5000/kss/${this.$store.state.domainTitle}`, {
        headers: {
          Authorization: sessionStorage.getItem("token"),
        },
      })
      .then((response) => {
        this.knowledgeSpaces = response.data.knowledge_spaces;
      })
      .catch((error) => {
        this.$router.push("/");
      });
  },
};
</script>

<style>
</style>