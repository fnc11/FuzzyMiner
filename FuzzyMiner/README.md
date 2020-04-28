# FuzzyMiner
This is a django project for fuzzy miner.
## Environment
- python: version 3.7.3
- django: version 2.2.9
## Setup
1. Rename the settings.py.example file to settings.py
2. Fill in the variable in settings.py file for the key of SECRET_KEY by running the secret.py script to get the secret key
3. Build the frontend and then check whether the static folder and index.html are existing in the templates folder
4. Run python3 $FUZZYMINER_DIR/manage.py runserver $PORT

**replace {FUZZYMINER_DIR} with your dir of the project directory and {PORT} with your linstening port**