<template>
    <div>
        <label class="header">Edge Filter</label>
        <p>The edge filter influences the amount of edges, and their selection, which will be included
        in the displayed graph.You can see 2 edge filter implementation in our application. You can see the radio button to chose the edge filter.
            Only one choice is possible. Preserve, S/c ratio and Ignore self loops can be modified on both the edge filters.
            Where as interpret absolute can be selected only when fuzzy edge filter is active.
        </p>
        <ol>
            <li><b>Best edges filter : </b>This filter preserves the best incoming and outgoing edge for each node, i.e. event class.
            </li>
            <br>
            <li><b>Fuzzy edges filter : </b>The fuzzy edges filter ranks all connected edges of a node locally.

                <ul>
                     <br>
                    <li><b>S/C Ratio :</b> This parameter configures the evaluation method for the ranking, as a ratio between significance and correlation.
                        When the S/C ratio is set to 1.0, only the most significant edges will be preserved; conversely, a value of 0.0 will only take correlation into account.</li>
                    <br>
                    <li><b>Preserve : </b>This parameter configures the amount of edges which will be preserved within each local ranking. The lower the preserve, the less edges will be included in the graph.</li>
                    <br>
                    <li><b>Interpret Absolute : </b>This checkbox will change the interpretation of the preserve value. If it is unchecked then default value of the preserve is taken.
                    Otherwise preserve is interpreted as percentage in the value range which will be preserved, leading to higher variation per nodes.</li>
                </ul>
            </li>
            <p><b>Ignore self-loops : </b>This checkbox can be selected and deselected on both the filters.If it is active, relations of nodes to themselves are not included in the evaluation for local ranking, and can thus not influence the amount of preserved links.
            By default it is set active.</p>
            <div style="display: flex">
                <el-image src="/static/img/edge.PNG" alt=""/>

            </div>
        </ol>

    </div>
</template>

<script>
    export default {
        name: "EdgeFilter"
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