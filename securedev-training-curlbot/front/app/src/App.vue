<template>
  <div id="app">
      <Navbar></Navbar>
      <div class="container">
        <div class="row">
          <router-view></router-view>
        </div>
      </div>
  </div>
</template>

<script>
import Navbar from './components/Navbar'

export default {
  watch: {
    /*'$route.path': function () {
      this.$router.push(this.$route.path)
    }*/
  },
  components: {
    Navbar
  },
  name: 'app',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<style>
@import './assets/css/bootstrap.min.css';
</style>