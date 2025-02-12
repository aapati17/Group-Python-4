<template>
  <form name="login-form" >
    <div class="mb-3">
      <label for="username">Username: </label>
      <input id="username" type="text" />
    </div>
    <div class="mb-3">
      <label for="password">Password: </label>
      <input id="password" type="password" />
    </div>
    <button class="btn btn-outline-dark" @click.prevent="goToHomeScreen" type="submit">
      Login
    </button>
    <button class="btn btn-outline-dark" @click.prevent="goToSignUp">
      Sign Up
    </button>
  </form>
</template>

<script>
export default {
name: 'LoginView',
methods: {
    goToSignUp() {
      this.$emit('switch-to-register');
    },
    goToHomeScreen(){
      this.$emit('switch-to-HomeScreen');
    },
    submitLogin() {
      // Handle login logic here. If login is successful, emit the event.
      
    }
  }
}
</script>