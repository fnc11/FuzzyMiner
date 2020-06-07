<template>
    <div>
        <label class="header">Installation on MacOS</label>
        <ol>
            <li>Install homebrew</li>
             <pre><code>ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
</code></pre>
        </ol>

        <ol start="2">
            <li>Install python</li>
              <pre><code>brew install python
</code></pre>
        </ol>

        <ol start="3">
            <li>Install pip</li>
             <pre><code>curl -O http://python-distribute.org/distribute_setup.py
python distribute_setup.py
curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
python get-pip.py
</code></pre>
        </ol>

        <ol start="4">
            <li>Install virtualenv</li>
            <pre><code>pip install virtualenv
</code></pre>
        </ol>

        <ol start="5">
            <li>Install nodejs and npm</li>
            <pre><code>brew update
brew install node
</code></pre>
        </ol>

    </div>
</template>

<script>
    export default {
        name: "Mac"
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