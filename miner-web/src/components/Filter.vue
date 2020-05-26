<template>
    <div class="page-layout" style="overflow: hidden">
        <el-row :gutter="10">
            <el-col :span="16" align="middle">
                <div class="model-view">
                    <h3 class="text-center-align">Fuzzy Model</h3>
                    <div class="el-tabs--border-card grid-content process-graph-view">
                        <img :src="image" alt=""/>
                    </div>
                    <el-button type="primary" plain class="button-position">Save Snapshot</el-button>
                </div>
            </el-col>
            <el-col :span="8">
                <div class="model-view">
                    <h3 class="text-center-align">Configurations</h3>
                    <el-row :gutter="10" class="el-tabs--border-card filter-container">
                        <el-col :span="8" class="grid-content-configuration el-table--border">
                            <h4>Node Filter</h4>
                              <el-divider></el-divider>
                            <div class="slider-adjustment1 text-center-align">
                            <label>Significance Cutoff</label>
                                <el-slider align="middle" vertical v-model="node" height="280px" :format-tooltip="slider_format" @change="nodeChanged" />
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
                                    <el-slider vertical v-model="sc" height="280px" :disabled="edge === 1" :format-tooltip="slider_format" @change="scChanged"/>
                                    <label>{{ sc / 100 }}</label>
                                </el-col>
                                <el-col :span="4" align="middle">
                                    <label>Cutoff</label>
                                    <el-slider vertical v-model="cutoff" height="280px" :disabled="edge === 1" :format-tooltip="slider_format" @change="cutoffChanged"/>
                                    <label>{{ cutoff / 100 }}</label>
                                </el-col>
                            </el-row>
                            <div style="position: relative;top:60px;">
                                <el-checkbox v-model="loops" :disabled="edge === 1">Ignore Self-Loops</el-checkbox>
                                <el-checkbox v-model="absolute" :disabled="edge === 1">Interpret Absolute</el-checkbox>
                            </div>
                        </el-col>
                        <el-col :span="8" class="grid-content-configuration el-table--border">

                            <h4 class="text-center-align">Concurrency Filter</h4>
                            <el-divider></el-divider>
                            <el-checkbox v-model="concurrency"><label style="color: black">Filter Concurrency</label>
                            </el-checkbox>
                            <el-row :gutter="20" type="flex" justify="center" class="text-center-align">
                                <el-col :span="10">
                                    <label>Preserve</label>
                                    <el-slider vertical v-model="preserve" height="280px" :disabled="!concurrency"
                                               :format-tooltip="slider_format"
                                               @change="preserveChanged"/>
                                    <label>{{ preserve / 100 }}</label>
                                </el-col>
                                <el-col :span="10">
                                    <label>Balance</label>
                                    <el-slider vertical v-model="balance" height="280px" :disabled="!concurrency"
                                               :format-tooltip="slider_format" @change="balanceChanged"/>
                                    <label>{{ balance / 100 }}</label>
                                </el-col>

                            </el-row>

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
                append-to-body="false"
                width="40%" style="font-family: Arial, Helvetica, sans-serif;">
            <div>
                <el-tabs type="border-card">
                    <el-tab-pane label="Metrics" class="el-tabs__content">
                        <el-cascader v-model="selectedType" :options="selectTypes"></el-cascader>
                        <div v-if="selectedType[0] === 'binarySignificance'">
                            <div v-for="(value, key, index) in metricsConfig.metrics.binarySignificance"
                                 :key="index">
                                <el-divider></el-divider>
                                <div>
                                    <h4>{{ value.label }}</h4>
                                    <div style="display: flex">
                                        <el-checkbox v-model="value.inc">Include</el-checkbox>
                                        <el-checkbox v-model="value.invert">Invert the significance</el-checkbox>
                                    </div>
                                    <br>
                                    <div class="horizontal-align">
                                        <label class="slider-label">Weight</label>
                                        <el-slider class="adjust-slider-width" v-model="value.weight"
                                                   :format-tooltip="slider_format"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-else-if="selectedType[0] === 'binaryCorrelation'">
                            <div v-for="(value, key, index) in metricsConfig.metrics.binaryCorrelation"
                                 :key="index">
                                <el-divider></el-divider>
                                <h4>{{ value.label }}</h4>
                                <div style="display: flex">
                                    <el-checkbox v-model="value.inc">Include</el-checkbox>
                                    <el-checkbox v-model="value.invert">Invert the significance</el-checkbox>
                                </div>
                                <br>
                                <div class="horizontal-align">
                                    <label class="slider-label">Weight</label>
                                    <el-slider class="adjust-slider-width" v-model="value.weight"
                                               :format-tooltip="slider_format"/>
                                </div>
                            </div>
                        </div>
                        <div v-else>
                            <div v-for="(value, key, index) in metricsConfig.metrics.unary" :key="index">
                                <el-divider></el-divider>
                                <div>
                                    <h4>{{ value.label }}</h4>
                                    <div style="display: flex">
                                        <el-checkbox v-model="value.inc">Include</el-checkbox>
                                        <el-checkbox v-model="value.invert">Invert the significance</el-checkbox>
                                    </div>
                                    <br>
                                    <div class="horizontal-align">
                                        <label class="slider-label">Weight</label>
                                        <el-slider class="adjust-slider-width" v-model="value.weight"
                                                   :format-tooltip="slider_format"/>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </el-tab-pane>
                    <el-tab-pane label="Attenuation">
                        <div>
                            <label>Maximal event distance</label>
                            <el-slider v-model="metricsConfig.attenuation.eventDistance" :min="1" :max="20" />
                        </div>
                        <el-divider></el-divider>
                        <div>
                            <h4>Select Attenuation</h4>
                            <el-radio-group v-model="metricsConfig.attenuation.seleted">
                                <el-radio :label="1">Linear Attenuation</el-radio>
                                <br>
                                <el-radio :label="2">N(th) root with radical</el-radio>
                            </el-radio-group>
                            <el-slider v-model="metricsConfig.attenuation.radical"
                                       :disabled="metricsConfig.attenuation.seleted === 1" :min="1" :max="4"
                                       step="0.01"/>
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
        <el-dialog
            title="Loading"
            :visible="progress"
            width="25%">
            <el-progress type="line" :percentage="percentage"></el-progress>
            <i class="el-icon-loading" />
            <label v-if="percentage === 100">Please hold on, the server is running.</label>
        </el-dialog>
    </div>
