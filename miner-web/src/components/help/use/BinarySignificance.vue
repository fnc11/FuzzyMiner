<template>
    <div>
        <label class="header">Binary Significance</label>
        <p>Binary significance describes the relative importance of a precedence relation between
            two event classes, i.e. an edge in the graph.In our application, it primarily influences the selection of
            edges which will be
            included in the simplified process model. To select this metrics select 'Binary Significance' from the
            dropdown menu.</p>
        <br>
        <ul>
            <div class="block">
                <el-image src="/static/img/binarysignificance.PNG" alt=""/>
            </div>
        </ul>
        <ol>
            <li><b>Frequency Significance Metrics : </b>This metric is also
                the most important implementation for binary significance. The more often two event
                classes are observed after one another, the more significant their precedence relation.
            </li>
            <br>
            <li><b>Distance Significance Metrics : </b>The more the significance of a relation differs from its source
                and target nodes’
                significances, the less its distance significance value. Distance significance locally amplifies crucial
                key relations between event
                classes, and weakens already insignificant relations. Thereby, it can clarify ambiguous
                situations in edge abstraction, where many relations “compete” over being included in
                the simplified process model.
            </li>
        </ol>

    </div>
</template>

<script>
    export default {
        name: "BinarySignificance"
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