<template>
    <div>
        <h2>Steps to generate a fuzzy model</h2>
        <p>Follow below instructions in order to generate a fuzzy model.</p>
        <br>
        <ul>
            <li><b>Step1 : </b> Launch fuzzy miner application in chrome browser.</li>
            <br><br>
            <li><b>Step2 : </b>Click on upload logs button to upload a log from your files.
            </li>
            <br>

            <el-image src="/static/img/upload3.PNG" alt=""/>

            <br>

            <el-image src="/static/img/uploadlog1.PNG" alt=""/>
            <br><br><br>

            <li><b>Step3 : </b>Generate button gets activated on successful log upload. Click on it.</li>
            <br>

            <el-image src="/static/img/uploadlog2.PNG" alt=""/>

            <br><br><br>
            <li><b>Step4 : </b>You will be navigated to the filter screen where you can see the generated fuzzy model.
            </li>
            <br>

            <el-image src="/static/img/filter.PNG" alt=""/>

        </ul>
    </div>
</template>

<script>
    export default {
        name: "Generate"
    }
</script>

<style scoped>
    .el-image {
        width: 60%;
        height: 60%;
        border: ridge;
    }

    p, li {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Droid Sans', 'Helvetica Neue', Arial, sans-serif;
    }

</style>