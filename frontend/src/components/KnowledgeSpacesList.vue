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
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "KnowledgeSpacesList",
  data() {
    return {
      knowledgeSpaces: null,
    };
  },
  methods: {
    seeGraph(title) {
      this.$store.commit("addKsTitle", title);
      this.$router.push("/knowledge-space");
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