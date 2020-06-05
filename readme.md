<h1 align="center">Fuzzy Miner</h1>
<div align="center">
  <strong>A fuzzy miner web application by which you can generate process models as per your requirements. Import a <a href="http://xes-standard.org/" target="_blank">XES</a> log file and just wait for the miner to generate the process model. The metrics and the filters are at your disposal and can be modified as per your requirements.</strong>
</div>
<div align="center">
  
  [![forthebadge](http://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)
  <br>
  <!-- Stability -->
  <a href="https://nodejs.org/api/documentation.html#documentation_stability_index">
    <img src="https://img.shields.io/badge/stability-stable-orange.svg?style=flat-square"
      alt="API stability" />
  </a>
  <a href="https://github.com/fnc11/FuzzyMiner/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/fnc11/FuzzyMiner"></a>
  <!-- Standard -->
  <a href="https://standardjs.com">
    <img src="https://img.shields.io/badge/code%20style-standard-brightgreen.svg?style=flat-square"
      alt="Standard" />
  </a>
  
  ![GitHub repo size](https://img.shields.io/github/repo-size/fnc11/fuzzyminer)
  
</div>

## Table of Contents
- [Features](#features)
- [Technology used](#technology-used)
- [Installation requirements](#installation-requirements)
    - [Windows](#windows)
    - [MacOS](#macos)
    - [Linux](#linux)
- [Creating a virtual environnment](#creating-a-virtual-environment)
- [How to use](#how-to-use)
- [Contributors](#contributors)
- [Credits](#credits)

## Features
- __Easy to use:__ our package makes it easy for generating process models for unstructured data
- __Isomorphic:__ renders seamlessly in both Node and browsers
- __Fast:__ Can handle large log files. Well in case of too large, you need to wait a bit!

## Technology used
<b>Built with</b>
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Vue JS](https://vuejs.org/)
- [Element](https://element.eleme.io/#/en-US)

<b>Tested with</b>
- [PyUnit](https://docs.python.org/2/library/unittest.html)

## Installation requirements

#### Windows
1. Install Python from [here](https://www.python.org/). <br> <br>
Four Python 3.6 installers are available for download - two each for the 32-bit and 64-bit versions of the interpreter. The web installer is a small initial download, and it will automatically download the required components as necessary. <br>
<br>
After starting the installer, one of two options may be selected:
<br><br>
<b>If you select “Install Now”:</b>
- You will not need to be an administrator (unless a system update for the C Runtime Library is required or you install the [Python Launcher](https://docs.python.org/3.6/using/windows.html#launcher) for Windows for all users)
- Python will be installed into your user directory
- The [Python Launcher](https://docs.python.org/3.6/using/windows.html#launcher) for Windows will be installed according to the option at the bottom of the first page
- The standard library, test suite, launcher and pip will be installed
- If selected, the install directory will be added to your `PATH`
- Shortcuts will only be visible for the current user
<br><br>
<b>Selecting “Customize installation” will allow you to select the features to install, the installation location and other options or post-install actions. To install debugging symbols or binaries, you will need to use this option.</b>
<br><br>
- To perform an all-users installation, you should select “Customize installation”. In this case:
- You may be required to provide administrative credentials or approval
- Python will be installed into the Program Files directory
- The Python Launcher for Windows will be installed into the Windows directory
- Optional features may be selected during installation
- The standard library can be pre-compiled to bytecode
- If selected, the install directory will be added to the system PATH
- Shortcuts are available for all users


2. Install Node.js
```
pip install nodejs
```
3. Install npm
```
pip install npm
```

#### MacOS

#### Linux

## Creating a Virtual Environment
1. The virtualenv package is required to create virtual environments. You can install it with pip:
```
pip install virtualenv
``` 
2. To create a virtual environment, you must specify a path. For example to create one in the local directory called ‘mypython’, type the following:
```
virtualenv mypython
```
3.You can activate the python environment by running the following:
##### Windows command
```
mypthon\Scripts\activate
```
##### MacOS/Linux command
```
source mypython/bin/activate
```
You should see the name of your virtual environment in brackets on your terminal line e.g. (mypython). Any python commands you use will now work with your virtual environment

## Running the project
1. Clone the repository:
```
git clone URL
```
2. Assuming you have virtual environment somewhere inside or outside the project(it doesn't matter as that will not be stored on github), activate it and install necessary softwares by running following command.
```
pip install -r requirements.txt 
```
3. Go to `/miner-web` folder and run the following
```
npm install
npm run build
```
4. Change `FuzzyMiner/FuzzyMiner/settings.py.example` to `settings.py`
5. Run the script `secret.py`
```
python3 secret.py
```
6. Copy the displayed key in previous step and paste it in as value for `SECRET_KEY` variable in the `settings.py` file
7. Run the following command after navigating to `FuzzyMiner/FuzzyMiner`
```
python3 manage.py runserver
```
## How to use?
Please refer to the <b>Help</b> page of the web application when you run it.

## Contributors
Built with ❤ by:

* [Praveen Yadav](https://github.com/fnc11) 
* [Pruthvi Hegde](https://github.com/pruthvi11) 
* [Prantik Chatterjee](https://github.com/Prantikc22)
* [Iftekhr Ahmed](https://github.com/iftekhar-ahmed)
* [Yongzhao Li](https://github.com/Pireirik) 


## Reference
* Madhavi Shankar Narayana
* [ Business Process Management: 5th International Conference, BPM 2007, Brisbane, Australia, September 24-28, 2007. Proceedings](https://www.researchgate.net/publication/221586306_Fuzzy_Mining_-_Adaptive_Process_Simplification_Based_on_Multi-perspective_Metrics)
