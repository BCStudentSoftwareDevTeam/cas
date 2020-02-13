
import os
from app.loadConfig import *
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb


dir_name= os.path.dirname(__file__) # Return the directory name of pathname _file_
cfg       =load_config(os.path.join(dir_name, 'app/config.yaml'))
db_name   =cfg['db']['db_name']
host      =cfg['db']['host']
username=cfg['db']['username']
password =cfg['db']['password']
db= MySQLdb.connect( host, username, password, db_name)


cursor= db.cursor()

cursor.execute("ALTER TABLE `course` ADD `faculty_credit` FLOAT NOT NULL AFTER `parentCourse_id`")

db.close()
