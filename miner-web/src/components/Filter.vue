<template>
    <div>
        <el-row :gutter="10">
            <el-col :span="16">
                <div class="model-view">
                    <h3 align="center"> Fuzzy Model</h3>
                    <div class="el-tabs--border-card" >
                        <!-- here should be canvas -->
                    </div>
                    <el-button>Save Snapshot</el-button>
                </div>
            </el-col>
            <el-col :span="8">
                <div class="model-view">
                    <h3 align="center">Configurations</h3>
                    <el-row :gutter="10" class="el-tabs--border-card">
                        <el-col :span="8" class="el-table--border">
                            <label>Node Filter</label>
                            <label>Significance Cutoff</label>
                            <div align="center">
                                <el-slider vertical v-model="node" height="200px"/>
                                <label> {{ node / 100 }}</label>
                            </div>
                        </el-col>
                        <el-col :span="8" class="el-table--border">
                            <label>Edge Filter</label>
                            <label>Edge Transformer</label>
                            <el-radio-group>
                                <el-radio :label="1">Best Edges</el-radio>
                                <el-radio :label="2">Fuzzy Edges</el-radio>
                            </el-radio-group>
                            <label>S/C Ratio</label>
                            <div align="center">
                                <el-slider vertical v-model="sc" height="200px"/>
                                <label>{{ sc / 100 }}</label>
                            </div>
                            <label>Cutoff</label>
                            <el-checkbox v-model="loops">Ignore Self-Loops</el-checkbox>
                            <el-checkbox v-model="absolute">Interpret Absolute</el-checkbox>
                        </el-col>
                        <el-col :span="8" class="el-table--border">

                            <label>Concurrency Filter</label>
                            <el-checkbox v-model="concurrency">Filter Concurrency</el-checkbox>

                            <el-row :gutter="20">
                                <el-col :span="10" align="center">
                                    <label>Preserve</label>
                                    <el-slider vertical v-model="preserve" height="200px"/>
                                    <label>{{ preserve / 100 }}</label>
                                </el-col>

                                <el-col :span="10" align="center">
                                    <label>Balance</label>

                                    <el-slider vertical v-model="balance" height="200px"/>
                                    <label>{{ balance / 100 }}</label>
                                </el-col>
                            </el-row>

                        </el-col>
                    </el-row>
                    <div align="center">
                        <el-checkbox v-model="staticMethod">Static</el-checkbox>
                        <el-button-group>
                            <el-button>Apply</el-button>
                            <el-button>Undo</el-button>
                        </el-button-group>
                    </div>
                    <div align="center">
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
                staticMethod: false,
                dialog: false,
                incFrequency: true,
                frequencyWeight: 50,
                invertFrequency: true,
                incRouting: true,
                routingWeight: 50,
                invertRouting: true
            }
        },
        watch: {
            node(now, old) {
                console.log('Significance cutoff change');
                console.log(now);
                console.log(old);
            },
            edge(now, old) {
                console.log('Edge filter change');
                console.log(now);
                console.log(old);
            },
            sc(now, old) {
                console.log('S/C Ratio change');
                console.log(now);
                console.log(old);
            },
            cutoff(now, old) {
                console.log('Cutoff change');
                console.log(now);
                console.log(old);
            },
            preserve(now, old) {
                console.log('Preserve change');
                console.log(now);
                console.log(old);
            },
            balance(old, now) {
                console.log('Balance change');
                console.log(now);
                console.log(old);
            },
            frequencyWeight(now, old) {
                console.log("Frequency Significance Weight change");
                console.log(now);
                console.log(old);
            },
            routingWeight(now, old) {
                console.log("Routing Significance Weight change");
                console.log(now);
                console.log(old);
            }
        }
    }
</script>

<style scoped>
    .model-view {
        width: 90%;
        position: relative;
        top: 40px;
    }
</style>
