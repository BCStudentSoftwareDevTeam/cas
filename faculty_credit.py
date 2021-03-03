
import os
from app.loadConfig import *
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

def creating_new_columns_in_the_db():
    '''THIS FUNCTION RUNS QUERIES TO CREATE NEW COLUMNS ON EXISTING TABLES ON THE DB.
    IT DOES NOT CHANGE THE OLD EXISTING TABLES AND COLUMNS, IT ONLY ADDS NEW COLUMNS TO IT'''
    dir_name= os.path.dirname(__file__) # Return the directory name of pathname _file_
    cfg       =load_config(os.path.join(dir_name, 'app/secret_config.yaml'))
    db_name   =cfg['db']['db_name']
    host      =cfg['db']['host']
    username=cfg['db']['username']
    password =cfg['db']['password']
    db= MySQLdb.connect( host, username, password, db_name)


    cursor= db.cursor()

    cursor.execute("ALTER TABLE `course` ADD `faculty_credit` CHAR(34) NOT NULL AFTER `parentCourse_id`")
    cursor.execute("ALTER TABLE `specialtopiccourse` ADD `faculty_credit` CHAR(34) NOT NULL AFTER `section`")


    db.close()



creating_new_columns_in_the_db()
