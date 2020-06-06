<template>
    <div>
        <el-container>
            <el-aside>
                <el-menu
                        router
                        :default-active="this.$route.path"
                        class="el-menu-vertical-demo"
                        @open="handleOpen"
                        @close="handleClose">
                    <el-submenu index="1">
                        <template slot="title">
                            <h4>Set up guide</h4>
                        </template>
                        <el-menu-item index="/help/windows">Installations on Windows</el-menu-item>
                        <el-menu-item index="/help/mac">Installations on Mac</el-menu-item>
                        <el-menu-item index="/help/linux">Installations on Linux</el-menu-item>
                        <el-menu-item index="/help/pycharm">Set up pycharm project</el-menu-item>
                    </el-submenu>

                    <el-submenu index="2">
                        <template slot="title">
                            <h4>How to use Fuzzy Web</h4>
                        </template>
                        <el-menu-item index="/help/generate">To generate fuzzy model</el-menu-item>
                        <el-submenu index="2-2">
                            <template slot="title">To apply filter configurations</template>
                            <el-menu-item index="/help/node">Node Filter</el-menu-item>
                            <el-menu-item index="/help/edge">Edge Filter</el-menu-item>
                            <el-menu-item index="/help/concurrency">Concurrency Filter</el-menu-item>
                        </el-submenu>
                        <el-submenu index="2-3">
                            <template slot="title">To apply Metrics configurations</template>
                            <el-menu-item index="/help/unary">Unary Significance Metrics</el-menu-item>
                            <el-menu-item index="/help/binary">Binary Significance Metrics</el-menu-item>
                            <el-menu-item index="/help/correlation">Binary Correlation Metrics</el-menu-item>
                        </el-submenu>
                        <el-submenu index="2-4">
                            <template slot="title">To Modify Attenuation</template>
                            <el-menu-item index="/help/linear">Linear Attenuation</el-menu-item>
                            <el-menu-item index="/help/nroot">N(th) Root Attenuation</el-menu-item>
                        </el-submenu>
                        <el-menu-item index="/help/snapshot">To save model snapshot
                        </el-menu-item>
                    </el-submenu>
                    <el-menu-item index="/help/video">
                        <h4>Demo Video</h4>
                    </el-menu-item>
                    <el-menu-item index="/help/faqs">
                        <h4>FAQs</h4>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <router-view />
            </el-main>
        </el-container>
    </div>
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