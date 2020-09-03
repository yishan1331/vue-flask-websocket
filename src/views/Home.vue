<template>
    <div class="home">
        <img alt="Vue logo" src="../assets/logo.png" />
        <!-- <HelloWorld msg="Welcome to Your Vue.js App" /> -->
    </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";

export default {
    name: "Home",
    data() {
        return {
            msg: "測試",
            log_list: ["aaa"],
        };
    },
    components: {
        HelloWorld,
    },
    methods: {
    
    },
};
</script>
