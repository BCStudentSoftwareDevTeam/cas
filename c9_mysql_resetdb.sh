# Drops your existing c9 database
# Creates the c9 database, empty
# Imports data from cas.sql file
# To run the file, enter "source c9_mysql_resetdb.sh" into the terminal

{           # Try
    mysql -u $C9_USER -e "DROP DATABASE c9"
} || {}     # Catch
{
    mysql -u $C9_USER -e "CREATE DATABASE c9"
} || {}

# cas.sql is exported from the production server; make sure the file is in 
# the same directory as this file

mysql -u $C9_USER c9 < cas.sql