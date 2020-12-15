<template>
  <v-container>
    <h1>Domains</h1>
    <v-simple-table>
      <template>
        <thead>
          <tr>
            <th class="text-left">Domain title</th>
            <th class="text-left">Domain description</th>
            <th class="text-left">Subject</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in domains" :key="d.id">
            <td>{{ d.domain.title }}</td>
            <td>{{ d.domain.description }}</td>
            <td>{{ d.name }}</td>
            <th>
              <v-btn
                class="ma-2"
                outlined
                color="deep-purple accent-4"
                @click="addKnowledgespace(d.domain.title)"
              >
                add knowledge space
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
  name: "DomainsList",
  data() {
    return {
      domains: null,
    };
  },
  methods: {
    addKnowledgespace(domainTitle) {
      this.$store.commit("addDomainTitle", domainTitle);
      this.$router.push("/knowledge-space");
    },
  },
  created() {
    axios
      .get(
        `http://localhost:5000/subjects/${this.$store.state.loggedUser.username}`,
        {
          headers: {
            Authorization: sessionStorage.getItem("token"),
          },
        }
      )
      .then((response) => {
        this.domains = response.data.user_subjects.filter(
          (d) => d.domain !== ""
        );
      })
      .catch((error) => {
        this.$router.push("/");
      });
  },
};
</script>

<style>
</style>