<template>
    <div class="help-content">
        <div align="center">
            <div class="text-center-align header-text">Do you want to know how to use our product?</div>
            <br>
            <iframe width="540" height="400"
                    src="https://www.youtube.com/embed/PVhmK-Gc8oE?controls=1c">
            </iframe>
        </div>
        <el-collapse accordion>
            <el-collapse-item name="1">
                <template class="collapse-text" slot="title">
                    <div class="collapse-text-header">How to interpret graph view?</div>
                </template>
                <div class="collapse-text"><p>The ultimate goal of the Fuzzy Miner is to create an appropriate graph representation of the process expressed in the mined log.
                    <b>Yellow square nodes</b> represent event classes, their significance (maximal value is 1.0) is provided below the event class name in each node.</p>
                    <p>Less significant and lowly correlated behavior is discarded from the process model, i.e. nodes and arcs which fall into this category are removed from the graph. Coherent groups of less significant behavior, which is however highly correlated, is represented in aggregated form, as clusters. <b>Cluster nodes</b> are represented as ovals.</p>

                </div>
            </el-collapse-item>
            <el-collapse-item name="2">
                <template class="collapse-text" slot="title">
                    <div class="collapse-text-header">How to configure filters?</div>
                </template>
                <div class="collapse-text">
                    <ul>
                        <li><b>Node Filter:</b>The node filter controls the amount of event classes which will be
                            included in the displayed graph. It features a single control, the significance cutoff. All
                            event classes with an aggregate significance measure lower than the value specified in the
                            significance cutoff will be subject to filtering. Depending on their environment, they will
                            be either removed from the graph or aggregated in a cluster.
                        </li>
                        <li><b>Edge Filter:</b>
                        The edge filter influences the amount of edges, and their selection,
                        which will be included in the displayed graph. Currently there are two edge filter
                        implementations provided.
                        <p><b>Best edges filter</b>
                            This filter preserves the best incoming and outgoing edge for each node, i.e. event class.
                        </p>
                        <p><b>Fuzzy edges filter</b>
                            The fuzzy edges filter ranks all connected edges of a node locally. The parameter <b>S/C
                                ratio</b> configures the evaluaton method for this ranking, as a ratio between
                            significance and correlation. When the S/C ratio is set to 1.0, only the most significant
                            edges will be preserved; conversely, a value of 0.0 will only take correlation into account.
                            The <b>cutoff</b> parameter configures the amount of edges which will be preserved within
                            each local ranking. The lower the cutoff, the less edges will be included in the graph.
                            If the checkbox <b>ignore self-loops</b> is active, relations of nodes to themselves are not
                            included in the evaluation for local ranking, and can thus not influence the amount of
                            preserved links.
                            The checkbox <b>interpret absolute</b> will change the interpretation of the cutoff value.
                            If it is not checked, the default setting, the cutoff value will be interpreted in a
                            relative manner, i.e. the same percentage of links will be preserved for each node. If the
                            cutoff value is interpreted as absolute, the cutoff is interpreted as the percentage in the
                            value range which will be preserved, leading to higher variation per nodes.</p>
                        </li>
                        <li><b>Concurrency Filter:</b>
                            The concurrency filter is used to resolve conflicts between two event classes. Conflicts are
                            defined as two nodes which are connected in both directions. This may represent either a
                            lengh-two-loop or two event types which are actually in parallel, i.e. can be executed
                            concurrently.
                            <p>The <b>preserve</b> parameter allows you to specify, how significant two conflicting
                                relations need to be in order to both be preserved. This parameter, usually set to a low
                                value, ensures that real length-two-loops will not accidentially be removed.</p>
                            <p>All conflicting relations which do not meet the preservation criteria are resolved. The
                                <b>balance</b> parameter will influence the method of resolution. If set to a high
                                value, conflicting relations will rather be resolved by removing both relations from the
                                graph. If set to a low value, conflicting relations will rather be preserved by removing
                                only the weaker relation.</p></li>
                    </ul>
                </div>

            </el-collapse-item>
            <el-collapse-item name="3">
                <template class="collapse-text" slot="title">
                    <div class="collapse-text-header">How to configure Metrics?</div>
                </template>
                <div class="collapse-text">
                    <ul>Each metric has the same set of configuration options, which help you to optimize the
                        measurements taken with respect to your specific situation:
                        <li><b>weight:</b> All metrics of a specific type (unary or binary significance and correlation)
                            will be aggregated before taken into account for mining. By modifying the weight of each
                            metric, you can specify how strongly it will be taken into account when aggregated. For
                            example, to emphasize a specific metric, reduce the weight of all other metrics of this
                            type.
                        </li>
                        <li><b>invert:</b> If this checkbox is active, all measurements of this metric will be inverted.
                            After measurement, all values gathered by a metric will be normalized, such that the highest
                            measurement taken will be equal to 1.0. If a metric is inverted, this means that for all
                            measurements, 1.0 - original_value will be returned. This can be a handy tool if, e.g., you
                            want highly frequent events to be considered less significant.
                        </li>
                        <li><b>active:</b> If this checkbox is non-checked, the respective metric will be ignored in the
                            mining pass. Use this option when you think that a specific metric does not contribute to
                            better results, or is even contra-productive. Note that setting a metric to non-active does
                            not improve performance; the Fuzzy Miner is highly optimized for performance also when
                            running with full-blown settings.
                        </li>
                    </ul>
                </div>

            </el-collapse-item>
            <el-collapse-item name="4">
                <template class="collapse-text" slot="title">
                    <div class="collapse-text-header">What is Attenuation?</div>
                </template>
                <div class="collapse-text">
                    <ul>Obviously, you want longer-distance relationships to affect the measurement less than direct
                        following relationships. This is what the attenuation settings are for.
                        <li><b>Linear Attenuation:</b>This will ensure linear attenuation with rising distance of
                            events.
                        </li>
                        <li><b>Nth root Attenuation:</b>The Nth root attenuation allows for negative exponential
                            attenuation by configuring an Nth root function. A relatively high radical value will
                            progressively attenuate the longer-distance measure points, which is useful when you want to
                            focus on short-term relationships. A relatively low radical helps when you have frequent
                            interlockings of noise events which obscure the important relationships.
                        </li>
                    </ul>
                </div>

            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
    export default {
        name: "Help"
    }
</script>

<style scoped>
    .help-content {
        position: relative;
        height: 110vh;
        overflow: hidden;
        top: 30px;
    }

    .header-text {
        font-family: "Sitka Subheading";
        font-size: xx-large;
        color: darkorange;

    }

    .collapse-text-header {
        color: #2f70cd;
        font-size: medium;
        font-family: "Sitka Subheading";
    }

    .collapse-text {
        color: black;
        font-size: small;
        font-family: Calibri;
    }
</style>
