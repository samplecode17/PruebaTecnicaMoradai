<template>
  <!-- top bar -->
  <div class="top-bar" v-if="isAuthenticated">
    <span class="user-name">User: {{ user.username }}</span>
    <button @click="logOut">Logout</button>
  </div>
</template>

<script setup>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { computed } from 'vue'

const store = useStore()
const router = useRouter()

//see if isAuthentificated state is true
const isAuthenticated = computed(() => store.getters.isAuthenticated)
//get the user username
const user = computed(() => store.getters.stateUser)

// logout action (in the future extract that feature into a container)
const logOut = () => {
  store.dispatch('logOut')
  router.push('/') // optional, redirect home after logout
}
</script>

<style scoped>
/* top nav bar */
.top-bar {
  position: fixed;        /* stays on top */
  top: 0;
  left: 0;
  width: 100%;
  height: 50px;
  background-color: #064581; /* azul oscuro */
  display: flex;
  justify-content: space-between; /* user left, logout right */
  align-items: center;
  padding: 0 20px;
  color: white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  z-index: 1000;
  box-sizing: border-box;
}

/* user text on the left */
.top-bar .user-name {
  font-weight: bold;
}

/* logout button */
.top-bar button {
  background-color: white;
  color: #064581;
  border: none;
  padding: 8px 16px; 
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

.top-bar button:hover {
  background-color: #e0e0e0;
}
</style>
