<template>
  <v-container>
    <h1>Students</h1>
    <v-simple-table>
      <template>
        <thead>
          <tr>
            <th class="text-left">Username</th>
            <th class="text-left">Email</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in students" :key="s.id">
            <td>{{ s.email }}</td>
            <td>{{ s.username }}</td>
            <th>
              <v-btn
                class="ma-2"
                outlined
                color="deep-purple accent-4"
                @click="seeTests(s.username)"
              >
                see tests
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
  name: "StudentsList",
  data() {
    return {
      students: null,
    };
  },
  methods: {
    seeTests(studentUsername) {
      this.$store.commit("addStudent", studentUsername);
      this.$router.push("/student-results");
    },
  },
  created() {
    axios
      .get(`http://localhost:5000/students`, {
        headers: {
          Authorization: sessionStorage.getItem("token"),
        },
      })
      .then((response) => {
        this.students = response.data.students;
      })
      .catch((error) => {
        this.$router.push("/");
      });
  },
};
</script>

<style>
</style>