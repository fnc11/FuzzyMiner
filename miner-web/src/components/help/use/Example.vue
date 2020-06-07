<template>
    <div>
        <label class="header">Steps to generate an example model</label>
        <p>Follow below steps to generate an example model.</p>
        <br>
        <ul>
            <li><b>Step1 : </b>Click on 'Generate Example Model' on the home page.You will be navigated to the filter
                page where you can see the
                fuzzy model generated for the example log.
            </li>
            <br>
            <div class="block">
                <el-image src="/static/img/example.PNG" alt=""/>

            </div>
            <br>
            <li><b>Step2 : </b> Interpret the example log.</li>
            <div class="block">
                <el-image src="/static/img/example1.PNG" alt=""/>

            </div>
            <br>
            <p></p>
            <br>


        </ul>
    </div>
</template>

<script>
    export default {
        name: "Example",
        data() {
            return {
            }
        }
    }
</script>

<style scoped>
    .el-image {
        border-color: black;
        width: 40%;
        height: 40%;
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