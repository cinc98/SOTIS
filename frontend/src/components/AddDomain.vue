<template>
  <v-container>
    <h2>Add Domain</h2>
    <form @submit.prevent="submit">
      <v-text-field
        v-model="domainTitle"
        label="Domain title"
        required
      ></v-text-field>

      <v-text-field
        v-model="domainDescription"
        label="Domain description"
        required
      ></v-text-field>

      <v-btn color="primary" @click="submit"> submit </v-btn>
    </form>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "AddDomain",
  data() {
    return {
      domainTitle: "",
      domainDescription: "",
    };
  },
  methods: {
    submit() {
      axios
        .post(
          `http://localhost:5000/add-domain`,
          {
            domain_title: this.domainTitle,
            domain_description: this.domainDescription,
            subject_id: this.$store.state.subjectTest,
          },
          {
            headers: {
              Authorization: sessionStorage.getItem("token"),
            },
          }
        )
        .then((response) => {
          alert(response.data.message);
          this.domainTitle = "";
          this.domainDescription = "";
        })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
  },
};
</script>

<style>
</style>