<template>
    <div>
        <label class="header">Concurrency Filter</label>
        <p>The concurrency filter is used to resolve conflicts between two event classes. Conflicts are defined as two
            nodes which are connected in both directions. This may represent either a lengh-two-loop or two event types
            which are actually in parallel, i.e. can be executed concurrently. By default it is
            active. But you can disable it by
            uncheckig the filter concurrency checkbox.
        </p>

        <ul>
            <li><b>Preserve : </b>This parameter allows you to specify, how significant two conflicting relations need
                to be in order to both be preserved. This parameter, usually set to a low value, ensures that real
                length-two-loops will not accidentially be removed. Default value is set to 0.13
            </li>
            <br>
            <li><b>Balance : </b>This parameter will influence the resolution of all conflicting relations which do not
                meet the preservation criteria.If set to a high value, conflicting relations will rather be resolved by
                removing both relations from the graph. If set to a low value,
                conflicting relations will rather be preserved by removing only the weaker relation.Default value is
                0.7
            </li>
            <br>
            <div class="block">
                <el-image src="/static/img/concurrency.PNG" alt=""/>
            </div>
        </ul>


    </div>
</template>

<script>
    export default {
        name: "ConcurrencyFilter"
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