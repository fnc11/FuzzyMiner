<template>
    <div class="page-layout" style="overflow: hidden">
        <el-row :gutter="10">
            <el-col :xl="16" :lg="16" :md="12" :sm="14" :xs="10" align="middle">
                <div class="model-view">
                    <h3 class="text-center-align">Fuzzy Model</h3>
                    <div class="el-tabs--border-card grid-content process-graph-view">

                        <viewer id="viewer" :images="images" @inited="inited">
                            <img v-for="(item, index) in images" :src="item" :key="index">
                        </viewer>
                    </div>
                    <el-button type="primary" plain class="button-position" @click="downloadImage">Save
                        Snapshot
                    </el-button>
                </div>
            </el-col>
            <el-col :xl="8" :lg="8" :md="12" :sm="10" :xs="10">
                <div class="model-view-conf">
                    <h3 class="text-center-align">Filter Configurations</h3>
                    <el-row :gutter="10" class="el-tabs--border-card filter-container"
                            style="overflow-wrap: break-spaces">
                        <el-col :xl="8" :lg="8" :md="6" :sm="6" :xs="6"
                                class="text-center-align grid-content-configuration el-table--border">
                            <h4 class="text-center-align">Node</h4>
                            <el-divider style="position:relative;top:10vh"></el-divider>
                            <div class="slider-adjustment1">
                                <h5>Significance Cutoff</h5>
                                <el-slider align="middle" vertical v-model="node" height="30vh"
                                           @change="nodeChanged" :min="0.0" :max="1.0" :step="0.001"/>
                                <label> {{ node }}</label>
                            </div>
                        </el-col>
                        <el-col :xl="8" :lg="8" :md="9" :sm="9" :xs="9"
                                class="grid-content-configuration el-table--border">
                            <h4 class="text-center-align">Edge</h4>
                            <el-divider class="hidden-sm-and-down"></el-divider>
                            <el-radio-group v-model="edge">
                                <el-radio :label="1" style="color: black;">Best Edges</el-radio>
                                <el-radio :label="2" style="color: black;">Fuzzy Edges</el-radio>
                            </el-radio-group>
                            <div align="center" style="position: relative;top:6px;">
                                <el-checkbox class="el-checkbox__label1" v-model="absolute" :disabled="edge === 1"
                                             style="font-size: 8px;">Interpret Absolute
                                </el-checkbox>
                            </div>
                            <div class="slider-adjustment2">
                                <div align="center">
                                    <h5>Preserve</h5>
                                    <el-slider vertical v-model="cutoff" height="30vh" :disabled="edge === 1"
                                               @change="cutoffChanged" :min="0.001" :max="1.0" :step="0.001"/>
                                    <label>{{ cutoff }}</label>
                                </div>
                                <div align="center">
                                    <h5>S/C Ratio</h5>
                                    <el-slider vertical v-model="sc" height="30vh" :disabled="edge === 1"
                                               @change="scChanged" :min="0.0" :max="1.0" :step="0.001"/>
                                    <label>{{ sc }}</label>
                                </div>
                            </div>
                            <div style="position:relative;top:2vh;">
                                <el-checkbox class="el-checkbox__label" v-model="loops">Ignore Self-Loops</el-checkbox>
                            </div>
                        </el-col>
                        <el-col :xl="8" :lg="8" :md="9" :sm="9" :xs="9"
                                class="grid-content-configuration el-table--border">

                            <h4 class="text-center-align">Concurrency</h4>
                            <el-divider></el-divider>
                            <el-checkbox v-model="concurrency" align="left">
                                <label style="color: black">Filter Concurrency</label>

                            </el-checkbox>
                            <div class="slider-adjustment3">
                                <div align="center">
                                    <h5>Preserve</h5>
                                    <el-slider vertical v-model="preserve" height="30vh" :disabled="!concurrency"
                                               @change="preserveChanged"
                                               :min="0.0" :max="1.0" :step="0.01" :format-tooltip="() => { return Math.pow(this.preserve, 4).toFixed(3); }" />
                                    <label>{{ concurrencyPreserve }}</label>
                                </div>
                                <div align="center">
                                    <h5>Balance</h5>
                                    <el-slider vertical v-model="balance" height="30vh" :disabled="!concurrency"
                                               @change="balanceChanged"
                                               :min="0.0" :max="1.0" :step="0.001"/>
                                    <label>{{ balance }}</label>
                                </div>
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
                append-to-body="false"
                width="40vw" style="font-family: Arial, Helvetica, sans-serif;">
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
                                                   :min="0.0" :max="1.0" :step="0.01"/>
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
                                               :min="0.0" :max="1.0" :step="0.01"/>
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
                                                   :min="0.0" :max="1.0" :step="0.01"/>
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
                                       :step="0.01"/>
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
            :visible.sync="progress"
            width="25%">
            <el-progress type="line" :percentage="percentage"></el-progress>
            <i class="el-icon-loading" />
            <label v-if="percentage === 100">Please hold on, the server is running.</label>
        </el-dialog>
    </div>
