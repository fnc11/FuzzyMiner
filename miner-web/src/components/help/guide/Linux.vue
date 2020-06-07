<template>
    <div>
        <label class="header">Installation on Linux</label>
        <ol>
            <li>Python3 comes preinstalled in Ubuntu 18.04 and 20.04 so no need to separately do anything, however you
                may need to update it, for that follow below commands:
            </li>
              <pre><code>sudo apt update
sudo apt -y upgrade
</code></pre>
        </ol>

        <ol start="2">
            <li>To install virtualenv pacakge do the following:</li>
            <pre><code>sudo apt-get install python3-venv
</code></pre>
        </ol>

        <ol start="3">
            <li>Install nodejs related packages.</li>
             <pre><code>sudo apt-get install nodejs
sudo apt-get install npm
</code></pre>
        </ol>

        <p>(If there are errors install this first <code>sudo apt-get install nodejs-dev node-gyp libssl1.0-dev</code>
            and then retry installing npm.)</p>
    </div>
</template>

<script>
    export default {
        name: "Linux"
    }
</script>

<style scoped>
    .el-image {
        border-color: black;
        width: 80%;
        height: 80%;
        border: ridge;
    }

    .block {
        border-color: black;
    }

    p, li {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Droid Sans', 'Helvetica Neue', Arial, sans-serif;
        font-size: 15px;
    }

    .header {
        color: black;
        font-size: 30px;
        font-weight: bold;
    }
</style>