

import { createApp } from 'vue'
import App from './App.vue'
import store from './store';
import router from './router';

//app creation
const app = createApp(App);

//inject vuex global state config
app.use(store);
//inject router 
app.use(router);

app.mount("#app");


