<template>
    <div>
        <label-wrap class="header">Fuzzy Model Screen</label-wrap>
        <p>Fuzzy model screen appears when you select generate button on the home page, after the successful upload of
            the log
            file.In this page on the left hand side you can see the fuzzy model generated with the default values set
            for filter configurations and metrics configurations.
            On the right hand side you will see filter configurations with the default values.At the bottom of the page
            you can see a button to save fuzzy model and a button to open metrics configurations dialog.</p>
        <br>
        <div class="block">
            <el-image src="/static/img/filteredited.PNG" alt=""/>
        </div>
        <p><b>A - Fuzzy Model :</b>Image shows the generated fuzzy model for the log file you uploaded. Initially model
            image is generated based on the default values set for filter configuration and metrics configuration.

        <p><b>B - Filter Configurations : </b>Node, edge and concurrency filters can be configured here.On changing each
            of the filter values, new model is generated and rendered.
            To know in detail about filter configuration select 'Configure Filters' from the nav menu.</p>
        <p><b>C - Image Toolbar :</b> You can navigate through the history and you can see all the generated images. You
            can also apply below options on the graph image in order to view differently.
        <li>Zoom in</li>
        <li>Zoom out</li>
        <li>One to one ratio</li>
        <li>Reset</li>
        <li>Previous</li>
        <li>Next</li>
        <li>Play</li>


        <p><b>D - Save Snapshot :</b>By clicking on save snapshot button, image generated in the fuzzy model view gets dowloaded automatically. </p>
        <p><b>E - Metrics Configuration :</b> By clicking on metrics configuration button configuration dialog opens. And you can configure metrics and attenuation.To know in detail you can refer to metrics configuration section.
            User interface of the dialog looks like below.</p>
       <div class="block">
        <br>
            <el-image src="/static/img/metrics.PNG" alt=""/>
       </div>

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

    .header {
        color: black;
        font-size: 30px;
        font-weight: bold;
    }
</style>