</template>

<script>
    import {generate} from "@/api/home";
    import {concurrencyFilter, edgeFilter, metrics, nodeFilter} from '@/api/filter';

    export default {
        name: "Filter",
        data() {
            return {
                image: '',
                progress: false,
                percentage: 0,
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
                    'binarySignificance': 'Binary Significance',
                    'binaryCorrelation': 'Binary Correlation'
                },
                selectedType: 'unary',
                metricsConfig: {
                    metrics: {
                        unary: {
                            frequency: {
                                label: 'Frequency Significance Metric',
                                inc: true,
                                invert: false,
                                weight: 50
                            },
                            routing: {
                                label: 'Routing Significance',
                                inc: true,
                                invert: false,
                                weight: 50
                            }
                        },
                        binarySignificance: {
                            frequency: {
                                label: 'Frequency Significance Metric',
                                inc: true,
                                invert: false,
                                weight: 50
                            },
                            distance: {
                                label: 'Distance Significance',
                                inc: true,
                                invert: false,
                                weight: 50
                            }
                        },
                        binaryCorrelation: {
                            proximity: {
                                label: 'Proximity Correlation',
                                inc: true,
                                invert: false,
                                weight: 50
                            },
                            endpoint: {
                                label: 'Endpoint Correlation',
                                inc: true,
                                invert: false,
                                weight: 50
                            },
                            originator: {
                                label: 'Originator Correlation',
                                inc: true,
                                invert: false,
                                weight: 50
                            },
                            dataType: {
                                label: 'Data Type Correlation',
                                inc: true,
                                invert: false,
                                weight: 50
                            },
                            dataValue: {
                                label: 'Data Value Correlation',
                                inc: true,
                                invert: false,
                                weight: 50
                            }
                        },
                    },
                    attenuation: {
                        eventDistance: 5,
                        seleted: 2,
                        radical: 2
                    }
                },
                metrics_save: {},
                value: [],
                selectTypes: [{
                    value: 'unary',
                    label: 'Unary Metrics'
                }, {
                    value: 'binarySignificance',
                    label: 'Binary Metrics'
                }, {
                        value: 'binaryCorrelation',
                        label: 'Binary Correlation'
                }]
            }
        },
        methods: {
            slider_format(value) {
                return value / 100;
            },
            progressing() {
                this.progress = true;
                this.percentage = 0;
                let obj = setInterval(() => {
                    this.percentage += 1;
                    if (this.percentage >= 100 || this.progress === false)
                        clearInterval(obj);
                }, 300);
            },
            async nodeChanged(value) {
                this.progressing();
                const { data } = await nodeFilter({
                    'cutoff': value / 100
                });
                console.log('change node filter with cutoff: ' + String(value / 100));
                this.image = data;
                this.progress = false;
            },
            async scChanged(value) {
                this.progressing();
                const { data } = await edgeFilter({
                    'edge_transformer': 'Fuzzy Edges',
                    's/c_ratio': value / 100,
                    'cutoff': this.cutoff / 100,
                    'ignore_self_loops': this.loops,
                    'interpret_absolute': this.absolute
                });
                console.log('change edge filter with s/c ratio: ' + String(value / 100));
                this.image = data;
                this.progress = false;
            },
            async cutoffChanged(value) {
                this.progressing();
                const { data } = await edgeFilter({
                    'edge_transformer': 'Fuzzy Edges',
                    's/c_ratio': this.sc / 100,
                    'cutoff': value / 100,
                    'ignore_self_loops': this.loops,
                    'interpret_absolute': this.absolute
                });
                console.log('change edge filter with cutoff: ' + String(value / 100));
                this.image = data;
                this.progress = false;
            },
            async preserveChanged(value) {
                this.progressing();
                const { data } = await concurrencyFilter({
                    'filter_concurrency': this.concurrency,
                    'preserve': value / 100,
                    'balance': this.balance / 100
                });
                console.log('change concurrency filter with preserve: ' + String(value / 100));
                this.image = data;
                this.progress = false;
            },
            async balanceChanged(value) {
                this.progressing();
                const { data } = await concurrencyFilter({
                    'filter_concurrency': this.concurrency,
                    'preserve': this.preserve / 100,
                    'balance': value / 100
                });
                console.log('change concurrency filter with balance: ' + String(value / 100));
                this.image = data;
                this.progress = false;
            },
            selectTypes(value) {
                this.selectedType = value;
            },
            openConfig() {
                this.dialog = true;
                // JSON.parse(JSON.stringify(obj));
            },
            async saveConfig() {
                let req = {
                    metrics: {
                        unary_metrics: {
                            frequency: {
                                include: this.metricsConfig.metrics.unary.frequency.inc,
                                invert: this.metricsConfig.metrics.unary.frequency.invert,
                                weight: this.metricsConfig.metrics.unary.frequency.weight / 100
                            },
                            routing: {
                                include: this.metricsConfig.metrics.unary.routing.inc,
                                invert: this.metricsConfig.metrics.unary.routing.invert,
                                weight: this.metricsConfig.metrics.unary.routing.weight / 100
                            }
                        },
                        binary_significance: {
                            frequency: {
                                include: this.metricsConfig.metrics.binarySignificance.frequency.inc,
                                invert: this.metricsConfig.metrics.binarySignificance.frequency.invert,
                                weight: this.metricsConfig.metrics.binarySignificance.frequency.weight / 100
                            },
                            distance: {
                                include: this.metricsConfig.metrics.binarySignificance.distance.inc,
                                invert: this.metricsConfig.metrics.binarySignificance.distance.invert,
                                weight: this.metricsConfig.metrics.binarySignificance.distance.weight / 100
                            }
                        },
                        binary_correlation: {
                            proximity: {
                                include: this.metricsConfig.metrics.binaryCorrelation.proximity.inc,
                                invert: this.metricsConfig.metrics.binaryCorrelation.proximity.invert,
                                weight: this.metricsConfig.metrics.binaryCorrelation.proximity.weight / 100
                            },
                            endpoint: {
                                include: this.metricsConfig.metrics.binaryCorrelation.endpoint.inc,
                                invert: this.metricsConfig.metrics.binaryCorrelation.endpoint.invert,
                                weight: this.metricsConfig.metrics.binaryCorrelation.endpoint.weight / 100
                            },
                            originator: {
                                include: this.metricsConfig.metrics.binaryCorrelation.originator.inc,
                                invert: this.metricsConfig.metrics.binaryCorrelation.originator.invert,
                                weight: this.metricsConfig.metrics.binaryCorrelation.originator.weight / 100
                            },
                            data_type: {
                                include: this.metricsConfig.metrics.binaryCorrelation.dataType.inc,
                                invert: this.metricsConfig.metrics.binaryCorrelation.dataType.invert,
                                weight: this.metricsConfig.metrics.binaryCorrelation.dataType.weight / 100
                            },
                            data_value: {
                                include: this.metricsConfig.metrics.binaryCorrelation.dataValue.inc,
                                invert: this.metricsConfig.metrics.binaryCorrelation.dataValue.invert,
                                weight: this.metricsConfig.metrics.binaryCorrelation.dataValue.weight / 100
                            }
                        }
                    },
                    attenuation: {
                        maximal_event_distance: this.metricsConfig.attenuation.eventDistance,
                    }
                };
                if (this.metricsConfig.attenuation.seleted === 1) {
                    req.attenuation.selected = 'Linear Attenuation';
                } else {
                    req.attenuation.selected = 'N root with radical';
                    req.attenuation.radical = this.radical/100;
                }
                this.progressing();
                const { data } = await metrics(req);
                this.image = data;
                this.dialog = false;
                this.progress = false;
            },
            cancelConfig() {
                this.metrics_save = {};
                this.dialog = false;
            },
            async loading() {
                this.progressing();
                const path = this.$route.params.path;
                const { data } = await generate({path: path});
                this.progress = false;
                console.log(data);
            }
        },
        watch: {
            edge: async function(now, old) {
                this.progressing();
                let resp;
                if (now === old)
                    return;
                if (now === 1) {
                    resp =await edgeFilter({
                        'edge_transformer': 'Best Edges'
                    });
                } else {
                    resp = await edgeFilter({
                        'edge_transformer': 'Fuzzy Edges',
                        's/c_ratio': this.sc / 100,
                        'cutoff': this.cutoff / 100,
                        'ignore_self_loops': this.loops,
                        'interpret_absolute': this.absolute
                    });
                }
                console.log('change edge filter with edge transformer: ' + now);
                this.image = resp.data;
                this.progress = false;
            },
            loops: async function (now, old) {
                this.progressing();
                if (now === old)
                    return;
                const { data } = await edgeFilter({
                    'edge_transformer': 'Fuzzy Edges',
                    's/c_ratio': this.sc / 100,
                    'cutoff': this.cutoff / 100,
                    'ignore_self_loops': now,
                    'interpret_absolute': this.absolute
                });
                console.log('change edge filter with ignore self-loops: ' + String(now));
                this.image = data;
                this.progress = false;
            },
            absolute: async function(now, old) {
                this.progressing();
                if (now === old)
                    return;
                const { data } = await edgeFilter({
                    'edge_transformer': 'Fuzzy Edges',
                    's/c_ratio': this.sc / 100,
                    'cutoff': this.cutoff / 100,
                    'ignore_self_loops': this.loops,
                    'interpret_absolute': now
                });
                console.log('change edge filter with interpret absolute: ' + String(now));
                this.image = data;
                this.progress = false;
            },
            concurrency: async function (now, old) {
                this.progressing();
                if (now === old)
                    return;
                const { data } = await concurrencyFilter({
                    'filter_concurrency': now,
                    'preserve': this.preserve / 100,
                    'balance': this.balance / 100
                });
                console.log('change concurrency filter with filter concurrency: ' + String(now));
                this.image = data;
                this.progress = false;
            },
        },
        created() {
            this.loading();
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
        top:20px;
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
        width: 80%;

    }

    .slider-label {
        position: relative;
        top: 10px;
        width: 16%;
        padding-left: 2px;
    }

    .horizontal-align {
        display: flex;
        justify-content: left;
    }

    .el-tabs__content {
        overflow-y: scroll;
        position: relative;
        height: 300px;
    }



</style>
