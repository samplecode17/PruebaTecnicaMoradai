<template>
  <div class="success-container">
    <img class="logo-image" src="https://framerusercontent.com/images/dEVRXt7ma4i9PhQDpqjd2e0g.png?scale-down-to=512" alt="Moradai Logo" />
    <h1 class="success-message">
      Bienvenidos a la prueba técnica de Moradai!
    </h1>
    <button @click="goToHome">empezar</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

// initialize the router
const router = useRouter()

// function to navigate to home
const goToHome = () => {
  router.push('/product') // navigate to home
}
</script>

<style>
.success-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh; /* occupy all the screen */
  text-align: center;
}

.logo-image {
  max-width: 200px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.success-message {
  font-size: 2.5rem; /* great text */
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 30px;
}

button {
  padding: 12px 30px;
  font-size: 1.2rem;
  font-weight: bold;
  color: white;
  background-color: #064581;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #006afdff;
}
</style>
