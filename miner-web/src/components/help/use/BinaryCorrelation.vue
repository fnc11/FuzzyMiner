<template>
    <div>
        <label class="header">Binary Correlation</label>
        <p> Binary correlation measures the distance of events in a precedence relation, i.e. how
            closely related two events following one another are. To select this metrics select 'Binary Correlation' from the
            dropdown menu. </p>
        <br>
        <ul>
            <div class="block">
                <el-image src="/static/img/binarycorrelation.PNG" alt=""/>
            </div>
        </ul>
        <ol>
            <li><b>Proximity Correlation : </b>This n evaluates event classes, which occur shortly after one another,
                as highly correlated. This is important for identifying clusters of events which correspond to one
                logical activity, as these are commonly executed within a short timeframe
            </li>
            <br>
            <li><b>Endpoint Correlation : </b>Originator correlation between event classes is determined from the names
                of the persons, which have triggered
                two subsequent events. The more similar these names, the higher correlated the respective event classes.
            </li>
            <br>
            <li><b>Originator Correlation : </b>It compares the
                activity names of subsequent events. More similar names will be interpreted as higher
                correlation. This is important for low-level logs including a large amount of less significant events
                which are closely related
            </li>
            <br>
            <li><b>Data Type Correlation : </b>It c evaluates event classes, where subsequent events share
                a large amount of data types (i.e., attribute keys), as highly correlated.
            </li>
            <br>
            <li><b>Data Value Correlation : </b>It takes the values of these common attributes into
                account. It uses relative similarity, i.e. small changes of an attribute value will
                compromise correlation less than a completely different value.
            </li>
        </ol>

    </div>
</template>

<script>
    export default {
        name: "BinaryCorrelation"
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