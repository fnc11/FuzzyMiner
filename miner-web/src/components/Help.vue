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
                            <h4>1.Set up guide</h4>
                        </template>
                        <el-menu-item index="/help/windows">1.1 Installations on Windows</el-menu-item>
                        <el-menu-item index="/help/mac">1.2 Installations on Mac</el-menu-item>
                        <el-menu-item index="/help/linux">1.3 Installations on Linux</el-menu-item>
                    </el-submenu>

                    <el-submenu index="2">
                        <template slot="title">
                            <h4>2. How to use Fuzzy Web</h4>
                        </template>
                        <el-menu-item index="/help/generate">2.1 To generate fuzzy model</el-menu-item>
                        <el-submenu index="2-2">
                            <template slot="title">2.2 To apply filter configurations</template>
                            <el-menu-item index="/help/node">2.2.1 Node Filter</el-menu-item>
                            <el-menu-item index="/help/edge">2.2.2 Edge Filter</el-menu-item>
                            <el-menu-item index="/help/concurrency">2.2.3 Concurrency Filter</el-menu-item>
                        </el-submenu>
                        <el-submenu index="2-3">
                            <template slot="title">2.3 To apply Metrics configurations</template>
                            <el-menu-item index="/help/unary">2.3.1 Unary Significance Metrics</el-menu-item>
                            <el-menu-item index="/help/binary">2.3.2 Binary Significance Metrics</el-menu-item>
                            <el-menu-item index="/help/correlation">2.3.3 Binary Correlation Metrics</el-menu-item>
                        </el-submenu>
                        <el-submenu index="2-4">
                            <template slot="title">2.4 To Modify Attenuation</template>
                            <el-menu-item index="/help/linear">2.4.1 Linear Attenuation</el-menu-item>
                            <el-menu-item index="/help/nroot">2.4.2 N(th) Root Attenuation</el-menu-item>
                        </el-submenu>
                        <el-menu-item index="/help/snapshot">2.5 To save model snapshot
                        </el-menu-item>
                    </el-submenu>
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

    display: inline-block;
        overflow:hidden;
        word-wrap: break-word;

    }

    .el-col-6 {

    }

    .el-sub-menu {
        

    }
</style>