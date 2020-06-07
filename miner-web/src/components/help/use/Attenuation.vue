<template>
    <div>
        <label class="header">Attenuation</label>
        <p>You can change attenuation from metrics configuration dialog.In this dialog if you select attenuation tab
            you can see an option to select one of the 2 attenuations. i.e Linear and N(th) root attenuation. You can
            also change maximal event distance.
        </p>
        <ol>
            <li><b>Maximal event distance :</b>
                The Fuzzy Miner is not limited to only measuring the significance and correlation of two events directly
                following one another in the log, it can also measure longer-term relationships,
                that is where maximal event distance is used. It can consider upto 20 events from the current event
                class (i.e node).
            </li>
            <br>
            <li><b>Attenuation Settings</b>
                <p>
                    <i>Linear Attenuation : </i>This will ensure linear attenuation with rising distance of events.
                </p>

                <i>Nth root attenuation : </i>This allows for negative exponential attenuation by configuring an Nth
                root function. A relatively high radical value will progressively attenuate the maximal event distance,
                which is useful when you want to focus on short-term relationships. A relatively low radical helps when
                you have
                frequent interlocking of noise events which obscure the important relationships.

            </li>
            <br>
            <div style="display: flex">
                <el-image src="/static/img/attenuation1.PNG" alt=""/>

            </div>
            <br>
            <p>Steps to modify :</p>
            <ul>
                <li>Click on A to select attenuation from the Metrics configuration dialog.
                </li>
                <li>You can slide B to modify maximal event distance.  </li>
                <li>You can change the  radical by sliding C.</li>
                <li>To change it to linear attenuation click on D.</li>
                <li>Finally save the configuration by clicking E.</li>
            </ul>
        </ol>

    </div>
</template>

<script>
    export default {
        name: "LinearAttenuation"
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