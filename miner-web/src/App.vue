<template>
    <div id="app">
        <el-container>
            <el-header>
                <label>Fuzzy Miner Web</label>
                <el-button-group>
                    <el-button :disabled="$route.name === 'Home'" @click="$router.push({path: '/'})">Home</el-button>
                    <el-button :disabled="$route.name === 'Help'" @click="$router.push({path: '/help'})">Help</el-button>
                </el-button-group>
            </el-header>
            <el-main>
                <router-view />
            </el-main>
            <el-footer>
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
</style>
