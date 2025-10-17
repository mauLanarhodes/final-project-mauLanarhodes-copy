// Need to install the following libs
// npm install axios bootstrap vue-chartjs chart.js


import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

//import bootstrap css
import "bootstrap/dist/css/bootstrap.min.css";
//import bootstrap library
import "bootstrap";

const app = createApp(App)

app.use(router)

app.mount('#app')
