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
            <br><br><br>
            <el-row class="file-list" justify="center" type="flex">
                <ul>
                    <li v-for="(elem, index) in fileList" :key="index">
                        <a>
                            <i class="el-icon-document"></i>
                            {{ elem }}
                        </a>
                        <label>
                            <i class="el-icon-upload-success el-icon-circle-check"></i>
                        </label>
                    </li>
                </ul>
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
    import { upload, generate } from "@/api/home";

    export default {
        name: "Home",
        data() {
            return {
                generated: true,
                fileList: [],
                path: ''
            }
        },
        methods: {
            async upload(param) {
                let form = new FormData();
                form.append('file', param.file);
                const data = await upload(form);
                this.path = data;
                console.log(this.path);
                this.generated = false;
            },
            async generate() {
                const data = await generate({
                    'path': this.path
                });
                this.$router.push({path: '/filter'});
            },
            uploadSuccess(response, file) {
                this.$message({
                    message: 'Success to upload the file, ' + file.name,
                    type: 'success',
                    duration: 3000,
                    showClose: true
                });
                this.fileList.splice(0, this.fileList.length);
                this.fileList.push(file.name);
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

    .file-list {
        text-align: center;
        position: inherit;
        bottom: 5vh;
    }
</style>
