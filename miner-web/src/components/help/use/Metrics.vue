<template>
   <div>
       <label class="header">Metrics Configurations</label>
       <p>Each metric has the same set of configuration options, which help you to optimize the measurements taken with respect to your specific situation:
       </p>

       <ol>
        <li><b>Weight : </b> All metrics of a specific type (unary or binary significance and correlation) will be aggregated before taken into account for mining. By modifying the weight of each metric, you can specify how strongly it will be taken into account when aggregated. For example, to emphasize a specific metric, reduce the weight of all other metrics of this type.</li>
       <br>
           <li><b>Invert : </b>If this checkbox is active, all measurements of this metric will be inverted. After measurement, all values gathered by a metric will be normalized, such that the highest measurement taken will be equal to 1.0. If a metric is inverted, this means that for all measurements, 1.0 - original_value will be returned. This can be a handy tool if, e.g., you want highly frequent events to be considered less significant.</li>
       <br>
           <li><b>Active : </b>If this checkbox is non-checked, the respective metric will be ignored in the mining pass. Use this option when you think that a specific metric does not contribute to better results, or is even contra-productive. Note that setting a metric to non-active does not improve performance; the Fuzzy Miner is highly optimized for performance also when running with full-blown settings.</li>
           </ol>

   </div>
</template>

<script>
    export default {
        name: "Metrics"
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