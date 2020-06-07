<template>
    <div class="help_container">
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
                            <h4>1. Installation Guide</h4>
                        </template>
                        <el-menu-item index="/help/windows">1.1 Installations on Windows</el-menu-item>
                        <el-menu-item index="/help/mac">1.2 Installations on Mac</el-menu-item>
                        <el-menu-item index="/help/linux">1.3 Installations on Linux</el-menu-item>
                    </el-submenu>

                        <el-submenu>
                            <template slot="title"><h4>2.1 Overview of the user interface</h4></template>
                            <el-menu-item index="/help/home">2.1.1 Home Screen</el-menu-item>
                            <el-menu-item index="/help/filter">2.1.2 Fuzzy Model Screen</el-menu-item>
                            <el-menu-item index="/help/helpscreen">2.1.3 Help Screen</el-menu-item>
                        </el-submenu>

                      <el-submenu>
                          <template slot="title"><h4>3. Get Started</h4></template>
                    <el-menu-item index="/help/generate">3.1 Generate a fuzzy model from the log
                             </el-menu-item>
                          <el-menu-item index="/help/graph">3.2 Understanding the graph view
                             </el-menu-item>
                             <el-menu-item index="/help/example">3.3 Generate an example model</el-menu-item>
                      </el-submenu>
                        <el-submenu index="3">
                            <template slot="title"><h4>4. Configure Filters</h4></template>
                            <el-menu-item index="/help/node">4.1 Node Filter</el-menu-item>
                            <el-menu-item index="/help/edge">4.2 Edge Filter</el-menu-item>
                            <el-menu-item index="/help/concurrency">4.3 Concurrency Filter</el-menu-item>
                        </el-submenu>
                        <el-submenu index="4">
                            <template slot="title"><h4>5. Configure Metrics</h4></template>
                            <el-menu-item index="/help/unary">5.1 Unary Significance Metrics</el-menu-item>
                            <el-menu-item index="/help/binary">5.2 Binary Significance Metrics</el-menu-item>
                            <el-menu-item index="/help/correlation">5.3 Binary Correlation Metrics</el-menu-item>
                        </el-submenu>


                           <el-menu-item index="/help/attenuation"><h4>6. Modify Attenuation</h4></el-menu-item>



                        <el-menu-item index="/help/video">
                            <h4>7. Demo Video</h4>
                        </el-menu-item>
                        <el-menu-item index="/help/faqs">
                            <h4>8. FAQs</h4>
                        </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main class="main-view">
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

        padding: 8px 0;
        overflow:hidden;
        word-wrap: break-word;

    }

    .el-aside {
        border-right: groove;
        overflow-x: hidden;
        overflow-y: fragments;
        position: relative;
        height: 100vh;

    }
  .el-main{

  }


    .help_container{
    position: relative;



    }
</style>