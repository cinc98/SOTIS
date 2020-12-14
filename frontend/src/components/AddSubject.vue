<template>
  <v-container>
    <h2>Add Subject</h2>
    <form @submit.prevent="submit">
      <v-text-field
        v-model="subjectCode"
        label="Subject code"
        required
      ></v-text-field>

      <v-text-field
        v-model="subjectName"
        label="Subject name"
        required
      ></v-text-field>

      <v-btn color="primary" @click="submit"> submit </v-btn>
    </form>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "addSubject",
  data() {
    return {
      subjectCode: "",
      subjectName: "",
    };
  },
  methods: {
    submit() {
      axios
        .post(
          `http://localhost:5000/add-subject`,
          {
            subject_name: this.subjectName,
            subject_code: this.subjectCode,
          },
          {
            headers: {
              Authorization: sessionStorage.getItem("token"),
            },
          }
        )
        .then((response) => {
          alert(response.data.message);
          this.subjectCode = "";
          this.subjectName = "";
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