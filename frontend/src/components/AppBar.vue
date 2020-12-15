<template>
  <v-app-bar color="deep-purple accent-4" dark max-height="64px">
    <v-toolbar-title>Page title</v-toolbar-title>
    <v-btn
      v-if="user.roles[0].name == 'PROFESSOR'"
      text
      class="add-question-btn"
      @click="
        () => {
          this.$router.push('/subjects-list');
        }
      "
      >Subjects</v-btn
    >

    <v-btn
      v-if="user.roles[0].name == 'PROFESSOR'"
      text
      class="add-question-btn"
      @click="
        () => {
          this.$router.push('/domains');
        }
      "
      >domains</v-btn
    >

    <v-btn
      v-if="user.roles[0].name == 'ADMIN'"
      text
      class="add-question-btn"
      @click="
        () => {
          this.$router.push('/add-subject');
        }
      "
      >add subject</v-btn
    >

        <v-btn
      v-if="user.roles[0].name == 'ADMIN'"
      text
      class="add-question-btn"
      @click="
        () => {
          this.$router.push('/users');
        }
      "
      >users</v-btn
    >

    <v-btn
      v-if="user.roles[0].name == 'STUDENT'"
      text
      class="add-question-btn"
      @click="
        () => {
          this.$router.push('/subjects-list');
        }
      "
      >tests</v-btn
    >
    <v-spacer></v-spacer>

    <v-btn icon>
      <v-icon>mdi-heart</v-icon>
    </v-btn>

    <v-btn icon>
      <v-icon>mdi-magnify</v-icon>
    </v-btn>

    <v-menu left bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon v-bind="attrs" v-on="on">
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item
          @click="
            () => {
              removeUser();
              this.$router.push('/');
            }
          "
        >
          <v-list-item-title>Loguot</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
import axios from "axios";

export default {
  name: "AppBar",
  data() {
    return {};
  },
  methods: {
    removeUser() {
      sessionStorage.removeItem("token");
      this.$store.commit("deleteLoggedUser");
    },
  },
  computed: {
    user() {
      return this.$store.state.loggedUser;
    },
  },
  created() {
    axios
      .get("http://localhost:5000/user", {
        headers: {
          Authorization: sessionStorage.getItem("token"),
        },
      })
      .then((response) => {
        this.$store.commit("addLoggedUser", response.data.user);
      })
      .catch((error) => {
        this.$router.push("/");
      });
  },
};
</script>

<style>
.add-question-btn {
  margin: 10px;
}
</style>