<template>
    <v-main>
      <v-container
        fluid
        fill-height
      >
        <v-layout
          align-center
          justify-center
        >
          <v-flex
            xs12
            sm8
            md4
          >
            <v-card class="elevation-12">
              <v-toolbar
                color="deep-purple accent-4"
                dark
                flat
              >
                <v-toolbar-title>Login</v-toolbar-title>


              </v-toolbar>
              <v-card-text>
                <v-form @submit.prevent="add" >
                  <v-text-field
                    label="Username"
                    name="username"
                    prepend-icon="mdi-account"
                    type="text"
                    v-model="username"
                  ></v-text-field>

                  <v-text-field
                    v-model="password"
                    id="password"
                    label="Password"
                    name="password"
                    prepend-icon="mdi-lock"
                    type="password"
                  ></v-text-field>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn type="submit" color="deep-purple accent-4 white--text" >Login</v-btn>
              </v-card-actions>
              </v-form>
             </v-card-text>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-main>
</template>

<script>
import axios from 'axios';
export default {
    name: 'Login',
    components: {
    },
    data() {
        return {
            username: '',
            password: '',
        };
    },
    methods: {
        add() {
            this.$router.push('/home');
               
        },
    },
};
</script>
