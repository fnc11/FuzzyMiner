<template>
    <div class="main">
        <div>
            <el-row class="banner-content">
                <h1 class="wrapper">One step to mine the Fuzzy Model!</h1>
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
                        <div slot="tip" class="el-upload__tip" style="color: slategrey">Accepted file format is .xes.</div>
                    </el-upload>
                </el-col>
                <el-col :span="2.5">
                    <el-button type="success" class="button-success" @click="generate" :disabled="generated">Generate</el-button>
                </el-col>
                <el-col :span="2.5">
                    <el-button @click="generateDemo">Example Model</el-button>
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
            <br><br><br>
        </div>
        <!--
    <div>
        <h3>Process Mining</h3>
    </div>
    <div>
        <h3>Fuzzy Miner</h3>
    </div>
    -->
        <el-dialog
            title="Progress"
            :visible="progress"
            width="25%">
            <el-progress type="line" :percentage="percentage"></el-progress>
            <i class="el-icon-loading" />
            <label v-if="percentage === 100">Please hold on, the server is running.</label>
        </el-dialog>
    </div>
</template>

<script>
    import {upload} from "@/api/home";

    export default {
        name: "Home",
        data() {
            return {
                generated: true,
                fileList: [],
                path: '',
                progress: false,
                percentage: 0,

            }
        },
        methods: {
            async upload(param) {
                this.progress = true;
                let form = new FormData();
                form.append('file', param.file);
                let config = {
                    onUploadProgress: progressEvent => {
                        let completed = (progressEvent.loaded / progressEvent.total).toFixed(2) * 100;
                        this.percentage = completed;
                        if (this.percentage >= 100) {
                            this.progress = false;
                        }
                    },
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                };
                const data = await upload(form, config);
                this.path = data;
                console.log(this.path);
                this.generated = false;
                this.percentage = 0;
            },
            generate() {
                this.$router.push({name: 'Filter', params: {path: this.path}});
            },
            generateDemo() {
                this.$router.push({name: 'Filter', params: {path: '/media/Road50.xes'}});
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
        position: relative;
        top: 5vh;
    }

    .button-class {
        position: relative;
        height: inherit;
        top: 10vh;

    }

    .button-primary {
        background-color: cornflowerblue;
        border-color: cornflowerblue;

    }


    .file-list {
        text-align: center;
        position: relative;
        top:20px;
    }

    .wrapper {
        color: darkorange;
        overflow: hidden;
        font-weight: bold;
        font-size: xx-large;
        border-right: .15em solid orange;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .12em;
        animation: typing 3.5s steps(40, end),
        blink-caret .75s step-end infinite;

    }

    @keyframes typing {
        from {
            width: 0
        }
        to {
            width: 100%
        }
    }

    @keyframes blink-caret {
        from, to {
            border-color: transparent
        }
        50% {
            border-color: black;
        }
    }


</style>
