<template>
  <div class="success-container">
    <img class="logo-image" src="https://framerusercontent.com/images/dEVRXt7ma4i9PhQDpqjd2e0g.png?scale-down-to=512" alt="Moradai Logo" />
    <h1 class="success-message">
      🎉 pago completado 🎉
    </h1>
    <button @click="goToHome" >volver al inicio</button>
  </div>
</template>
<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const goToHome = () => {
  router.push('/') // navigate to home
}


</script>
<style>
.success-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh; /* ocupies all the screen*/
  text-align: center;
}

.success-message {
  font-size: 3rem; /* Great text */
  font-weight: bold;
  color: #2c3e50; 
  margin-bottom: 30px;
}

.logo-image {
  max-width: 200px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
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
