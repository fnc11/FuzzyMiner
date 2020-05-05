<template>
    <div id="app">
        <el-container>
            <el-header>
                <el-row class="row-bg">
                    <el-col :span="20">
                        <div class="grid-content bg-purple-dark">
                            <label>FuzzyMinerWeb</label>
                        </div>
                    </el-col>
                    <el-col :span="4">
                        <el-button-group>
                            <el-button :disabled="$route.name === 'Home'" @click="$router.push({path: '/'})">Home
                            </el-button>
                            <el-button :disabled="$route.name === 'Help'" @click="$router.push({path: '/help'})">
                                Help
                            </el-button>
                        </el-button-group>
                    </el-col>
                </el-row>
            </el-header>

            <el-main>
                <router-view/>
            </el-main>
            <el-footer class="fluid-container footer">
                <p>@Copy right: 2020</p>
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

<style scoped>
    .grid-content{
        font-family: "Sitka Heading";
        font-size: x-large;
        color: midnightblue;
        font-weight: bold;

    }
    .fluid-container.footer {
        margin-bottom: 0;
    }

    .fluid-container.footer > *:last-child {
        text-align: center;
    }
</style>
