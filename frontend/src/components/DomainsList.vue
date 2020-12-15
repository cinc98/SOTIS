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
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in domains" :key="d.id">
            <td>{{ d.domain.title }}</td>
            <td>{{ d.domain.description }}</td>
            <td>{{ d.name }}</td>
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
  methods: {},
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
        this.domains = response.data.user_subjects;
      })
      .catch((error) => {
        this.$router.push("/");
      });
  },
};
</script>

<style>
</style>