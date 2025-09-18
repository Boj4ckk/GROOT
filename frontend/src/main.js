import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import axios from "axios"


axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:5000'

const app = createApp(App)
const pinia = createPinia() 
app.use(pinia)
app.use(router)
app.mount('#app')