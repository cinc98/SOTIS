<template>
<v-container>
    <h1>Tests for {{this.$store.state.subjectTest}}</h1>
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
              @click="startTest(s.name)"
            >
              Start test
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
    name: "TestsList",
    data() {
    return {
      tests: null,
      user: this.$store.state.loggedUser,
    };
  },
  methods: {
      startTest(name_test){

      }
  },
  created() {
    axios
      .get(
        `http://localhost:5000/tests-list/${this.$store.state.subjectTest}`,
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