<template>
  <div class="centered-container">
    <div class="flex-wrapper">
      <div class="image-column">
        <img src="https://framerusercontent.com/images/NiwAy8X3Vf2KytmxtQVd9YvOgvE.png?scale-down-to=1024&width=2048&height=2048" alt="Product image">
      </div>
      <div class="info-column">
        <h1 class="title">El testigo</h1>
        <p class="price">299.99€</p>
        <button @click="goToPayment"  class="action-btn">Comprar ahora</button>
        <details class="dropdown">
          <summary>Detalles</summary>
          <p>Detalles sobre el servicio ...</p>
        </details>
        
        <details class="dropdown">
          <summary>Politica de devolución</summary>
          <p>Politica de devolucion.</p>
        </details>


        <details class="dropdown">
          <summary>Info del envio</summary>
          <p>informacion del envio ...</p>
        </details>
      </div>
      
      
    </div>
  </div>
</template>
<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
//when the button is clicked 
const goToPayment = () => {
  router.push('/payment') // navigate to /payment
}

</script>
<style scoped>
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

/* dropdown element styles */
.dropdown {
  margin-bottom: 15px;
  border: 1px solid #3498db; /* blue border */
  padding: 10px;
  border-radius: 6px;
  background-color: #f2f2f2; /* light gray/white background for distinction */
}
button {
  background-color: #064581;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 6px;
  font-size: 1em;
  cursor: pointer;
  margin-bottom: 20px; /* space below button */
  transition: background 0.3s;
}
button:hover {
  background-color: #006afdff; /* lighter on hover */
}

.dropdown summary {
  cursor: pointer;
  font-weight: bold;
  color: #2c3e50;
  padding: 5px 0;
  transition: color 0.2s;
}

.dropdown summary:hover {
    color: #2980b9;
}

.dropdown p {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #3498db; /* dashed blue separator */
  font-size: 0.95em;
  color: #2c3e50;
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
  box-shadow: 0 4px 10px rgba(52, 152, 219, 0.3); /* shadow with blue tint */
}

/* media query for responsiveness */
@media (max-width: 768px) {
  .flex-wrapper {
    flex-direction: column; 
    gap: 20px;
  }
}
</style>