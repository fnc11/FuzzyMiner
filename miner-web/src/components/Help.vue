<template>
    <el-row class="tac">

        <el-col :span="6">
            <el-menu
                    default-active="1-1"
                    class="el-menu-vertical-demo"
                    @open="handleOpen"
                    @close="handleClose">
                <el-submenu index="1">
                    <template slot="title">
                        <h4>Set up guide</h4>
                    </template>
                    <el-menu-item index="1-1">Installations on Windows</el-menu-item>
                    <el-menu-item index="1-2">Installations on Mac</el-menu-item>
                    <el-menu-item index="1-3">Installations on Linux</el-menu-item>
                    <el-menu-item index="1-4">Set up pycharm project</el-menu-item>
                </el-submenu>

                <el-submenu index="2">
                    <template slot="title">
                        <h4>How to use Fuzzy Web</h4>
                    </template>
                    <el-menu-item index="2-1">To generate fuzzy model</el-menu-item>
                    <el-submenu index="2-2">
                        <template slot="title">To apply filter configurations</template>
                        <el-menu-item index="2-2-1">Node Filter</el-menu-item>
                        <el-menu-item index="2-2-2">Edge Filter</el-menu-item>
                        <el-menu-item index="2-2-3">Concurrency Filter</el-menu-item>
                    </el-submenu>
                    <el-submenu index="2-3">
                        <template slot="title">To apply Metrics configurations</template>
                        <el-menu-item index="2-2-1">Unary Significance Metrics</el-menu-item>
                        <el-menu-item index="2-2-2">Binary Significance Metrics</el-menu-item>
                        <el-menu-item index="2-2-3">Binary Correlation Metrics</el-menu-item>
                    </el-submenu>
                    <el-submenu index="2-4">
                        <template slot="title">To Modify Attenuation</template>
                        <el-menu-item index="2-4-1">Linear Attenuation</el-menu-item>
                        <el-menu-item index="2-4-2">N(th) Root Attenuation</el-menu-item>
                    </el-submenu>
                    <el-menu-item index="2-5">To save model snapshot
                    </el-menu-item>
                </el-submenu>
                <el-menu-item index="3">
                    <h4>Demo Video</h4>
                </el-menu-item>
                <el-submenu index="4">
                    <template slot="title">
                        <h4>FAQs</h4>
                    </template>
                    <el-menu-item index="4-1">How to occlude irrelavant nodes?</el-menu-item>
                    <el-menu-item index="4-2">How to only visualise only important edges?</el-menu-item>
                    <el-menu-item index="4-3">How to give higher importance to Resource Correlation?</el-menu-item>
                    <el-menu-item index="4-4">How to change attenuation from Nth root to Linear?</el-menu-item>
                    <el-menu-item index="4-5">How to disable concurrency filter?</el-menu-item>
                </el-submenu>
            </el-menu>
        </el-col>
        <el-col :span="18">

        </el-col>

    </el-row>

</template>

<script>
    export default {
        methods: {
            handleOpen(key, keyPath) {
                console.log(key, keyPath);
            },
            handleClose(key, keyPath) {
                console.log(key, keyPath);
            }
        }
    }
</script>

<style scoped>
    .el-menu {
        letter-spacing: normal;
        color: #606266;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Droid Sans', 'Helvetica Neue', Arial, sans-serif;
        font-size: 12px;
        font-weight: normal;
        line-height: 16px;
        padding: 8px 0;

    display: inline-block;
        overflow:hidden;
        word-wrap: break-word;

    }

    .el-col-6 {

    }

    .el-sub-menu {
        

    }
</style>