<template>
  <div class="create-container">
    <h2>Crear Referral Code</h2>
    <p>Este paso es necesario para poder crear codigos de referido para probarlo</p>
    <input
      v-model="code"
      type="text"
      placeholder="Introduce tu código"
      class="input-box"
    />
    <div class="button-row">
      <button @click="createCode">Crear</button>
      <button class="home-btn" @click="goHome">Home</button>
    </div>

    <div v-if="creation === true" class="success-msg">
      Codigo de referido creado
    </div>
    <div v-else-if="creation === false" class="error-msg">
      No se ha creado el codigo, debe ser algun problema
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()
const code = ref('')

const creation = computed(() => store.getters.stateCreation)
const user = computed(() => store.getters.stateUser)

// resetear el estado al entrar y salir del componente
onMounted(() => {
  store.commit('setCreation', null)
})
onBeforeUnmount(() => {
  store.commit('setCreation', null)
})

const createCode = () => {
  // prepare the json that will be sended with the post to create a referal code
  const payload = {
    user_id: user.value.id,
    code: code.value.trim(),
  }

  store.dispatch('createReferralCode', payload)
}

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.create-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
}

h2 {
  color: #064581;
  margin-bottom: 20px;
}

.input-box {
  padding: 10px;
  width: 250px;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-bottom: 15px;
  font-size: 1em;
}

.button-row {
  display: flex;
  gap: 10px;
  justify-content: center;
}

button {
  background-color: #064581;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background-color: #006afd;
}

.home-btn {
  background-color: #999;
}

.home-btn:hover {
  background-color: #777;
}

.success-msg {
  color: green;
  margin-top: 20px;
}

.error-msg {
  color: red;
  margin-top: 20px;
}
</style>
