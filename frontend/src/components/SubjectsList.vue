<template>
  <v-container>
    <h1>Subjects</h1>
    <v-simple-table>
      <template>
        <thead>
          <tr>
            <th class="text-left">Label</th>
            <th class="text-left">Subject name</th>
            <th class="text-left" v-if="user.roles[0].name == 'PROFESSOR'">
              Domain
            </th>
            <th class="text-left"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in subjects" :key="s.id">
            <td>{{ s.code }}</td>
            <td>{{ s.name }}</td>
            <td v-if="user.roles[0].name == 'PROFESSOR'">
              {{ s.domain.title }}
            </td>
            <td>
              <v-btn
                v-if="user.roles[0].name == 'PROFESSOR'"
                class="ma-2"
                outlined
                color="deep-purple accent-4"
                @click="setSubjectName(s.name)"
                :disabled="s.domain == ''"
              >
                New test
              </v-btn>
              <v-btn
                v-if="user.roles[0].name == 'PROFESSOR' && s.domain == ''"
                class="ma-2"
                outlined
                color="deep-purple accent-4"
                @click="addDomain(s.name)"
              >
                add domain
              </v-btn>
              <v-btn
                class="ma-2"
                outlined
                color="deep-purple accent-4"
                @click="seeTest(s.name,  s.domain.title)"
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
    seeTest(name, domainTitle) {
      this.$store.commit("addSubjectName", name);
      this.$store.commit("addDomainTitle", domainTitle);

      this.$router.push("/tests-list");
    },
    addDomain(name) {
      this.$store.commit("addSubjectName", name);
      this.$router.push("/add-domain");
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