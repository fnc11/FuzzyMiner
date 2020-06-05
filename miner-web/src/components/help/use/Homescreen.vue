<template>
    <div>
        <h2>Fuzzy Web Home Screen</h2>
        <p>When you launch our fuzzy web application, you will see home screen. User interface for the home page looks like the below image.
        Page allows you to upload logs, generate model and to view example model. Generate model will be enabled only after you upload the log successfully. You can also navigate between home and help page using button bar provided at the top right corner. </p>
        <br>
        <div class="block">
            <el-image  src="/static/img/Home.PNG" alt="" />
        </div>
        <p><b>Upload :</b>To upload the log file which is in .xes format.</p>
        <p><b>Generate :</b>To generate the process graph after the successful upload of the logs.</p>
        <p><b>Generate Exaple Model :</b> To Generate a model based on the example log.</p>
        <p><b>Home/Help </b>: To navigate between home and help page.</p>
    </div>

</template>

<script>
    export default {
        name: "Homescreen",
        data(){
            return{
            }
        }
    }
</script>

<style scoped>
    .el-image{
        border-color: black;
        width: 60%;
        height: 60%;
        border:ridge;
    }
    .block{
        border-color: black;
    }
    p{
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Droid Sans', 'Helvetica Neue', Arial, sans-serif;
        font-size: 15px;
    }

</style>