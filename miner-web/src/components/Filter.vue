<template>
    <div>
        <el-row :gutter="10">
            <el-col :span="16">
                <div class="model-view">
                    <h3 align="center"> Fuzzy Model</h3>
                    <div class="el-tabs--border-card" >

                    </div>
                    <!-- here should be canvas -->
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
                    <div>
                        <el-checkbox v-model="staticMethod">Static</el-checkbox>
                        <el-button-group>
                            <el-button>Apply</el-button>
                            <el-button>Undo</el-button>
                        </el-button-group>
                    </div>
                    <el-button>Metrics Configuration</el-button>
                </div>
            </el-col>
        </el-row>
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
                staticMethod: false
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
