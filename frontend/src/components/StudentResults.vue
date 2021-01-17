<template>
    <v-container>
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
      user: this.$store.state.loggedUser,
    };
  },
  methods: {
    seeTest(name_test) {
      this.$store.commit("addTestName", name_test);
      this.$router.push("/test-review");
    },
  },
  created() {
    axios
      .get(
        `http://localhost:5000/student-tests`,
        {
          headers: {
            Authorization: sessionStorage.getItem("token"),
          },
        }
      )
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