<template>
    <div>
        <h2>Fuzzy Model Screen</h2>
        <p>Fuzzy model screen appears when you select generate button on the home page, after the successful upload of the log
            file.In this page on the left hand side you can see the fuzzy model generated with the default values set for filter configurations and metrics configurations.
            On the right hand side you will see filter configurations with the default values.At the bottom of the page you can see a button to save fuzzy model and a button to open metrics configurations dialog.</p>
         <br>
        <div class="block">
            <el-image  src="/static/img/filter.PNG" alt="" />
        </div>
        <p><b>Fuzzy Model : </b>Image shows the generated fuzzy model for the log file you uploaded. Initially model image is generated based on the default values set for filter configuration and metrics configuration.
            Image can be zoomed in, zoomed out, rotated and mirrored with a
        <p><b>Filter Configurations : </b>Node, edge and concurrency filters can be configured here.On changing each of the filter values, new model is generated and rendered.
    To know in detail about filter configuration select <el-link @click="$router.push({path: '/help/filter'})">here</el-link></p>
        <p><b>Save Snapshot :</b></p>
        <p><b>Metrics Configuration :</b></p>

    </div>
</template>

<script>
    export default {
        name: "Filterscreen"
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
</style>