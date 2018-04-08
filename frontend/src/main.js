import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import swal from 'sweetalert2'
import BootstrapVue from 'bootstrap-vue'
import Vuelidate from 'vuelidate'
import VueMarkdown from 'vue-markdown'
import VueSweetalert2 from 'vue-sweetalert2';


import 'bootstrap/dist/css/bootstrap.css'
import 'mdbootstrap/css/mdb.css';
import 'prismjs/themes/prism.css'

import router from './router'
import store from './store'

axios.defaults.baseURL = 'http://127.0.0.1:5000/api';
axios.defaults.headers.accepts = 'application/json';

axios.interceptors.response.use(res => {
    console.log('inter_res', res);
    return res
}, (error) => {
    console.log('inter_error', error.response);
    console.log('CODE: ', error.response.status);
    swal("Error", error.response.data.msg, "error");
    return error
});

axios.interceptors.request.use(req => {
    console.log('inter_req', req);
    req.headers.authorization = store.getters.sessionUUID;
    return req
});

Vue.use(BootstrapVue);
Vue.use(Vuelidate);
Vue.use(VueMarkdown);
Vue.use(VueSweetalert2);

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});
