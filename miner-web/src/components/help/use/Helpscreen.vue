<template>
    <div>
   <label class="header">Help Screen</label>
    <p>This is the page where you are currently in. In case if you want to know how to navigate to the other screens and within the screen, you can refer to the below image.</p>

        <div class="block">
            <el-image src="/static/img/helpscreen.PNG" alt=""/>
        </div>
        <br>
        <p><b>A : </b>Click on banner text to navigate to the home.</p>
        <p><b>B & D : </b>Click on top button bar to navigate to home and back.</p>
        <p><b>C : </b>Navigate through the help using navigation menu.</p>
</div>
</template>

<script>
    export default {
        name: "Helpscreen"
    }
</script>


<style scoped>
    .el-image {
        border-color: black;
        width: 80%;
        height: 80%;
        border: ridge;
    }

    .block {
        border-color: black;
    }

    p, li {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Droid Sans', 'Helvetica Neue', Arial, sans-serif;
        font-size: 15px;
    }

    .header {
        color: black;
        font-size: 30px;
        font-weight: bold;
    }
</style>