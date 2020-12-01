<template>
  <v-container>
      <h1>Subjects</h1>
    <v-simple-table>
      <template>
        <thead>
          <tr>
            <th class="text-left">Label</th>
            <th class="text-left">Subject name</th>
            <th class="text-left"></th>
            <th class="text-left"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in subjects" :key="s.id">
            <td>{{ s.code }}</td>
            <td>{{ s.name }}</td>
            <td>
              <v-btn
                v-if="user.roles[0].name == 'PROFESSOR'"
                class="ma-2"
                outlined
                color="deep-purple accent-4"
                @click="setSubjectName(s.name)"
              >
                New test
              </v-btn>
            </td>
            <td>
              <v-btn
                v-if="user.roles[0].name == 'STUDENT'"
                class="ma-2"
                outlined
                color="deep-purple accent-4"
                @click="seeTest(s.name)"
              >
                see tests
              </v-btn>
            </td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "SubjectsList",
  data() {
    return {
      subjects: null,
      user: this.$store.state.loggedUser,
    };
  },
  methods: {
    setSubjectName(name) {
      this.$store.commit("addSubjectName", name);
      this.$router.push("/add-test");
    },
    seeTest(name) {
      this.$store.commit("addSubjectName", name);
      this.$router.push("/tests-list");
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
        this.subjects = response.data.user_subjects;
      })
      .catch((error) => {
        this.$router.push("/");
      });
  },
};
</script>

<style>
</style>