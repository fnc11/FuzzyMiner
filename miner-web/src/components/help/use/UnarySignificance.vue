<template>
    <div>
        <label class="header">Unary Significance</label>
        <p>
            Unary significance matrix describes the relative importance of the event class,which is represented as
            node in the graph.To select this metrics select 'Unary Significance' from the
            dropdown menu.
        </p>
        <ul>
            <div class="block">
                <el-image src="/static/img/unary.PNG" alt=""/>
            </div>
        </ul>
        <ol>
            <li><b>Frequency Significance Metrics: </b>More often a
                certain event class is observed in the log, the more significant it is.Frequency is a logbased metric,
                and is in fact the most intuitive of all metrics.
            </li>
            <br>
            <li><b>Routing Significance Metrics : </b> The idea
                behind routing significance is that points, at which the process either forks (i.e., split
                nodes) or synchronizes (i.e., join nodes), are interesting in that they substantially define
                the structure of a process. The higher the number and significance of predecessors for a
                node (i.e., its incoming arcs) differs from the number and significance of its successors
                (i.e., outgoing arcs), the more important that node is for routing in the process. Routing
                significance is important as amplifier metric, i.e. it helps separating important routing
                nodes (whose significance it increases) from those less important.
            </li>
        </ol>
    </div>
</template>

<script>
    export default {
        name: "UnarySignificance"
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