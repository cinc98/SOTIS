<template>
  <v-container>
    <h1>Tests</h1>
    <v-simple-table>
      <template>
        <thead>
          <tr>
            <th class="text-left">Test name</th>
            <th class="text-left">Author</th>
            <th class="text-left"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in tests" :key="t.id">
            <td>{{ t.test_name }}</td>
            <td>{{ t.author }}</td>
            <td>
              <v-btn
                v-if="user.roles[0].name == 'STUDENT'"
                class="ma-2"
                outlined
                color="deep-purple accent-4"
                @click="seeTest(t.test_name)"
              >
                see test
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
  name: "StudentResults",
  data() {
    return {
      tests: null,
    };
  },
  methods: {
    seeTest(name_test) {
      this.$store.commit("addTestName", name_test);
      this.$router.push("/test-review");
    },
  },
  computed: {
    user() {
      if (this.$store.state.loggedUser.roles[0].name == 'STUDENT')
        return this.$store.state.loggedUser;
      else
        return this.$store.state.student
    },
  },
  created() {
    axios
      .get(`http://localhost:5000/student-tests/${this.user.username}`)
      .then((response) => {
        this.tests = response.data.tests;
      })
      .catch((error) => {
        this.$router.push("/");
      });
  },
};
</script>

<style>
</style>