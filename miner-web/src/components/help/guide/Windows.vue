<template>
    <div>
        <label class="header">Installation on Windows</label>
        <ol>
            <li>Install Python from <a href="https://www.python.org/" rel="nofollow">here</a>. <br> <br>
                Four Python 3.6 installers are available for download - two each for the 32-bit and 64-bit versions of
                the interpreter. The web installer is a small initial download, and it will automatically download the
                required components as necessary.<br>
                After starting the installer, one of two options may be selected:<br>
                <b>If you select "Install Now":</b></li>
        </ol>
        <ul>
            <li>You will not need to be an administrator (unless a system update for the C Runtime Library is required
                or you install the <a href="https://docs.python.org/3.6/using/windows.html#launcher" rel="nofollow">Python
                    Launcher</a> for Windows for all users)
            </li>
            <li>Python will be installed into your user directory</li>
            <li>The <a href="https://docs.python.org/3.6/using/windows.html#launcher" rel="nofollow">Python Launcher</a>
                for Windows will be installed according to the option at the bottom of the first page
            </li>
            <li>The standard library, test suite, launcher and pip will be installed</li>
            <li>If selected, the install directory will be added to your <code>PATH</code></li>
            <li>Shortcuts will only be visible for the current user<br><br>
                <b>Selecting “Customize installation” will allow you to select the features to install, the installation
                    location and other options or post-install actions. To install debugging symbols or binaries, you
                    will need to use this option.</b><br><br></li>
            <li>To perform an all-users installation, you should select “Customize installation”. In this case:</li>
            <li>You may be required to provide administrative credentials or approval</li>
            <li>Python will be installed into the Program Files directory</li>
            <li>The Python Launcher for Windows will be installed into the Windows directory</li>
            <li>Optional features may be selected during installation</li>
            <li>The standard library can be pre-compiled to bytecode</li>
            <li>If selected, the install directory will be added to the system PATH</li>
            <li>Shortcuts are available for all users</li>
        </ul>
        <br>
        <ol start="2">
            <li>
                <p>Install Node.js from <a href="https://www.python.org/" rel="nofollow">here</a>. <br> <br>
                    The node package manager (npm) will also be installed with NodeJS and is required for project.<br>
                </p>
            </li>
        </ol>

        <ol start="3">
            <li>Install npm</li>
              <pre><code>pip install npm
</code></pre>
        </ol>

        <ol start="4">
            <li>Install virtualenv</li>
             <pre><code>pip install virtualenv
</code></pre>

        </ol>


    </div>
</template>

<script>
    export default {
        name: "Windows"
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
    code{

    }
</style>
