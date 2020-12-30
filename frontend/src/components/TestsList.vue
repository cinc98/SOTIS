<template>
  <v-container>
    <h1>Tests for {{ this.$store.state.subjectTest }}</h1>
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
                @click="startTest(t.test_name)"
              >
                Start test
              </v-btn>
              <v-btn
                v-if="user.roles[0].name == 'PROFESSOR'"
                class="ma-2"
                outlined
                color="deep-purple accent-4"
                @click="createRKS(t.test_name)"
              >
                create real ks
              </v-btn>
              <v-btn
                v-if="user.roles[0].name == 'PROFESSOR'"
                class="ma-2"
                outlined
                color="deep-purple accent-4"
                @click="exportqti(t.test_name)"
              >
                export to ims qti
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
    startTest(name_test) {
      this.$store.commit("addTestName", name_test);
      this.$router.push("/test");
    },
    createRKS(name_test) {
      axios
        .get(`http://localhost:5000/get-realks/${name_test}`, {
          headers: {
            Authorization: sessionStorage.getItem("token"),
          },
        })
        .then((response) => {
          alert(response.data.message);
          this.$router.push("/knowledge-spaces");
        })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
    exportqti(name_test) {
      axios
        .post(
          `http://localhost:5000/get-xml/${name_test}`,
          {},
          {
            responseType: "arraybuffer",
            headers: { Accept: "application/octet-stream" },
          }
        )
        .then((response) => {
          let blob = new Blob([response.data], { type: "application/zip" });
          let link = document.createElement("a");
          link.href = window.URL.createObjectURL(blob);
          link.download = name_test + ".zip";

          link.click();
        })
        .catch((error) => {
          // alert(error.response.data.message);
        });
    },
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