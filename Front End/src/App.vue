<template>
  <!-- Show LoginView if showLogin is true -->
  <!--<LoginView v-if="showLogin" @switch-to-register="showRegisterView" /> -->
  <LoginView @switch-to-HomeScreen="showHomeScreen" v-if="showLogin" @switch-to-register="showRegisterView" />

  <!-- Show RegisterView if showLogin is false and isLoggedIn is false -->
  <RegisterView v-if="!showLogin && !isLoggedIn" />

  <!-- Show Homescreen once logged in -->
  <HomeScreen v-if="isLoggedIn" />
</template>

<script>
import LoginView from './components/LoginView.vue'
import RegisterView from './components/RegisterView.vue'
import HomeScreen from './components/HomeScreen.vue'
export default {
  name: 'App',
  components: {
    LoginView,
    RegisterView,
    HomeScreen
  },
  data() {
    return {
      showLogin: true, // Controls whether to show the LoginView or RegisterView
      isLoggedIn: false  // Tracks whether the user is logged in
    }
  },
  methods: {
    showRegisterView() {
      this.showLogin = false;
    },
    // Method to handle the event when login is successful
    showHomeScreen() {
      this.isLoggedIn = true;  // Set logged-in state to true
      this.showLogin = false;  // Optionally hide the login view after login
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
