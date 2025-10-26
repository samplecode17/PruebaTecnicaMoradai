<template>
  <div class="auth">
    <div class="card">
      <!-- login section-->
      <div class="box left">
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
          <input v-model="loginForm.username" placeholder="Username" required />
          <input v-model="loginForm.password" type="password" placeholder="Password" required />
          <button>Login</button>
        </form>
      </div>

      <!-- register section-->
      <div class="box right">
        <h2>Register</h2>
        <form @submit.prevent="handleRegister">
          <input v-model="registerForm.username" placeholder="Username" required />
          <input v-model="registerForm.email" type="email" placeholder="Email" required />
          <input v-model="registerForm.password" type="password" placeholder="Password" required />
          <button>Register</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

// load the store to use the methods to modify the global state and make calls to the API
const store = useStore();
// load the router
const router = useRouter();
//login and register  reactivity
const loginForm = reactive({ username: "", password: "" });
const registerForm = reactive({ username: "", email: "", password: "" });

//handle login calling dispatch store methods to do the login rest query
const handleLogin = async () => {
  try {
    const f = new FormData();
    f.append("username", loginForm.username);
    f.append("password", loginForm.password);
    await store.dispatch("login", f);
    router.go(-1);
  } catch {
    alert("login failed");
  }
};
//handle register calling dispatch store methods to do the register rest query
const handleRegister = async () => {
  try {
    await store.dispatch("register", { ...registerForm });
    router.go(-1);
  } catch {
    alert("register failed");
  }
};
</script>

<style scoped>
/* layout */
.auth {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  
}

.card {
  display: flex;
  width: 90%;
  max-width: 900px;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* sections */
.box {
  flex: 1;
  padding: 30px;
}

.left {
  background: #fff;
  color: #004080;
  border-right: 1px solid #ccc;
}

.right {
  background: #004080;
  color: #fff;
}

/* form */
input {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #bbb;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  background: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

/* responsive */
@media (max-width: 700px) {
  .card {
    flex-direction: column;
  }
  .left {
    border-right: none;
    border-bottom: 1px solid #ccc;
  }
}
</style>
