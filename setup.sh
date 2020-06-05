'''
This file sets up the virtual environment.
Run "source setup.sh" each time you want to run the app.
'''
FLASK_VERSION="${FLASK_VERSION:-0.12.2}"              #0.12.2
# PEEWEE_VERSION="${PEEWEE_VERSION:-2.10.2}"            #2.10.2
PYAML_VERSION="${PYAML_VERSION:-3.12}"                #3.12
XLSXWRITER_VERSION="${XLSXWRITER_VERSION:-1.0.2}"     #1.0.2
MYSQLPYTHON_VERSION="${MYSQLPYTHON_VERSION=-1.2.5}"   #1.2.5
FLASK_ADMIN_VERSION="${FLASK_ADMIN_VERSION:-1.5.0}"   #1.5.0
WTF_PEEWEE_VERSION="${WTF_PEEWEE_VERSION:-0.2.6}"     #0.2.6
FLASK_LOGIN_VERSION="${FLASK_LOGIN_VERSION:-0.4.1}"   #0.4.1


mkdir -p data

if [ ! -d venv ]
then
  python3 -m venv venv
fi

. venv/bin/activate

python3 -m pip install --upgrade pip #added python-m for pip installs (source setup overwrite for venv)

python3 -m pip install -r requirements.txt
