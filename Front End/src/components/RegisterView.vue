<template>
  <form name="Register-form" >
    <div class="mb-4">
      <input type="text" v-model="name"
          placeholder="Name"
          class="form-input">
    </div>
    <div class="mb-4">
      <input type="email" v-model="email" 
          placeholder="Email" 
          class="form-input">
    </div>
    <div class="mb-4">
      <input type="password" v-model="password"
          placeholder="Password" 
          class="form-input">
      </div>
      <div class="mb-6">
        <input type="password" 
          v-model="confirmPassword" 
          placeholder="Confirm Password" 
          class="form-input">
      </div>
      <button>
      Sign Up
      </button>
  </form>
</template>

<script>
export default {
name: 'RegisterView',
}
</script>