</template>

<script>
    import Axios from 'axios';
    import {generate} from "@/api/home";
    import {concurrencyFilter, edgeFilter, metrics, nodeFilter} from '@/api/filter';

    export default {
        name: "Filter",
        data() {
            return {
                selectedImage: '',
                images: [],
                progress: false,
                percentage: 0,
                node: 0,
                edge: 2,
                sc: 0.75,
                cutoff: 0.2,
                preserve: 0.8801117368,
                balance: 0.7,
                loops: true,
                absolute: false,
                concurrency: true,
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
                                label: 'Frequency Significance',
                                inc: true,
                                invert: false,
                                weight: 0.5
                            },
                            routing: {
                                label: 'Routing Significance',
                                inc: true,
                                invert: false,
                                weight: 0.5
                            }
                        },
                        binarySignificance: {
                            frequency: {
                                label: 'Frequency Significance',
                                inc: true,
                                invert: false,
                                weight: 0.5
                            },
                            distance: {
                                label: 'Distance Significance',
                                inc: true,
                                invert: false,
                                weight: 0.5
                            }
                        },
                        binaryCorrelation: {
                            proximity: {
                                label: 'Proximity Correlation',
                                inc: true,
                                invert: false,
                                weight: 0.5
                            },
                            endpoint: {
                                label: 'Endpoint Correlation',
                                inc: true,
                                invert: false,
                                weight: 0.5
                            },
                            originator: {
                                label: 'Originator Correlation',
                                inc: true,
                                invert: false,
                                weight: 0.5
                            },
                            dataType: {
                                label: 'Data Type Correlation',
                                inc: true,
                                invert: false,
                                weight: 0.5
                            },
                            dataValue: {
                                label: 'Data Value Correlation',
                                inc: true,
                                invert: false,
                                weight: 0.5
                            }
                        },
                    },
                    attenuation: {
                        eventDistance: 5,
                        seleted: 2,
                        radical: 2.7
                    }
                },
                value: [],
                selectTypes: [{
                    value: 'unary',
                    label: 'Unary Metrics'
                }, {
                    value: 'binarySignificance',
                    label: 'Binary Significance'
                }, {
                    value: 'binaryCorrelation',
                    label: 'Binary Correlation'
                }],
                save: null
            }
        },
        methods: {
            inited(viewer) {
                viewer.view(this.images.length - 1);
            },
            progressing() {
                this.progress = true;
                this.percentage = 0;
                let obj = setInterval(() => {
                    this.percentage += 1;
                    if (this.percentage >= 100 || this.progress === false)
                        clearInterval(obj);
                }, 450);
            },
            async nodeChanged(value) {
                this.progressing();
                const data = await nodeFilter({
                    'cutoff': value,
                    'id': this.$store.getters.id
                });
                console.log('change node filter with cutoff: ' + String(value));
                this.handleResponse(data);
                this.progress = false;
            },
            async scChanged(value) {
                this.progressing();
                const data = await edgeFilter({
                    'edge_transformer': 'Fuzzy Edges',
                    's/c_ratio': value,
                    'preserve': this.cutoff,
                    'ignore_self_loops': this.loops,
                    'interpret_absolute': this.absolute,
                    'id': this.$store.getters.id
                });
                console.log('change edge filter with s/c ratio: ' + String(value));
                this.handleResponse(data);
                this.progress = false;
            },
            async cutoffChanged(value) {
                this.progressing();
                const data = await edgeFilter({
                    'edge_transformer': 'Fuzzy Edges',
                    's/c_ratio': this.sc,
                    'preserve': value,
                    'ignore_self_loops': this.loops,
                    'interpret_absolute': this.absolute,
                    'id': this.$store.getters.id
                });
                console.log('change edge filter with cutoff: ' + String(value));
                this.handleResponse(data);
                this.progress = false;
            },
            async preserveChanged(value) {
                this.progressing();
                const data = await concurrencyFilter({
                    'filter_concurrency': this.concurrency,
                    'preserve': Math.pow(value, 4),
                    'balance': this.balance,
                    'id': this.$store.getters.id
                });
                console.log('change concurrency filter with preserve: ' + String(value));
                this.handleResponse(data);
                this.progress = false;
            },
            async balanceChanged(value) {
                this.progressing();
                const data = await concurrencyFilter({
                    'filter_concurrency': this.concurrency,
                    'preserve': Math.pow(this.preserve, 4),
                    'balance': value,
                    'id': this.$store.getters.id
                });
                console.log('change concurrency filter with balance: ' + String(value));
                this.handleResponse(data);
                this.progress = false;
            },
            selectTypes(value) {
                this.selectedType = value;
            },
            openConfig() {
                this.dialog = true;
                this.save = JSON.stringify(this.metricsConfig);
            },
            async saveConfig() {
                if (JSON.stringify(this.metricsConfig) === this.save) {
                    this.$alert('There are no any changes for this operation.', 'No Changes', {
                        confirmButtonText: 'Confirm',
                        type: 'warning'
                    });
                    this.cancelConfig();
                    return;
                }
                let errors = []
                if (!this.metricsConfig.metrics.unary.frequency.inc && !this.metricsConfig.metrics.unary.frequency.invert
                    && !this.metricsConfig.metrics.unary.routing.inc && !this.metricsConfig.metrics.unary.routing.invert) {
                    errors.push('unary significance');
                }
                if (!this.metricsConfig.metrics.binarySignificance.frequency.inc && !this.metricsConfig.metrics.binarySignificance.frequency.invert
                    && !this.metricsConfig.metrics.binarySignificance.distance.inc && !this.metricsConfig.metrics.binarySignificance.distance.invert) {
                    errors.push('binary significance');
                }
                if (!this.metricsConfig.metrics.binaryCorrelation.proximity.inc && !this.metricsConfig.metrics.binaryCorrelation.proximity.invert
                    && !this.metricsConfig.metrics.binaryCorrelation.originator.inc && !this.metricsConfig.metrics.binaryCorrelation.originator.invert
                    && !this.metricsConfig.metrics.binaryCorrelation.endpoint.inc && !this.metricsConfig.metrics.binaryCorrelation.endpoint.invert
                    && !this.metricsConfig.metrics.binaryCorrelation.dataType.inc && !this.metricsConfig.metrics.binaryCorrelation.dataType.invert
                    && !this.metricsConfig.metrics.binaryCorrelation.dataValue.inc && !this.metricsConfig.metrics.binaryCorrelation.dataValue.invert) {
                    errors.push('binary correlation');
                }
                if (errors.length >= 1) {
                    let msg = 'Choose at least one metric for ';
                    for (let i = 0; i < errors.length; i++) {
                        if (i)
                            msg += ', ' + errors[i];
                        else
                            msg += errors[i];
                    }
                    msg += '.';
                    this.$alert(msg, 'Error', {
                        confirmButtonText: 'OK',
                        type: 'error'
                    });
                    return;
                }
                let req = {
                    metrics: {
                        unary_metrics: {
                            frequency_significance_unary: {
                                include: this.metricsConfig.metrics.unary.frequency.inc,
                                invert: this.metricsConfig.metrics.unary.frequency.invert,
                                weight: this.metricsConfig.metrics.unary.frequency.weight
                            },
                            routing_significance_unary: {
                                include: this.metricsConfig.metrics.unary.routing.inc,
                                invert: this.metricsConfig.metrics.unary.routing.invert,
                                weight: this.metricsConfig.metrics.unary.routing.weight
                            }
                        },
                        binary_significance: {
                            frequency_significance_binary: {
                                include: this.metricsConfig.metrics.binarySignificance.frequency.inc,
                                invert: this.metricsConfig.metrics.binarySignificance.frequency.invert,
                                weight: this.metricsConfig.metrics.binarySignificance.frequency.weight
                            },
                            distance_significance_binary: {
                                include: this.metricsConfig.metrics.binarySignificance.distance.inc,
                                invert: this.metricsConfig.metrics.binarySignificance.distance.invert,
                                weight: this.metricsConfig.metrics.binarySignificance.distance.weight
                            }
                        },
                        binary_correlation: {
                            proximity: {
                                include: this.metricsConfig.metrics.binaryCorrelation.proximity.inc,
                                invert: this.metricsConfig.metrics.binaryCorrelation.proximity.invert,
                                weight: this.metricsConfig.metrics.binaryCorrelation.proximity.weight
                            },
                            endpoint: {
                                include: this.metricsConfig.metrics.binaryCorrelation.endpoint.inc,
                                invert: this.metricsConfig.metrics.binaryCorrelation.endpoint.invert,
                                weight: this.metricsConfig.metrics.binaryCorrelation.endpoint.weight
                            },
                            originator: {
                                include: this.metricsConfig.metrics.binaryCorrelation.originator.inc,
                                invert: this.metricsConfig.metrics.binaryCorrelation.originator.invert,
                                weight: this.metricsConfig.metrics.binaryCorrelation.originator.weight
                            },
                            datatype_correlation_binary: {
                                include: this.metricsConfig.metrics.binaryCorrelation.dataType.inc,
                                invert: this.metricsConfig.metrics.binaryCorrelation.dataType.invert,
                                weight: this.metricsConfig.metrics.binaryCorrelation.dataType.weight
                            },
                            datavalue_correlation_binary: {
                                include: this.metricsConfig.metrics.binaryCorrelation.dataValue.inc,
                                invert: this.metricsConfig.metrics.binaryCorrelation.dataValue.invert,
                                weight: this.metricsConfig.metrics.binaryCorrelation.dataValue.weight
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
                    req.attenuation.radical = this.metricsConfig.attenuation.radical;
                }
                req.id = this.$store.getters.id;
                this.progressing();
                const data = await metrics(req);
                this.handleResponse(data);
                this.dialog = false;
                this.progress = false;
            },
            cancelConfig() {
                if (JSON.stringify(this.metricsConfig) === this.save)
                    this.metricsConfig = JSON.parse(this.save);
                this.save = null;
                this.dialog = false;
            },
            async loading() {
                this.progressing();
                const path = this.$route.params.path;
                const data = await generate({path: path});
                this.progress = false;
                this.handleResponse(data);
                if (data.id)
                    await this.$store.dispatch('app/setId', data.id);
                console.log(data);
            },
            handleResponse(resp) {
                // here needs to handle error message
                if (resp.message_type === 0) {
                    this.images.push(resp.graph_path);
                } else if (resp.message_type === 1) {
                    this.$alert(resp.message_desc + " You'll be redirected to home page to upload a new log file.", 'Error', {
                        confirmButtonText: 'OK',
                        type: 'error'
                    }).then(() => {
                        this.$router.push({path: "/"});
                    });
                } else if (resp.message_type === 2) {
                    this.$alert(resp.message_desc, 'Error', {
                        confirmButtonText: 'OK',
                        type: 'error'
                    });
                }
            },
            async downloadImage() {
                console.log("Download Image");
                const resp = await Axios({
                    url: this.selectedImage,
                    method: 'get',
                    responseType: 'blob'
                });
                // here need to handle error
                const data = resp.data;
                let a = document.createElement('a');
                let url = window.URL.createObjectURL(new Blob([data], {type: 'image/png'}));
                a.href = url;
                a.download = 'graph.png';
                a.click();
                window.URL.revokeObjectURL(url);
                a.remove();
            }
        },
        watch: {
            edge: async function (now, old) {
                this.progressing();
                let resp;
                if (now === old)
                    return;
                if (now === 1) {
                    resp = await edgeFilter({
                        'edge_transformer': 'Best Edges',
                        'ignore_self_loops': this.loops,
                        'id': this.$store.getters.id
                    });
                } else {
                    resp = await edgeFilter({
                        'edge_transformer': 'Fuzzy Edges',
                        's/c_ratio': this.sc,
                        'preserve': this.cutoff,
                        'ignore_self_loops': this.loops,
                        'interpret_absolute': this.absolute,
                        'id': this.$store.getters.id
                    });
                }
                console.log('change edge filter with edge transformer: ' + now);
                this.handleResponse(resp);
                this.progress = false;
            },
            loops: async function (now, old) {
                this.progressing();
                if (now === old)
                    return;
                let data;
                if (this.edge === 1) {
                    data = await edgeFilter({
                        'edge_transformer': 'Best Edges',
                        'ignore_self_loops': now,
                        'id': this.$store.getters.id
                    });
                } else {
                    data = await edgeFilter({
                        'edge_transformer': 'Fuzzy Edges',
                        's/c_ratio': this.sc,
                        'preserve': this.cutoff,
                        'ignore_self_loops': now,
                        'interpret_absolute': this.absolute,
                        'id': this.$store.getters.id
                    });
                }
                console.log('change edge filter with ignore self-loops: ' + String(now));
                this.handleResponse(data);
                this.progress = false;
            },
            absolute: async function (now, old) {
                this.progressing();
                if (now === old)
                    return;
                const data = await edgeFilter({
                    'edge_transformer': 'Fuzzy Edges',
                    's/c_ratio': this.sc,
                    'preserve': this.cutoff,
                    'ignore_self_loops': this.loops,
                    'interpret_absolute': now,
                    'id': this.$store.getters.id
                });
                console.log('change edge filter with interpret absolute: ' + String(now));
                this.handleResponse(data);
                this.progress = false;
            },
            concurrency: async function (now, old) {
                this.progressing();
                if (now === old)
                    return;
                const data = await concurrencyFilter({
                    'filter_concurrency': now,
                    'preserve': Math.pow(this.preserve, 4),
                    'balance': this.balance,
                    'id': this.$store.getters.id
                });
                console.log('change concurrency filter with filter concurrency: ' + String(now));
                this.handleResponse(data);
                this.progress = false;
            },
        },
        computed: {
            concurrencyPreserve() {
                return Math.pow(this.preserve, 4).toFixed(3);
            }
        },
        mounted() {
            this.$el.querySelector('#viewer').addEventListener('viewed', (e) => {
                this.selectedImage = e.detail.originalImage.currentSrc;
            });
        },
        created() {
            this.loading();
        }
    }
</script>

<style>
    .viewer-canvas {
        background-color: #303133 !important;
    }
</style>

<style scoped>
    .model-view {
        width: 90%;
        position: relative;
        display: block;
    }

    .model-view-conf {
        width: 96%;
        position: relative;
        display: block;
    }

    .text-center-align {
        text-align: center;
    }

    .page-layout {
        position: relative;

        height: 100vh;

    }

    .filter-container {
        height: 70vh;
        border-color: #f0f0f0;

    }

    .grid-content {
        height: inherit;
        background-color: #d9d9d9;

    }

    .grid-content-configuration {
        height: inherit;
        border-color: #d9d9d9;
    }

    .process-graph-view {
        height: 70vh;
        border-color: #dcdfe6;
        overflow: hidden;
    }

    .button-position {

        position: relative;
        top: 20px;
        border-radius: 2px;


    }

    .slider-adjustment1 {
        position: relative;
        top: 12.5%;
    }

    .slider-adjustment2 {
        display: flex;
        align-items: center;
        justify-content: space-evenly

    }

    .slider-adjustment3 {
        display: flex;
        justify-content: space-evenly;
        position: relative;
        top: 5.5%;
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

    h4 {
        font-size: 1vm;
        font-weight: bold;

    }

    h5 {
        font-weight: lighter;
        color: coral;
    }

    [class*="el-checkbox"] {
        padding-left: 0;

    }

    h3 {
        color: darkorange;
    }
    .el-radio__label{
        font-size: 16px;
    }

</style>
