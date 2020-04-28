<template>
    <div>
        <div>
            <h3>Fuzzy Miner Web Application</h3>
            <el-upload
                ref="upload"
                action=""
                :limit="1"
                accept=".xes"
                :http-request="upload"
                :auto-upload="true">
                <el-button>Upload Logs</el-button>
                <div slot="tip" class="el-upload__tip">Accepted file format is .xes.</div>
            </el-upload>
            <el-button @click="generate">Generate</el-button>
        </div>
        <div>
            <h3>Process Mining</h3>
        </div>
        <div>
            <h3>Fuzzy Miner</h3>
        </div>
    </div>
</template>

<script>
    import { upload } from "@/api/home";

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
</style>
