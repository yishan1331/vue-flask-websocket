<template>
    <div class="Monitor">
        <h1>This is an Monitor page</h1>
        <button type="button" class="mr-3 btn btn-primary" @click="socket_connect">連接socket</button>
        <button type="button" class="mr-3 btn btn-success" @click="inputfile(true)">測試資料開始</button>
        <button type="button" class="mr-3 btn btn-warning" @click="inputfile(false)">測試資料結束</button>
        <button type="button" class="mr-3 btn btn-danger" @click="cleanfile">清除測試資料</button>
        <div style="text-align:center;margin:15px">
            <b-form-select v-model="selected" :options="options" style="width:310px" size="lg">
                <template v-slot:first>
                    <b-form-select-option :value="null" disabled>-- Please select an option --</b-form-select-option>
                </template>
            </b-form-select>
        </div>
        <button type="button" class="btn btn-info" @click.prevent="monitor">送出</button>
        <!-- {{set_latest_number}} | {{sid}} -->
        <div id="loggingStreamView">
            <div v-for="(item,key) in log_list" :key="key">{{item}}</div>
        </div>
    </div>
</template>
<script>
import axios from "axios";
export default {
    name: "Monitor",
    data() {
        return {
            log_list: [],
            set_latest_number: 0,
            options: [],
            selected: null,
            sid: null,
        };
    },
    components: {},
    watch: {
        set_latest_number: {
            handler() {
                console.log("@@@@@@@");
                // this.QueryData();
                this.$socket.emit("keep");
                // this.$socket.emit("keep",this.selected);
            },
        },
    },
    updated() {
        // 聊天定位到底部
        //https://zhuanlan.zhihu.com/p/89906315
        //https://lianjy357.github.io/baymax/2019/04/24/Vue%E8%81%8A%E5%A4%A9%E6%A1%86%E9%BB%98%E8%AE%A4%E6%BB%9A%E5%8A%A8%E5%88%B0%E5%BA%95%E9%83%A8/
        let ele = document.getElementById("loggingStreamView");
        ele.scrollTop = ele.scrollHeight;
    },
    created() {
        this.getLogFile();
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
                    this.sid = val.sid;
                    console.log("成功连接服务！！！");
                });
            } else {
                console.log("already connected");
            }
            // this.socket_subscribe_watch_log();
        },
        getLogFile() {
            let vm = this;
            axios
                // .get("http://localhost:5000/getLoggingFile", {
                .get("getLoggingFile", {
                    headers: {
                        "Access-Control-Allow-Origin": "*",
                    },
                })
                .then(function (response) {
                    console.log(response);
                    vm.options = response.data.file;
                })
                .catch(function (error) {
                    // 请求失败处理
                    console.log(error);
                });
        },
        //註冊監聽watch_log事件
        monitor() {
            let vm = this;
            console.log(vm.selected);
            vm.log_list = [];
            vm.set_latest_number = 0;

            axios
                // .get("http://localhost:5000/monitorFile/" + vm.selected, {
                .get("monitorFile/" + vm.selected, {
                    headers: {
                        "Access-Control-Allow-Origin": "*",
                    },
                })
                .then(function (response) {
                    console.log(response);
                    if (response.data == "ok") {
                        console.log("~~~socket_subscribe~~~~");
                        vm.$socket.emit(vm.selected, vm.selected);
                        console.log("~~~socket_subscribe~~~~");
                        vm.options.forEach((element) => {
                            //將舊的訂閱全部取消，以免同時抓取多種訂閱
                            vm.sockets.listener.unsubscribe("watch_" + element);
                        });
                        vm.sockets.listener.subscribe(
                            "watch_" + vm.selected,
                            (val) => {
                                if (
                                    vm.set_latest_number <
                                        val.already_print_num ||
                                    (vm.set_latest_number == 0 &&
                                        val.already_print_num == 0)
                                ) {
                                    console.log(val.data);
                                    console.log(val.already_print_num);
                                    vm.set_latest_number =
                                        val.already_print_num;
                                    vm.log_list.push(val.data);
                                }
                            }
                        );
                        console.log(vm.sockets.listener);
                        console.log(vm.sockets);
                    }
                })
                .catch(function (error) {
                    // 请求失败处理
                    console.log(error);
                });
        },
        inputfile(status) {
            let vm = this;
            axios
                // .get("http://localhost:5000/inputfile/" + status, {
                .get("inputfile/" + status, {
                    headers: {
                        "Access-Control-Allow-Origin": "*",
                    },
                })
                .then(function (response) {
                    console.log(response);
                })
                .catch(function (error) {
                    // 请求失败处理
                    console.log(error);
                });
        },
        cleanfile() {
            let vm = this;
            axios
                // .get("http://localhost:5000/cleanfile", {
                .get("cleanfile", {
                    headers: {
                        "Access-Control-Allow-Origin": "*",
                    },
                })
                .then(function (response) {
                    console.log(response);
                })
                .catch(function (error) {
                    // 请求失败处理
                    console.log(error);
                });
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
            // this.$socket.emit("disconnect",this.selected);
            this.sockets.listener.unsubscribe("re_connect");
            console.log(this.$socket.disconnected);
        }
        next();
    },
};
</script>
<style scoped>
#loggingStreamView {
    margin: 11px 0 4px;
    background-color: #f7f8fb;
    border: 1px solid #e3e7ef;
    border-radius: 4px;
    height: 600px;
    overflow-y: scroll;
}
</style>
