<template>
    <div>
        <el-row :gutter="10">
            <el-col :span="16">
                <div>
                    <h3>Fuzzy Model</h3>
                    <!-- here should be canvas -->
                    <el-button>Save Snapshot</el-button>
                </div>
            </el-col>
            <el-col :span="8">
                <div>
                    <h3>Configurations</h3>
<!--                    <el-table style="width: 100%">-->
<!--                        <el-table-column-->
<!--                            label="Node Filter">-->
<!--                            <label>Significance Cutoff</label>-->
<!--                            <el-slider vertical v-model="node" height="200px" />-->
<!--                            <label>{{ node / 100 }}</label>-->
<!--                        </el-table-column>-->
<!--                        <el-table-column-->
<!--                            label="Edge Filter">-->
<!--                            <label>Edge Transformer</label>-->
<!--                            <el-radio-group>-->
<!--                                <el-radio :label="1">Best Edges</el-radio>-->
<!--                                <el-radio :label="2">Fuzzy Edges</el-radio>-->
<!--                            </el-radio-group>-->
<!--                            <label>S/C Ratio</label>-->
<!--                            <el-slider vertical v-model="sc" height="200px" />-->
<!--                            <label>{{ sc / 100 }}</label>-->
<!--                            <label>Cutoff</label>-->
<!--                            <el-slider vertical v-model="cutoff" height="200px" />-->
<!--                            <label>{{ cutoff / 100 }}</label>-->
<!--                            <el-checkbox v-model="loops">Ignore Self-Loops</el-checkbox>-->
<!--                            <el-checkbox v-model="absolute">Interpret Absolute</el-checkbox>-->
<!--                        </el-table-column>-->
<!--                        <el-table-column-->
<!--                            label="Concurrency Filter">-->
<!--                            <el-checkbox v-model="concurrency">Filter Concurrency</el-checkbox>-->
<!--                            <label>Preserve</label>-->
<!--                            <el-slider vertical v-model="preserve" height="200px" />-->
<!--                            <label>{{ preserve / 100 }}</label>-->
<!--                            <label>Balance</label>-->
<!--                            <el-slider vertical v-model="balance" height="200px" />-->
<!--                            <label>{{ balance / 100 }}</label>-->
<!--                        </el-table-column>-->
<!--                    </el-table>-->
<!--                    <el-checkbox v-model="staticMethod">Static</el-checkbox>-->
<!--                    <el-button-group>-->
<!--                        <el-button>Apply</el-button>-->
<!--                        <el-button>Undo</el-button>-->
<!--                    </el-button-group>-->
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

</style>
