<template>
    <div class="help-content">
        <div align="center">
            <div class="text-center-align header-text">Do you want to know how to use our product?</div>
            <br>
            <iframe width="540" height="400"
                    src="https://www.youtube.com/embed/tgbNymZ7vqY?controls=1c">
            </iframe>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Help"
    }
</script>

<style scoped>
    .help-content{
        position: relative;
        height: 70vh;
        overflow: hidden;
        top: 30px;
    }

    .header-text {
        font-family: "Sitka Subheading";
        font-size: xx-large;
        color: #3875d7;

    }

    .el-collapse-item__header {
        color: green;
    }
</style>
