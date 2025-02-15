<template>
  <!-- Show LoginView if showLogin is true -->
  <LoginView @switch-to-HomeScreen="showHomeScreen" v-if="showLogin && !isOutputView" @switch-to-register="showRegisterView" />

  <!-- Show RegisterView if showLogin is false and isLoggedIn is false -->
  <RegisterView v-if="!showLogin && !isLoggedIn && !isOutputView" />

  <!-- Show Homescreen once logged in -->
  <HomeScreen v-if="isLoggedIn && !isOutputView" @switch-to-OutputView="showOutputView" />

  <!-- Show OutputView when showOutputView is true -->
  <OutputView v-if="isLoggedIn && isOutputView" />
</template>

<script>
import LoginView from './components/LoginView.vue'
import RegisterView from './components/RegisterView.vue'
import HomeScreen from './components/HomeScreen.vue'
import OutputView from './components/OutputView.vue'
export default {
  name: 'App',
  components: {
    LoginView,
    RegisterView,
    HomeScreen,
    OutputView
  },
  data() {
    return {
      showLogin: true, // Controls whether to show the LoginView or RegisterView
      isLoggedIn: false,  // Tracks whether the user is logged in
      isOutputView: false // Controls whether to show OutputView
    }
  },
  methods: {
    showRegisterView() {
      this.showLogin = false;
      this.isLoggedIn = false;
      this.showOutputView = false;
    },
    // Method to handle the event when login is successful
    showHomeScreen() {
      this.isLoggedIn = true;  // Set logged-in state to true
      this.showLogin = false;  // Optionally hide the login view after login
      this.isOutputView = false; // Ensure OutputView is hidden
    },
    // Method to show OutputView
    showOutputView() {
      this.isOutputView = true;
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
