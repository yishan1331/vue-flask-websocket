<template>
    <div class="about">
        <h1>This is an about page</h1>
        <button @click="socket_connect">连接socket</button>
        <button @click="socket_subscribe_test">查看test.txt</button>
        <button @click="socket_subscribe_test2">查看test2.txt</button>
        {{set_latest_number}}
        <div id="chatRecord" style="height:600px;border:1px solid #000;overflow-y:scroll">
            <div v-for="(item,key) in log_list" :key="key">{{item}}</div>
        </div>
    </div>
</template>
<script>
export default {
    name: "about",
    data() {
        return {
            log_list: [],
            set_latest_number: 0,
        };
    },
    components: {},
    watch: {
        set_latest_number: {
            handler() {
                console.log("@@@@@@@");
                // this.QueryData();
                this.$socket.emit("keep");
            },
        },
    },
    updated() {
        // 聊天定位到底部
        //https://zhuanlan.zhihu.com/p/89906315
        //https://lianjy357.github.io/baymax/2019/04/24/Vue%E8%81%8A%E5%A4%A9%E6%A1%86%E9%BB%98%E8%AE%A4%E6%BB%9A%E5%8A%A8%E5%88%B0%E5%BA%95%E9%83%A8/
        let ele = document.getElementById("chatRecord");
        ele.scrollTop = ele.scrollHeight;
    },
    methods: {
        // 连接socket
        socket_connect() {
            console.log(this.set_latest_number);
            if (!this.$socket.connected) {
                console.log(this.$socket);
                console.log(this.sockets);
                // 开始连接socket
                this.$socket.connect();
                this.sockets.listener.subscribe("re_connect", (val) => {
                    console.log(val);
                    console.log("成功连接服务！！！");
                });
            } else {
                console.log("already connected");
            }
            // this.socket_subscribe_watch_log();
        },
        //註冊監聽watch_log事件
        socket_subscribe_test() {
            let vm = this;
            vm.log_list = [];
            vm.set_latest_number = 0;
            console.log("~~~socket_subscribe_test~~~~");
            vm.$socket.emit("test");
            console.log("~~~socket_subscribe_test~~~~");
            vm.sockets.listener.unsubscribe("watch_test2");
            vm.sockets.listener.subscribe("watch_test", (val) => {
                if (vm.set_latest_number < val.already_print_num) {
                    console.log(val.data);
                    console.log(val.already_print_num);
                    vm.set_latest_number = val.already_print_num;
                    vm.log_list.push(val.data);
                }
            });
            //https://segmentfault.com/a/1190000022624044
        },
        socket_subscribe_test2() {
            let vm = this;
            vm.log_list = [];
            vm.set_latest_number = 0;
            console.log("~~~socket_subscribe_test2~~~~");
            vm.$socket.emit("test2");
            console.log("~~~socket_subscribe_test2~~~~");
            vm.sockets.listener.unsubscribe("watch_test");
            vm.sockets.listener.subscribe("watch_test2", (val) => {
                if (vm.set_latest_number < val.already_print_num) {
                    console.log(val.data);
                    console.log(val.already_print_num);
                    vm.set_latest_number = val.already_print_num;
                    vm.log_list.push(val.data);
                }
            });
            //https://segmentfault.com/a/1190000022624044
        },
    },
    //調用router守衛，在離開時將socket disconnect
    beforeRouteLeave(to, from, next) {
        console.log(to);
        console.log(from);
        console.log(this.$socket.connected);
        if (this.$socket.connected) {
            console.log(this.$socket.disconnected);
            this.$socket.disconnect(); // 結束socket
            this.sockets.listener.unsubscribe("re_connect");
        }
        next();
    },
};
</script>
