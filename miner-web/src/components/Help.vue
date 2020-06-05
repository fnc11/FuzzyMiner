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
                            <h4>1.Installation Guide</h4>
                        </template>
                        <el-menu-item index="/help/windows">1.1 Installations on Windows</el-menu-item>
                        <el-menu-item index="/help/mac">1.2 Installations on Mac</el-menu-item>
                        <el-menu-item index="/help/linux">1.3 Installations on Linux</el-menu-item>
                    </el-submenu>

                    <el-submenu index="2">
                        <template slot="title">
                            <h4>2.Get Started</h4>
                        </template>
                        <el-submenu>
                            <template slot="title">2.1 Overview of the user interface</template>
                            <el-menu-item index="/help/home">2.1.1 Home Screen</el-menu-item>
                            <el-menu-item index="/help/filter">2.1.2 Fuzzy Model Screen</el-menu-item>
                            <el-menu-item index="/help/metrics">2.1.3 Metrics Configuration</el-menu-item>
                        </el-submenu>
                    </el-submenu>
                        <el-menu-item index="/help/generate">
                            <h4>3. How To generate fuzzy model</h4>
                        </el-menu-item>
                        <el-submenu index="3">
                            <template slot="title"><h4>4. Filter configuration</h4></template>
                            <el-menu-item index="/help/node">3.1 Node Filter</el-menu-item>
                            <el-menu-item index="/help/edge">3.2 Edge Filter</el-menu-item>
                            <el-menu-item index="/help/concurrency">3.3 Concurrency Filter</el-menu-item>
                        </el-submenu>
                        <el-submenu index="4">
                            <template slot="title"><h4>4. To apply Metrics configurations</h4></template>
                            <el-menu-item index="/help/unary">4.1 Unary Significance Metrics</el-menu-item>
                            <el-menu-item index="/help/binary">4.2 Binary Significance Metrics</el-menu-item>
                            <el-menu-item index="/help/correlation">4.3 Binary Correlation Metrics</el-menu-item>
                        </el-submenu>
                        <el-submenu index="5">
                            <template slot="title"><h4>5. To Modify Attenuation</h4></template>
                            <el-menu-item index="/help/linear">5.1 Linear Attenuation</el-menu-item>
                            <el-menu-item index="/help/nroot">5.2 N(th) Root Attenuation</el-menu-item>
                        </el-submenu>
                        <el-menu-item index="/help/snapshot"><h4>6. To save model snapshot</h4>
                        </el-menu-item>

                        <el-menu-item index="/help/video">
                            <h4>3. Demo Video</h4>
                        </el-menu-item>
                        <el-menu-item index="/help/faqs">
                            <h4>4. FAQs</h4>
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
        font-family: "Sitka Subheading";
        font-weight: normal;
        line-height: 16px;
        padding: 8px 0;
        overflow:hidden;
        word-wrap: break-word;

    }

    .el-aside {
        border-right: groove;
        overflow-x: hidden;
        position: page;
    }


    .el-sub-menu {
        

    }
</style>