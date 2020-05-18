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

                    <el-button type="primary" plain class="button-position">Save Snapshot</el-button>


                </div>
            </el-col>
            <el-col :span="8">
                <div class="model-view">
                    <h3 class="text-center-align">Configurations</h3>
                    <el-row :gutter="10" class="el-tabs--border-card filter-container">
                        <el-col :span="8" class="grid-content-configuration el-table--border">
                            <h4 class="text-center-align">Node Filter</h4>
                              <el-divider></el-divider>
                            <div class="slider-adjustment1 text-center-align">
                            <label>Significance Cutoff</label>
                                <el-slider align="middle" vertical v-model="node" height="280px" @change="nodeChanged" />
                                <label> {{ node / 100 }}</label>
                            </div>
                        </el-col>
                        <el-col :span="8" class="grid-content-configuration el-table--border">
                            <h4 class="text-center-align">Edge Filter</h4>
                            <el-divider></el-divider>
                            <label>Edge Transformer</label>
                            <el-radio-group v-model="edge" style="position: relative; top:10px;">
                                <el-radio :label="1">Best Edges</el-radio>
                                <el-radio :label="2">Fuzzy Edges</el-radio>
                            </el-radio-group>
                            <el-row :gutter="2" class="slider-adjustment2">
                                <el-col :span="14" align="middle">
                                    <label>S/C Ratio</label>
                                    <el-slider vertical v-model="sc" height="280px" @change="scChanged"/>
                                    <label>{{ sc / 100 }}</label>
                                </el-col>
                                <el-col :span="4" align="middle">
                                    <label>Cutoff</label>
                                    <el-slider vertical v-model="cutoff" height="280px" @change="cutoffChanged"/>
                                    <label>{{ cutoff / 100 }}</label>
                                </el-col>
                            </el-row>
                            <div style="position: relative;top:60px;">
                            <el-checkbox v-model="loops">Ignore Self-Loops</el-checkbox>
                            <el-checkbox v-model="absolute">Interpret Absolute</el-checkbox>
                                </div>
                        </el-col>
                        <el-col :span="8" class="grid-content-configuration el-table--border">
                            <div class="">
                            <h4 class="text-center-align">Concurrency Filter</h4>
                                  <el-divider></el-divider>
                            <el-checkbox v-model="concurrency">Filter Concurrency</el-checkbox>
                                <el-row :gutter="20" class="slider-adjustment3">
                                    <el-col :span="10" align="middle">
                                        <label>Preserve</label>
                                        <el-slider vertical v-model="preserve" height="280px"
                                                   @change="preserveChanged"/>
                                        <label>{{ preserve / 100 }}</label>
                                    </el-col>
                                    <el-col :span="10" align="middle">
                                        <label>Balance</label>
                                        <el-slider vertical v-model="balance" height="280px" @change="balanceChanged"/>
                                        <label>{{ balance / 100 }}</label>
                                    </el-col>

                                </el-row>
                        </div>
                        </el-col>
                    </el-row>
                    <div class="text-center-align metrics">
                        <el-button type="primary" plain class="button-position" @click="openConfig">Metrics
                            Configuration
                        </el-button>
                    </div>
                </div>
            </el-col>
        </el-row>
        <el-dialog
                title="Configure"
                :visible.sync="dialog"
                width="40%" style="font-family: Arial, Helvetica, sans-serif">
            <div>
                <el-tabs type="border-card">
                    <el-tab-pane label="Metrics">
                        <el-dropdown @command="selectTypes">
                            <span class="el-dropdown-link">
                                Select Metrics<i class="el-icon-arrow-down el-icon--left"></i>
                            </span>
                            <el-dropdown-menu slot="dropdown">
                                <el-dropdown-item command="unary">Unary Metrics</el-dropdown-item>
                                <el-dropdown-item command="significance" divided>Binary Significance</el-dropdown-item>
                                <el-dropdown-item command="correlation" divided>Binary Correlation</el-dropdown-item>
                            </el-dropdown-menu>
                        </el-dropdown>
                        <span>{{ " Metrics Selected : "+typeLabels[selectedType] }}</span>
                        <div v-if="selectedType === 'unary'">
                            <el-divider></el-divider>
                            <div>
                                <h4>Frequency Significance Metric</h4>
                                <div style="display: flex">
                                    <el-checkbox v-model="unaryFrequencyActive">Include</el-checkbox>
                                    <el-checkbox v-model="unaryFrequencySignificance">Invert the significance
                                    </el-checkbox>
                                </div>
                                <br>
                                <div class="horizontal-align">
                                    <label class="slider-label">Weight</label>
                                    <el-slider class="adjust-slider-width" v-model="unaryFrequencyWeight"/>
                                </div>

                            </div>
                            <el-divider></el-divider>
                            <div>
                                <h4>Routing Significance</h4>
                                <div style="display: table-cell">
                                    <el-checkbox v-model="routingActive">Include</el-checkbox>
                                    <el-checkbox v-model="routingSignificance">Invert the significance</el-checkbox>
                                </div>
                                <br>
                                <div class="horizontal-align">
                                    <label class="slider-label">Weight </label>
                                    <el-slider class="adjust-slider-width" v-model="routingWeight"/>
                                </div>
                            </div>
                        </div>
                        <div v-else-if="selectedType === 'significance'">
                            <el-divider></el-divider>
                            <div>
                                <h4>Frequency Significance Metric</h4>
                                <div style="display: flex">
                                    <el-checkbox v-model="binaryFrequencyActive">Include</el-checkbox>
                                    <el-checkbox v-model="binaryFrequencySignificance">Invert the significance
                                    </el-checkbox>
                                </div>
                                <br>
                                <div class="horizontal-align">
                                <label class="slider-label">Weight</label>
                                <el-slider class="adjust-slider-width" v-model="binaryFrequencyWeight"/>
                                </div>
                            </div>
                            <el-divider></el-divider>
                            <div>
                                <h4>Distance Significance</h4>
                                <div style="display: flex">
                                    <el-checkbox v-model="distanceActive">Include</el-checkbox>
                                    <el-checkbox v-model="distanceSignificance">Invert the significance</el-checkbox>
                                </div>
                                <br>
                                <div class="horizontal-align">
                                <label class="slider-label">Weight</label>
                                <el-slider class="adjust-slider-width" v-model="distanceWeight"/>
                                </div>
                            </div>
                        </div>
                        <div v-else>
                            <div v-for="(item, index) in binaryCorrelation" :key="index">
                                <el-divider></el-divider>
                                <h4>{{ item.name }}</h4>
                                <div style="display: flex">
                                    <el-checkbox v-model="item.active">Include</el-checkbox>
                                    <el-checkbox v-model="item.significance">Invert the significance</el-checkbox>
                                </div>
                                <br>
                                <div class="horizontal-align">
                                <label class="slider-label">Weight</label>
                                <el-slider class="adjust-slider-width" v-model="item.weight"/>
                                </div>
                            </div>
                        </div>
                    </el-tab-pane>
                    <el-tab-pane label="Attenuation">
                        <div>
                            <label>Maximal event distance</label>
                            <el-slider v-model="maximumEventDistance" :min="1" :max="20" />
                        </div>
                        <el-divider></el-divider>
                        <div>
                            <h4>Select Attenuation</h4>
                            <el-radio-group v-model="attenuationSelected">
                                <el-radio :label="1">Linear Attenuation</el-radio>
                                <br>
                                <el-radio :label="2">N(th) root with radical</el-radio>
                            </el-radio-group>
                            <div v-if="attenuationSelected===2">
                                <el-slider v-model="radical" :min="1" :max="4"/>
                            </div>
                        </div>
                    </el-tab-pane>
                </el-tabs>
            </div>
            <el-divider></el-divider>
            <div slot="footer" class="dialog-footer">
                <el-button @click="saveConfig">Save</el-button>
                <el-button @click="cancelConfig">Cancel</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    import {concurrencyFilter, edgeFilter, metrics, nodeFilter} from '@/api/filter';

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
                typeLabels: {
                    'unary': 'Unary Metrics',
                    'significance': 'Binary Significance',
                    'correlation': 'Binary Correlation'
                },
                selectedType: 'unary',
                unaryFrequencyActive: true,
                unaryFrequencySignificance: false,
                unaryFrequencyWeight: 50,
                routingActive: true,
                routingSignificance: false,
                routingWeight: 50,
                binaryFrequencyActive: true,
                binaryFrequencySignificance: false,
                binaryFrequencyWeight: 50,
                distanceActive: true,
                distanceSignificance: false,
                distanceWeight: 50,
                binaryCorrelation: [{
                    name: 'Proximity Correlation',
                    active: true,
                    significance: false,
                    weight: 50
                }, {
                    name: 'Endpoint Correlation',
                    active: true,
                    significance: false,
                    weight: 50
                }, {
                    name: 'Originator Correlation',
                    active: true,
                    significance: false,
                    weight: 50
                }, {
                    name: 'Data Type Correlation',
                    active: true,
                    significance: false,
                    weight: 50
                }, {
                    name: 'Data Value Correlation',
                    active: true,
                    significance: false,
                    weight: 50
                }],
                maximumEventDistance: 5,
                attenuationSelected: 2,
                radical: 2,
                metrics_save: {}
            }
        },
        methods: {
            async nodeChanged(value) {
                await nodeFilter({
                    'cutoff': value / 100
                });
                console.log('change node filter with cutoff: ' + String(value / 100));
            },
            async scChanged(value) {
                let edge = 'Best Edges';
                if (this.edge === 2) {
                    edge = 'Fuzzy Edges';
                }
                await edgeFilter({
                    'edge_transformer': edge,
                    's/c_ratio': value / 100,
                    'cutoff': this.cutoff / 100,
                    'ignore_self_loops': this.loops,
                    'interpret_absolute': this.absolute
                });
                console.log('change edge filter with s/c ratio: ' + String(value / 100));
            },
            async cutoffChanged(value) {
                let edge = 'Best Edges';
                if (this.edge === 2) {
                    edge = 'Fuzzy Edges';
                }
                await edgeFilter({
                    'edge_transformer': edge,
                    's/c_ratio': this.sc / 100,
                    'cutoff': value / 100,
                    'ignore_self_loops': this.loops,
                    'interpret_absolute': this.absolute
                });
                console.log('change edge filter with cutoff: ' + String(value / 100));
            },
            async preserveChanged(value) {
                await concurrencyFilter({
                    'filter_concurrency': this.concurrency,
                    'preserve': value / 100,
                    'balance': this.balance / 100
                });
                console.log('change concurrency filter with preserve: ' + String(value / 100));
            },
            async balanceChanged(value) {
                await concurrencyFilter({
                    'filter_concurrency': this.concurrency,
                    'preserve': this.preserve / 100,
                    'balance': value / 100
                });
                console.log('change concurrency filter with balance: ' + String(value / 100));
            },
            selectTypes(type) {
                this.selectedType = type;
            },
            openConfig() {
                this['dialog'] = true;
                // JSON.parse(JSON.stringify(obj));
                this.metrics_save['selectedType'] = this.selectedType;
                this.metrics_save['unaryFrequencyActive'] = this.unaryFrequencyActive;
                this.metrics_save['unaryFrequencySignificance'] = this.unaryFrequencySignificance;
                this.metrics_save['unaryFrequencyWeight'] = this.unaryFrequencyWeight;
                this.metrics_save['routingActive'] = this.routingActive;
                this.metrics_save['routingSignificance'] = this.routingSignificance;
                this.metrics_save['routingWeight'] = this.routingWeight;
                this.metrics_save['binaryFrequencyActive'] = this.binaryFrequencyActive;
                this.metrics_save['binaryFrequencySignificance'] = this.binaryFrequencySignificance;
                this.metrics_save['binaryFrequencyWeight'] = this.binaryFrequencyWeight;
                this.metrics_save['distanceActive'] = this.distanceActive;
                this.metrics_save['distanceSignificance'] = this.distanceSignificance;
                this.metrics_save['distanceWeight'] = this.distanceWeight;
                this.metrics_save['binaryCorrelation'] = [];
                this.binaryCorrelation.forEach(item => {
                    let temp = {};
                    for (let [key, value] in Object.entries(item)) {
                        temp[key] = value;
                    }
                    this.metrics_save['binaryCorrelation'] = temp;
                });
                this.metrics_save['maximumEventDistance'] = this.maximumEventDistance;
                this.metrics_save['attenuationSelected'] = this.attenuationSelected;
                this.metrics_save['radical'] = this.radical;
            },
            async saveConfig() {
                let data = {};
                const type = this.typeLabels[this.selectedType];
                data['metrics'] = {};
                data['metrics']['metrics_type'] = type;
                if (type === this.typeLabels['unary']) {
                    data['metrics']['frequency'] = this.unaryFrequencyActive;
                    data['metrics']['frequency_invert'] = this.unaryFrequencySignificance;
                    data['metrics']['frequency_wight'] = this.unaryFrequencyWeight / 100;
                    data['metrics']['routing'] = this.routingActive;
                    data['metrics']['routing_invert'] = this.routingSignificance;
                    data['metrics']['routing_weight'] = this.routingWeight / 100;
                } else if (type === this.typeLabels['significance']) {
                    data['metrics']['frequency'] = this.binaryFrequencyActive;
                    data['metrics']['frequency_invert'] = this.binaryFrequencySignificance;
                    data['metrics']['frequency_weight'] = this.binaryFrequencyWeight;
                    data['metrics']['distance'] = this.distanceActive;
                    data['metrics']['distance_invert'] = this.distanceSignificance;
                    data['metrics']['distance_weight'] = this.distanceWeight / 100;
                } else {
                    data['metrics']['correlation'] = [];
                    this.binaryCorrelation.forEach(item => {
                        data['metrics']['correlation'].push(item);
                    });
                }
                data['attenuation'] = {};
                data['attenuation']['maximal_event_distance'] = this.maximumEventDistance / 100;
                if (this.attenuationSelected === 1) {
                    data['attenuation']['selected'] = 'Linear Attenuation';
                } else {
                    data['attenuation']['selected'] = 'N root with radical';
                    data['attenuation']['radical'] = this.radical;
                }
                await metrics(data);
                this.dialog = false;
            },
            cancelConfig() {
                for (let [key, value] in Object.entries(this.metrics_save)) {
                    if (key !== 'binaryCorrelation')
                        this[key] = value;
                }
                this.binaryCorrelation = this.metrics_save['binaryCorrelation'];
                this.metrics_save = {};
                this.dialog = false;
            }
        },
        watch: {
            edge: async function(now, old) {
                if (now === old)
                    return;
                let edge = 'Best Edges';
                if (now === 2)
                    edge = 'Fuzzy Edges';
                await edgeFilter({
                    'edge_transformer': edge,
                    's/c_ratio': this.sc / 100,
                    'cutoff': this.cutoff / 100,
                    'ignore_self_loops': this.loops,
                    'interpret_absolute': this.absolute
                });
                console.log('change edge filter with edge transformer: ' + edge);
            },
            loops: async function (now, old) {
                if (now === old)
                    return;
                let edge = 'Best Edges';
                if (this.edge === 2)
                    edge = 'Fuzzy Edges';
                await edgeFilter({
                    'edge_transformer': edge,
                    's/c_ratio': this.sc / 100,
                    'cutoff': this.cutoff / 100,
                    'ignore_self_loops': now,
                    'interpret_absolute': this.absolute
                });
                console.log('change edge filter with ignore self-loops: ' + String(now));
            },
            absolute: async function(now, old) {
                if (now === old)
                    return;
                let edge = 'Best Edges';
                if (this.edge === 2)
                    edge = 'Fuzzy Edges';
                await edgeFilter({
                    'edge_transformer': edge,
                    's/c_ratio': this.sc / 100,
                    'cutoff': this.cutoff / 100,
                    'ignore_self_loops': this.loops,
                    'interpret_absolute': now
                });
                console.log('change edge filter with interpret absolute: ' + String(now));
            },
            concurrency: async function (now, old) {
                if (now === old)
                    return;
                await concurrencyFilter({
                    'filter_concurrency': now,
                    'preserve': this.preserve / 100,
                    'balance': this.balance / 100
                });
                console.log('change concurrency filter with filter concurrency: ' + String(now));
            },
        }
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
        height:570px;
       border-color: #f0f0f0;

    }

    .grid-content{
        height: inherit;
        background-color: #d9d9d9;

    }
    .grid-content-configuration{
        height: inherit;
        border-color: #d9d9d9;
    }
    .process-graph-view{
        height: 570px;
        border-color: #dcdfe6;
        overflow: scroll;
    }

    .button-position {

        position: relative;
        top: 20px;
        border-radius: 2px;


    }

    .slider-adjustment1 {
        position: relative;
        top: 70px;
    }

    .slider-adjustment2 {
        position: relative;
        top: 20px;
    }

    .slider-adjustment3 {
        position: center;
        top: 52px;
    }

    .el-dropdown-link {
        cursor: pointer;
        color: #409EFF;
        margin-bottom: 20px;

    }

    .el-icon-arrow-down {
        font-size: 12px;

    }

    .adjust-slider-width {
        width: 90%;

    }

    .slider-label {
        position: relative;
        top: 10px;
    }

    .horizontal-align {
        display: flex;
        justify-content: space-evenly;
    }


</style>
