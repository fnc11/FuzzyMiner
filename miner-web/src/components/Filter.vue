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

                    <el-button class="button-position el-button--default">Save Snapshot</el-button>


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
                            <el-radio-group v-model="edge">
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
                        <el-button class="button-position el-button--default" @click="dialog = true">Metrics Configuration</el-button>
                    </div>
                </div>
            </el-col>
        </el-row>
        <el-dialog
                title="Configure"
                :visible.sync="dialog"
                width="40%" style="font-family: 'Segoe UI Semibold';">
                <div>
                <el-tabs type="border-card">
                    <el-tab-pane label="Metrics">
                        <el-dropdown  type="primary" @command="selectTypes">
                            <span class="el-dropdown-link">
                                Select Metrics<i class="el-icon-arrow-down el-icon--right"></i>
                            </span>

                            <el-dropdown-menu slot="dropdown">
                                <el-dropdown-item command="unary">Unary Metrics</el-dropdown-item>
                                <hr>
                                <el-dropdown-item command="significance">Binary Significance</el-dropdown-item>
                                <hr>
                                <el-dropdown-item command="correlation">Binary Correlation</el-dropdown-item>
                            </el-dropdown-menu>
                        </el-dropdown>
                        <div v-if="selectedType === 'unary'">
                            <div>
                                <label>Frequency Significance Metric</label>
                                <div v-model="unaryFrequencySignificance" style="display: flex">
                                    <el-checkbox v-model="checked" :label="1">active</el-checkbox>
                                        <el-checkbox :label="2">Invert the significance</el-checkbox>
                                </div>
                                <label>Weight</label>
                                <el-slider v-model="unaryFrequencyWeight" />
                            </div>
                            <el-divider></el-divider>
                            <div>
                                <label>Routing Significance</label>
                                <div v-model="routingSignificance" style="display: table-cell">
                                         <el-checkbox v-model="checked" :label="1">Active</el-checkbox>
                                        <el-checkbox  :label="2">Invert the significance</el-checkbox>
                                </div>
                                <div style="vertical-align: middle">
                                <label>Weight </label>
                                <el-slider v-model="routingWeight" />
                                </div>
                            </div>
                        </div>
                        <div v-else-if="selectedType === 'significance'">
                            <div>
                                <label>Frequency Significance Metric</label>
                                <div v-model="binaryFrequencySignificance" style="display: flex">
                                    <el-checkbox v-model="checked" :label="1">active</el-checkbox>

                                    <el-checkbox  :label="2">Invert the significance</el-checkbox>
                                </div>
                                <label>Weight</label>
                                <el-slider v-model="binaryFrequencyWeight" />
                            </div>
                            <el-divider></el-divider>
                            <div>
                                <label>Distance Significance</label>
                                <div v-model="distanceSignificance" style="display: flex">
                                    <el-checkbox v-model="checked" :label="1">active</el-checkbox>
                                    <el-checkbox  :label="2">significance</el-checkbox>
                                </div>
                                <label>Weight</label>
                                <el-slider v-model="distanceWeight" />
                            </div>
                        </div>
                        <div v-else>

                            <div v-for="(item, index) in binaryCorrelation" :key="index">
                                 <el-divider></el-divider>
                                <label>{{ item.name }}</label>
                                <div style="display: flex">
                                    <el-checkbox v-model="checked" :label="1">active</el-checkbox>

                                    <el-checkbox  :label="2">Invert the significance</el-checkbox>
                                </div>
                                <label>Weight</label>
                                <el-slider v-model="item.weight" />

                            </div>

                        </div>
                    </el-tab-pane>
                    <el-tab-pane label="Attenuation">
                        <div>
                            <label>Maximal event distance</label>
                            <el-slider v-model="maximumDistance" :min="1" :max="20" />
                        </div>
                        <el-divider></el-divider>
                        <div>
                            <label >Select Attenuation</label>
                            <br>
                            <el-radio-group>
                                <el-radio :label="1">Linear Attenuation</el-radio>
                                <br>
                                <el-radio :label="2">N(th) root with radical</el-radio>
                            </el-radio-group>
                            <el-slider v-model="nrootradical" :min="2" :max="20" />
                        </div>
                    </el-tab-pane>
                </el-tabs>
            </div>
             <el-divider></el-divider>
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
                dialog: false,
                selectedType: 'unary',
                unaryFrequencySignificance: 1,
                unaryFrequencyWeight: 50,
                routingSignificance: 1,
                routingWeight: 50,
                binaryFrequencySignificance: 1,
                binaryFrequencyWeight: 50,
                distanceSignificance: 1,
                distanceWeight: 50,
                checked:true,

                binaryCorrelation: [{
                    name: 'Proximity Correlation',
                    selected: 1,
                    weight: 50
                }, {
                    name: 'Endpoint Correlation',
                    selected: 1,
                    weight: 50
                }, {
                    name: 'Originator Correlation',
                    selected: 1,
                    weight: 50
                }, {
                    name: 'Data Type Correlation',
                    selected: 1,
                    weight: 50
                }, {
                    name: 'Data Value Correlation',
                    selected: 1,
                    weight: 50
                }],
                maximumDistance: 5,
                nrootradical:2,

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
            selectTypes(type) {
                this.selectedType = type;
            },
            async saveConfig() {
                await metrics({
                    value: '1'
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
        background-color: #d9d9d9;

    }
    .process-graph-view{
        height: 560px;
        border-color: #dcdfe6;
        overflow: scroll;
    }
    .button-position{

        position: relative;
        top:20px;
        border-radius: 2px;
        border-color: #606266;
        color: #606266;;
    }


</style>
