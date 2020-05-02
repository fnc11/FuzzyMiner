#Read me file for this project.

##Running the project
1. Clone the repository:
```
git clone URL
```
2. Checkout the branch you want to see.
```
git checkout develop
```
3. Assuming you have virtual environment somewhere inside or outside the project(it doesn't matter as that will not be stored on github), activate it and install necessary softwares by running following command.
```
pip install -r requirements.txt 
```
4. Install nodejs related packages.
```
sudo apt-get install nodejs
sudo apt-get install npm
```
(If there are errors install this first ```sudo apt-get install nodejs-dev node-gyp libssl1.0-dev``` and then retry installing npm.)
5. Go to miner-web folder and run the following
```
npm install
npm run build
```
6. Change FuzzyMiner/FuzzyMiner/settings.py.example to settings.py
7. Run the script secret.py
```
python3 secret.py
```
8. copy the displayed key in previous step and paste it in as value for SECRET_KEY variable in the settings.py file.
9. Run the following command after going to the FuzzyMiner/FuzzyMiner place.
```
python3 manage.py runserver
```
##For Configuring PyCharm
