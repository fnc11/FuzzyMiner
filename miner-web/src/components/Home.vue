<template>
    <div>
        <div>
            <el-row class="banner-content">
                <h1>One step to Mine the Fuzzy Model!</h1>
            </el-row>
            <el-row type="flex" justify="center">
                <el-col :span="2.5">
                    <el-upload
                            ref="upload"
                            action=""
                            :limit="1"
                            accept=".xes"
                            :http-request="upload"
                            :auto-upload="true">
                        <el-button type="primary">Upload Logs</el-button>
                        <div slot="tip" class="el-upload__tip">Accepted file format is .xes.</div>
                    </el-upload>
                </el-col>
                <el-col :span="2.5">
                    <el-button type="success" @click="generate" disabled>Generate</el-button>
                </el-col>
            </el-row>
        </div>
        <!--
        <div>
            <h3>Process Mining</h3>
        </div>
        <div>
            <h3>Fuzzy Miner</h3>
        </div>
        -->
    </div>
</template>

<script>
    import {upload} from "@/api/home";

    export default {
        name: "Home",
        methods: {
            async upload(param) {
                let form = new FormData();
                form.append('file', param.file);
                const data = await upload(form);
                console.log(data);
            },
            generate() {

            }
        }
    }
</script>

<style scoped>
    .banner-content{
        text-align: center;
    }
</style>
