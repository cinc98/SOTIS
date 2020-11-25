<template>
    <v-main>
        <app-bar/>
        <v-container>
          <router-view/>
        </v-container>
    </v-main>
</template>

<script>
// @ is an alias to /src
import AppBar from '../components/AppBar.vue'

export default {
  name: 'Home',
  components: {
    AppBar
  }
}
</script>
