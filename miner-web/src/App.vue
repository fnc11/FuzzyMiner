<template xmlns:el-col="http://www.w3.org/1999/html">
    <div id="app">
        <el-container class="el-container">
            <el-header class="header-bg" height="6.5%">
                <el-row type="flex" justify="end">
                    <el-col :span="20">
                        <div class="grid-content" align="left">
                            <label @click="$router.push({path: '/'})">FuzzyMinerWeb</label>
                        </div>
                    </el-col>

                    <el-col :span="5">
                        <div class="button-group">
                            <el-button-group>
                                <el-button :disabled="$route.name === 'Home'" @click="$router.push({path: '/'})">Home
                                </el-button>
                                <el-button :disabled="$route.name === 'Help'" @click="$router.push({path: '/help'})">
                                    Help
                                </el-button>
                            </el-button-group>
                        </div>
                    </el-col>
                </el-row>
            </el-header>
            <el-main class="el-main">
                <router-view/>
            </el-main>
            <el-footer class="fluid-container footer" height="5%">
                <p>@Copyright: 2020</p>
            </el-footer>
        </el-container>
    </div>
</template>

<script>
    export default {
        name: 'App',
        methods: {
        }
    }
</script>

<style>
    html, body {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: auto;
    }
</style>

<style scoped>
    #app {
        height: 100%;
    }

    .el-main{
        overflow: hidden;
    }
    .header-bg {
        top: 0;
        position: relative;
        width: 100%;
        background-color: lightseagreen;
    }

    .grid-content {
        font-family: "Sitka Heading";
        font-size: xx-large;
        color: black;
        font-weight: bold;
        line-height: 1.7;

    }

    .fluid-container.footer {
        bottom: 0;
        position: absolute;
        width: 100%;
        background-color: lightseagreen;

    }

    .fluid-container.footer > *:last-child {
        text-align: center;


    }

    .button-group {
        position: absolute;
        bottom: 0;
    }
.el-container{

}



</style>
