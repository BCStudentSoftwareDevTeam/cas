# First, create an environmental variable for my username in 
# ~/.profile by adding the following line with your c9 username

# export USERNAME="sheggen1"

{           # Try
    mysql -u $C9_USER -e "DROP DATABASE c9"
} || {}     # Catch
{
    mysql -u $C9_USER -e "CREATE DATABASE c9"
} || {}

# cas.sql is exported from the production server; make sure the file is in 
# the same directory as this file

mysql -u $C9_USER c9 < cas.sql