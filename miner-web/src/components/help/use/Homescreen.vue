<template>
    <div>
        <U><h1>Fuzzy Web Home Screen</h1></U>
        <div class="block">
        <el-image :src="src"></el-image>
            </div>
    </div>

</template>

<script>
    export default {
        name: "Homescreen",
        data(){
            return{
                src : "../assets/Home.PNG"
            }
        }
    }
</script>

<style scoped>

</style>