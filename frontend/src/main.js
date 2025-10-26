import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import store from './store';

//app creation
const app = createApp(App);

//inject vuex global state config
app.use(store);

