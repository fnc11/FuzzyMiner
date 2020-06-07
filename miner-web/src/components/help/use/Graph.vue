<template>
    <div>
        <label class="header">Graph View</label>
        <br>
        <p>The main idea of the fuzzy miner is to create an appropriate process model of the mined log.
            The graph view let's you explore this graph. You can fine tune the graph using the filter configurations.
            Also default metrics configuration can be changed in the metrics configuration dialog.</p>
        <p>The graph can be easily interpreted. Nodes represent event classes. Nodes and arcs which have less
            significance and
            less correlated behavior are removed from the graph.Nodes which have low significance but have high
            significance are aggregated to form clusters.</p>
        <br>
        <div style="display: inline-block">
            <el-image  src="/static/img/graph.PNG" alt=""/>


            <el-image  src="/static/img/graph2.PNG" alt=""/>
        </div>
        <br> <br>
        <li><b>Nodes : </b>Blue color squares represent nodes. They display event class names and significance value.
            The color intensity of the node is based on the significance. Higher the significance value, higher the blue
            color intensity. Node in the cluster A has higher significance than the other nodes in the image B.
        </li>
        <br>
        <li><b>Cluster nodes :</b> They are represented in green oval shapes. They display mean significance of the
            clustered elements and their amount.
            Higher the color intensity of the cluster, higher the mean significance. Cluster in the image A has higher mean significance than the cluster in the image B.
        </li>
        <br>
        <li><b>Edges : </b>Arcs drawn between the nodes are decorated with the significance and correlation. Arcs are called Edges.
        and are colored in a dark orange color. Darker the color, higher is the significance of the relation.</li>
    </div>
</template>

<script>
    export default {
        name: "Overview"
    }
</script>

<style scoped>
    .el-image {
        border-color: black;
        width: 280px;
        height: 260px;
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