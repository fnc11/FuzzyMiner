<template>
    <div>
        <label class="header">Node Filter</label>
        <p>The filter controls the amount of event classes which will be included in the dispayed graph.
            It has single control <b>significance cutoff</b>. All event classes having the significance
        lower than the specified value will be filtered out. Either they will be removed or will be aggregated in the cluster.
            You can use the slider to change the value of significance cutoff. Default value is set to 0.715</p>
        <br>
         <div class="block">
            <el-image src="/static/img/node.PNG" alt=""/>
        </div>
    </div>
</template>

<script>
    export default {
        name: "NodeFilter"
    }
</script>

<style scoped>
  .el-image {
        border-color: black;
        height: 500px;
        width: 140px;
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