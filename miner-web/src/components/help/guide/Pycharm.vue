<template>
    <div>
        <label class="header">Running the project</label>

        <ol>
            <li>Clone the repository:</li>
            <pre><code>git clone URL
</code></pre>
        </ol>

        <ol start="2">
            <li>Create a virtual environment inside the package FuzzyMiner</li>
            <pre><code>virtualenv mypython
</code></pre>
        </ol>
        <ol>
            <p>In case of Ubuntu/Linux use the following command to create virtual environment:</p>
            <pre><code>python3 -m venv mypython
        </code></pre>
        </ol>
        <ol start="3">
            <li>Activate the virtual environment</li>
        </ol>
        <ol><h4>Windows command</h4>
            <pre><code>mypthon\Scripts\activate
        </code></pre>
        </ol>
        <ol><h4>MacOS/Linux command</h4>
            <pre><code>source mypython/bin/activate
        </code></pre>
        </ol>
        <ol start="4">
            <li>Assuming you have virtual environment somewhere inside or outside the project(it doesn't matter as that
                will not be stored on github), activate it and install necessary softwares by running following command.
            </li>
            <pre><code>pip install -r requirements.txt
</code></pre>
        </ol>

        <ol start="5">
            <li>Go to <code>/miner-web</code> folder and run the following</li>
            <pre><code>npm install
npm run build
</code></pre>
        </ol>

        <ol start="6">
            <li>Change <code>FuzzyMiner/FuzzyMiner/settings.py.example</code> to <code>settings.py</code></li>
            <li>Run the script <code>secret.py</code></li>
            <pre><code>python3 secret.py
</code></pre>
        </ol>

        <ol start="8">
            <li>Copy the displayed key in previous step and paste it in as value for <code>SECRET_KEY</code> variable in
                the <code>settings.py</code> file
            </li>
            <li>Run the following command after navigating to <code>FuzzyMiner/FuzzyMiner</code></li>
            <pre><code>python3 manage.py runserver
</code></pre>
        </ol>

    </div>
</template>

<script>
    export default {
        name: "Pycharm"
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

