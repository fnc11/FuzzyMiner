<template>
    <div class="page-layout">
        <el-row :gutter="10">
            <el-col :span="16" align="middle">
                <div class="model-view">
                    <h3 class="text-center-align">Fuzzy Model</h3>
                    <div class="el-tabs--border-card grid-content process-graph-view">
                        <canvas></canvas>


                        <!-- here should be canvas -->
                    </div>

                    <el-button>Save Snapshot</el-button>

                </div>
            </el-col>
            <el-col :span="8">
                <div class="model-view">
                    <h3 class="text-center-align">Configurations</h3>
                    <el-row :gutter="10" class="el-tabs--border-card filter-container">
                        <el-col :span="8" class="grid-content el-table--border">
                            <h4>Node Filter</h4>
                            <br>
                            <div align="center">
                            <label>Significance Cutoff</label>
                                <el-slider vertical v-model="node" height="320px" @change="nodeChanged" />
                                <label> {{ node / 100 }}</label>
                            </div>
                        </el-col>
                        <el-col :span="8" class="grid-content el-table--border">
                            <h4>Edge Filter</h4>
                            <br>
                            <label>Edge Transformer</label>
                            <el-radio-group>
                                <el-radio :label="1">Best Edges</el-radio>
                                <el-radio :label="2">Fuzzy Edges</el-radio>
                            </el-radio-group>
                            <el-row :gutter="20">
                            <el-col :span="10">
                                <label>S/C Ratio</label>

                                <el-slider vertical v-model="sc" height="320px" @change="scChanged" />
                                <label>{{ sc / 100 }}</label>
                            </el-col>
                               <el-col :span="10">
                                   <label>Cutoff</label>
                                   <el-slider vertical v-model="cutoff" height="320px" @change="cutoffChanged" />
                                   <label>{{ sc / 100 }}</label>
                               </el-col>
                            </el-row>
                            <el-checkbox v-model="loops">Ignore Self-Loops</el-checkbox>
                            <el-checkbox v-model="absolute">Interpret Absolute</el-checkbox>
                        </el-col>
                        <el-col :span="8" class="grid-content el-table--border">
                            <div class="">

                            <h4>Concurrency Filter</h4>
                            <el-checkbox v-model="concurrency">Filter Concurrency</el-checkbox>

                            <el-row :gutter="20" class="slider-position">

                                <el-col :span="10" align="left">
                                    <label>Preserve</label>
                                    <el-slider vertical v-model="preserve" height="320px" @change="preserveChanged" />
                                    <label>{{ preserve / 100 }}</label>
                                </el-col>

                                <el-col :span="10" align="right">
                                    <label>Balance</label>
                                    <el-slider vertical v-model="balance" height="320px" @change="balanceChanged" />
                                    <label>{{ balance / 100 }}</label>
                                </el-col>

                            </el-row>
                        </div>
                        </el-col>
                    </el-row>
                    <div class="text-center-align metrics">
                        <el-button @click="dialog = true">Metrics Configuration</el-button>
                    </div>
                </div>
            </el-col>
        </el-row>
        <el-dialog
                title="Metrics"
                :visible.sync="dialog"
                width="40%">
            <div>
                <div>
                    <label>Metrics Type</label>
                    <el-dropdown>
                        <el-button type="text">Select Type<i class="el-icon-arrow-down el-icon--right" /></el-button>
                    </el-dropdown>
                </div>
                <div>
                    <label>Unary Metrics</label>
                    <div>
                        <el-checkbox v-model="incFrequency">Include</el-checkbox>
                        <div>
                            <label>Frequency Significance</label>
                            <label>Weight</label>
                            <el-slider v-model="frequencyWeight"></el-slider>
                            <el-checkbox v-model="invertFrequency">Invert the Significance</el-checkbox>
                        </div>
                    </div>
                    <div>
                        <el-checkbox v-model="incRouting">Include</el-checkbox>
                        <div>
                            <label>Routing Significance</label>
                            <label>Weight</label>
                            <el-slider v-model="routingWeight"></el-slider>
                            <el-checkbox v-model="invertRouting">Invert the Significance</el-checkbox>
                        </div>
                    </div>
                    <p>Note: One of them has to be selected or the model will include one implicitly.</p>
                </div>
            </div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialog = false">Save</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    import { nodeFilter, scRatio, cutoff, preserve, balance, metrics } from '@/api/filter';

    export default {
        name: "Filter",
        data() {
            return {
                node: 50,
                edge: 1,
                sc: 50,
                cutoff: 50,
                preserve: 50,
                balance: 50,
                loops: false,
                absolute: false,
                concurrency: false,
                // staticMethod: false,
                dialog: false,
                incFrequency: true,
                frequencyWeight: 50,
                invertFrequency: true,
                incRouting: true,
                routingWeight: 50,
                invertRouting: true
            }
        },
        methods: {
            async nodeChanged(value) {
                await nodeFilter({
                    value: value
                });
                console.log(value);
            },
            async scChanged(value) {
                await scRatio({
                    value: value
                });
                console.log(value);
            },
            async cutoffChanged(value) {
                await cutoff({
                    value: value
                });
                console.log(value);
            },
            async preserveChanged(value) {
                await preserve({
                    value: value
                });
                console.log(value);
            },
            async balanceChanged(value) {
                await balance({
                    value: value
                });
                console.log(value);
            },
            async saveConfig() {
                await metrics({
                    value: value
                });
            },
        },
    }
</script>

<style scoped>
    .model-view {
        width: 90%;
        position: relative;
        top: 20px;
        display: block;
    }
    .text-center-align{
        text-align:center;
    }
    .page-layout{
        position:relative;
        top:40px;
        height:720px;
    }
    .filter-container{
        height:560px;
       border-color: #f0f0f0;

    }
    .slider-position{
        top:30px;
    }
    .grid-content{
        height: inherit;

    }
    .process-graph-view{
        height: 560px;
        border-color: #f0f0f0;
        overflow: scroll;
    }
    .button-height{

        height: inherit;
        top:5px;
    }


</style>
