# Drops your existing c9 database
# Creates the c9 database, empty
# Imports data from cas.sql file
# To run the file, enter "source c9_mysql_resetdb.sh" into the terminal

{           # Try
    mysql -u root -proot -e "DROP DATABASE cas"
} || {}     # Catch
{
    mysql -u root -proot -e "CREATE DATABASE cas"
} || {}

# cas.sql is exported from the production server; make sure the file is in 
# the same directory as this file

mysql -u root -proot cas < cas.sql
