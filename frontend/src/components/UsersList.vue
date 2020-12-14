<template>
  <v-container>
    <h1>Users</h1>
    <v-simple-table>
      <template>
        <thead>
          <tr>
            <th class="text-left">Username</th>
            <th class="text-left">Email</th>
            <th class="text-left">Role</th>
            <th class="text-left">Subjects</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.username }}</td>
            <td>{{ u.email }}</td>
            <td>
              <span v-for="(role, index) in u.roles" :key="role.id">
                <template v-if="index === u.roles.length - 1">
                  {{ role.name }}
                </template>
                <template v-else> {{ role.name }}, </template>
              </span>
            </td>
            <td>
              <v-autocomplete
                class="subjects"
                v-model="u.subjects"
                :items="subjects"
                item-text="name"
                item-value="id"
                dense
                chips
                small-chips
                label="Subjects"
                multiple
                solo
              ></v-autocomplete>
            </td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
    <v-row justify="end">
      <v-btn class="primary" id="saveBtn" @click="saveUsers">
        save
      </v-btn></v-row
    >
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  name: "UserList",
  data() {
    return {
      users: null,
      subjects: null,
    };
  },
  methods: {
    saveUsers() {
      var userSubjects = [];
      for (let [index, user] of this.users.entries()) {
        userSubjects.push({
          user_id: user.id,
          subjects: user.subjects.map(function (subject) {
            if (subject.id === undefined) return { id: subject };
            else return { id: subject.id };
          }),
        });
      }
      axios
        .post(
          `http://localhost:5000/subject-to-users`,
          {
            user_subjects: userSubjects,
          },
          {
            headers: {
              Authorization: sessionStorage.getItem("token"),
            },
          }
        )
        .then((response) => {
          alert(response.data.message);
        })
        .catch((error) => {
          alert(error.response.data.message);
        });
    },
  },
  created() {
    axios
      .all([
        axios.get(`http://localhost:5000/users`, {
          headers: {
            Authorization: sessionStorage.getItem("token"),
          },
        }),
        axios.get(`http://localhost:5000/subjects`, {
          headers: {
            Authorization: sessionStorage.getItem("token"),
          },
        }),
      ])
      .then(
        axios.spread((data1, data2) => {
          this.users = data1.data.users.filter(
            (u) => u.username !== this.$store.state.loggedUser.username
          );
          this.subjects = data2.data.subjects;
        })
      );
  },
};
</script>

<style>
#saveBtn {
  margin-right: 30px;
}
.subjects{
    padding-top: 28px !important;
}
</style>