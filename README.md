[TOC]
#Installation#
## Requirements ##
* Python 2.7
* One of the following: linux, unix, mac or windows (with attachments)
* Git 

## Creating Development Environment ##

1. **Fork** the repository from BitBucket and rename to your project.

2. If working on a **local machine**, then clone the repo from your terminal

``` bash
git clone https://username@bitbucket.org/username/repositoryname.git
source setup.sh
python create_db.py
python app.py
```
You can now check your localhost to see if it deployed correctly.

3. If working on a **cloud9** account follow instructions below to create a new workspace.
    1. Input your project name and description
    2. Get the git URL of your forked reposistory from BitBucket
    3. You should get the SSH URL, it should look something like: git@bitbucket.org:username/repositoryname.git
    4. Now paste the git URL into "Clone from Git URL" field in cloud9.
``` bash
source setup.sh
python create_db.py
python app.py
``` 
If you are succesful you will see something like:
``` bash
Starting application
Running server at http://0.0.0.0:8080/
```
Click the link in your terminal to check if it is deployed correctly.

# Working with the flask template #
## File Hierarchy ##
```
- Project Name
   - App
      -static
      -templates
        -start.html
      - __init__.py
      - allImports.py
      - config.yaml
      - models.py
      - start.py # this an example of a python file that renders a page
   - Data
       - db.sqlite
   - Venv
   - app.py
   - create_db.py
   - setup.sh
```
Above you will find the file structure for the flask template. You will be mostly working with the app/ directory.
Some **important** files and directories.

* models.py - This file contains the database schema or the tables and columns that will be in database.
If you want to make a new table then you will add a class to this file, see the example in the models.py file.
Once you are done making changes to this file run create_db.py to make the changes in the database.

* App/ directory - This directory will contain a python module in order for python files to be recognized they must be added to the \_\_init\_\_.py file in this directory.

* start.py - This file is a very quick example of a python file that will render a page. This file processes and renders the start.html file located under templates.

## Example for creating a new view ##
If I wanted to create a new webpage then I would do the following.

* Create your python file inside of the app/ directory. Here you will include the decorator @app.route as seen in other files
```python
        from allImports import *
        @app.route("/example", methods = ["GET"])
        def example():
            return render_template("example.html", cfg = cfg)
```
* Create HTML file inside of the templates folder and make sure to give it the **same name** as the one you used in the python file.
```HTML
{% extends "base.html" %}

{% block body %}

<h1> Header 1 </h1>
<p> Example Paragraph </p>

{% endblock %}
```
* Import the python file you created inside the \_\_init\_\_.py file.
```Python
from app import example.py
```

## Reading and Writing to the database ##

In order to read from a database you will need to make a query to get the data. You can find out more about queries at [the peewee site](http://docs.peewee-orm.com/en/latest/peewee/querying.html)
one quick example of a query would be the following:
```python
query = tableName.get( condition = something )
```
This will return a python object that will have the data as attributes. You can pass this object to the html file. You can access this data by typing query.Column. 

NOTE: Needs more details on asking query to finish reading and writing to the database.

## Documentation links ##

* [Jinja Documentation](http://jinja.pocoo.org/)
* [Peewee Documentation](http://docs.peewee-orm.com/en/latest/)
* [Git documentation](https://git-scm.com/documentation)
* [Flask Documentation](http://flask.pocoo.org/docs/0.10/)


## To run mysql migration scripts (mysql_migration.py and migrate_data.py)
1. Create mysql database: mysql-ctl install
2. Look for the below section in config.yaml and edit with your cloud9 username
      db_name: c9
      host: localhost
      password: ''
      username: nelsonk 
3. Run python mysql_migration.py which will create the mysql tables 
4. Run python migrate_data.py to transfer data from db.sqlite to newly created mysql. 
Depending on which version of the Cas db.sqlite you have, you might need to run python update_schema.py first. 
Also make sure that the models.py file is directed towards the sqlite database file.

If it is directed towards sqlite, the code to create the database connection will look like this: 
    # Create a database
    from app.loadConfig import *
    here = os.path.dirname(__file__)
    cfg       = load_config(os.path.join(here, 'config.yaml'))
    db	  = os.path.join(here,'../',cfg['databases']['dev']) 
    # mainDB    = SqliteDatabase(cfg['databases']['dev'])
    mainDB    = SqliteDatabase(db,
                              pragmas = ( ('busy_timeout',  100),
                                          ('journal_mode', 'WAL')
                                      ),
                              threadlocals = True
                              )
5. Once you run the migrate_data script, if successful, all data from the db.sqlite 
should have migrated to the mysql database created at step 1.  

6. Now, to run the application with the newly created mysql table, make sure that models.py is directed towards mysql: 
If it is directed towards mysql, the code to create the database connection will look like this: 
    # Create a database
    from app.loadConfig import *
    dir_name   = os.path.dirname(__file__) # Return the directory name of pathname _file_
    cfg        = load_config(os.path.join(dir_name, 'config.yaml'))
    db_name    = cfg['db']['db_name']
    host       = cfg['db']['host']
    username   = cfg['db']['username']
    password   = cfg['db']['password']
    
    mainDB     = MySQLDatabase ( db_name, host = host, user = username, passwd = password)

**** I would highly suggest that you keep two models.py files one with sqlite and one with mysql so you could transition between the two if needs be.

7. Delete all the db.sqlite files or rename them something other than db.sqlite 
8. Run python app.py and everything should work as usual 


With mysql, you will not be able to use DB browser to visualize the data like we used to with sqlite. You will have to run: 
1. mysql-ctl cli in the terminal
2. use c9; *remember that c9 is the default name for any mysql database created on cloud9
3. then you can type any SQL commands you want to see any data you want
