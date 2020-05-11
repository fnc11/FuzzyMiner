<template>
    <div class="main">
        <div>
            <el-row class="banner-content">
                <h1>One step to Mine the Fuzzy Model!</h1>
            </el-row>
            <el-row class="button-class" justify="center" type="flex">
                <el-col :span="2.5">
                    <el-upload
                            ref="upload"
                            action=""
                            :limit="1"
                            accept=".xes"
                            :http-request="upload"
                            :auto-upload="true"
                            :show-file-list="false"
                            :before-upload="checkType"
                            :on-success="uploadSuccess"
                            :on-error="uploadError">
                        <el-button type="primary" class="button-primary">Upload Logs</el-button>
                        <div slot="tip" class="el-upload__tip">Accepted file format is .xes.</div>
                    </el-upload>
                </el-col>
                <el-col :span="2.5">
                    <el-button type="success" class="button-success" @click="generate" :disabled="generated">Generate</el-button>
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
        data() {
            return {
                generated: true
            }
        },
        methods: {
            async upload(param) {
                let form = new FormData();
                form.append('file', param.file);
                const data = await upload(form);
                console.log(data);
                this.generated = false;
            },
            generate() {

            },
            uploadSuccess(response, file) {
                this.$message({
                    message: 'Success to upload the file, ' + file.name,
                    type: 'success',
                    duration: 3000,
                    showClose: true
                });
            },
            uploadError(error) {
                console.log(error.message);
                this.message({
                    message: error.message,
                    type: 'error',
                    duration: 3000,
                    showClose: true
                });
            },
            checkType(file) {
                if (!file.name.endsWith('.xes')) {
                    this.$message({
                        message: 'Wrong file format, xes file only',
                        type: 'error',
                        duration: 3000,
                        showClose: true
                    });
                    return false;
                }
                return true;
            }
        }
    }
</script>

<style scoped>
    .main {
        height: 60vh;
        display: flex;
        justify-content: center;
        align-items: center;

    }

    .banner-content {
        text-align: center;
    }

    .button-class {
        height: inherit;
        top: 5vh;

    }

    .button-primary {
        background-color: cornflowerblue;

    }
</style>
