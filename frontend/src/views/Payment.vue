<template>
  <!-- top bar -->
  <TopBar />

  <div class="centered-container">
    <div class="flex-wrapper">
      <div class="image-column">
        <img src="https://framerusercontent.com/images/NiwAy8X3Vf2KytmxtQVd9YvOgvE.png?scale-down-to=1024&width=2048&height=2048" alt="Product image">
      </div>
      <div class="info-column">
        <h1 class="title">El testigo</h1>
        <p class="price">299.99€</p>
        <div class="referral-code">
          <label for="referral">Introducir código de referido:</label>
          <input type="text" id="referral" v-model="referralCode" placeholder="Escribe tu código aquí">
          <button @click="Pay" class="action-btn">Comprar ahora</button>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        </div>
      </div>
      
      
    </div>
  </div>
</template>
<script setup>
import { ref, computed } from "vue";
import { useRouter } from 'vue-router';
import { useStore } from "vuex";
import TopBar from '@/components/TopBar.vue';

const router = useRouter();
const store = useStore();

// input model
const referralCode = ref("");
// show error if code is invalid
const errorMessage = ref("");

// get verification state from vuex
const verification = computed(() => store.getters.stateVerification);

// called when user clicks buy
const Pay = async () => {

  // call store action to check code
  await store.dispatch('verifyReferralCode', referralCode.value);
  
  // check if code is valid
  if (verification.value) {
    router.push('/payed'); // go to paid page
  } else {
    errorMessage.value = "Codigo de referido no válido, intentalo otravez"; // show error
  }
};
</script>

<style scoped>

.error-message {
  color: red;
  margin-top: 8px;
  font-weight: bold;
}
/* main centered container styles */
.centered-container {
  width: 90%;
  max-width: 1000px;
  padding: 30px;
  background-color: #fffff;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  border: 1px solid #ccc;
  border-radius: 12px;
  /* centers the container in its parent (e.g., app.vue) */
  margin: auto;
  /*position in the middle*/ 
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}


/* flex wrapper for the two columns */
.flex-wrapper {
  display: flex;
  gap: 40px; 
  align-items: flex-start; 
}

/* left column (information) styles */
.info-column {
  flex: 1; 
  min-width: 300px; 
}

.info-column .title {
  margin-top: 0;
  font-size: 2.2em;
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
}

.info-column .price {
  font-size: 2em;
  color: #2980b9; /* dark blue for the price */
  font-weight: bold;
  margin: 15px 0 25px 0;
}


button {
  background-color: #064581;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 6px;
  font-size: 1em;
  cursor: pointer;
  margin: 20px 0 20px 0; /* space below button */
  transition: background 0.3s;
}
button:hover {
  background-color: #006afdff; /* lighter on hover */
}


.referral-code {
  margin-top: 20px;
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #3498db;
  border-radius: 6px;
  background-color: #eaf6ff; /* light blue background for the referral section */
}

.referral-code label {
  display: block; /* label displayed on a separate line */
  margin-bottom: 8px;
  font-weight: bold;
  color: #2c3e50; /* dark blue/gray text color */
}

.referral-code input[type="text"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box; /* ensures padding doesn't add extra width */
  font-size: 1em;
}

/* right column (image) styles */
.image-column {
  flex: 1; 
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-column img {
  max-width: 100%; 
  height: auto;
  border-radius: 8px;
  border: 3px solid #3498db; /* blue border to highlight the image */
  box-shadow: 0 4px 10px rgba(52, 152, 219, 0.3); /* shadow with a blue tint */
}

/* media query for responsiveness */
@media (max-width: 768px) {
  .flex-wrapper {
    flex-direction: column; 
    gap: 20px; /* space between stacked items */
  }
}
</style>