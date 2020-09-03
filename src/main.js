import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import BootstrapVue from "bootstrap-vue";
import VueSocketIO from 'vue-socket.io';

// import socketio from 'socket.io-client';
// Vue.use(VueSocketIO, socketio('http://localhost:5000'))

Vue.use(BootstrapVue);
Vue.use(new VueSocketIO({
    //研发环境会打印socket初始化过程+socket中定义的事件
    debug: false,
    //我们的鉴权是拼接在query的 这个根据自己项目的实际情况来
    connection: '/',
    // connection: 'http://localhost:5000',
    options: {
        autoConnect: false//自动连接
        //https://github.com/MetinSeylan/Vue-Socket.io/issues/137
    }
}))

Vue.config.productionTip = false

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
