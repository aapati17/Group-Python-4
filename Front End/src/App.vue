<script>
import { ref } from 'vue'

export default {
    setup() {
        const message = ref([])

        const load = async () => {
            try {
                const response = await fetch("http://127.0.0.1:8000/", {
                    method: "GET",
                    // Change to 'cors' to allow cross-origin requests
                    mode: 'cors' 
                })


                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                message.value = await response.json()
                
            } catch (error) {
                console.error('There was a problem with your fetch operation:', error);
            }
        }

        load()

        return { message }
    }
}
</script>

<template>
  <main>
    <h1>Sample Heading Using SFC</h1>
    <h1> {{ message.message }}</h1>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
