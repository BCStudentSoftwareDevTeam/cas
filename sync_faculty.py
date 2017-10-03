from ldap3 import Server, Connection, ALL
from peewee import *
from os import path, remove
from app.models import *
import argparse

# Create database connection and model
database_path = "LDAP.db"
database = SqliteDatabase(database_path)

class Faculty(Model):
    fID               = PrimaryKeyField()
    username          = CharField(unique = True)
    bnumber           = TextField(null = True)
    lastname          = TextField(null = True)
    firstname         = TextField(null = True)

    class Meta:
        database = database

class Staff(Model):
    sID               = PrimaryKeyField()
    username          = CharField(unique = True)
    bnumber           = TextField(null = True)
    lastname          = TextField(null = True)
    firstname         = TextField(null = True)
    class Meta:
        database = database


def connect_to_server(user,password):
    server = Server ('berea.edu', port=389, use_ssl=False, get_info='ALL')
    # conn   = Connection (server, user=skt['ldap']['user'], password=skt['ldap']['pass'])
    conn   = Connection (server, user=user, password=password)
    if not conn.bind():
        print(conn.result)
        raise Exception("BindError")
    return conn

def grab_faculty(connection):
    return grab_data(connection, "Faculty")

def grab_staff(connection):
    return grab_data(connection,"Staff")

def grab_data(connection, description):
    # search_base and search_filter are the parameters
    connection.search('dc=berea,dc=edu',
      '(description=%s)' % (description),
      attributes = ['samaccountname', 'givenname', 'sn', 'employeeid']
      )

    return connection.entries

def grab_key(entry, key):
    if key in entry:
        return entry[key]
    else:
        return None


def dump_to_database(entries, Table):
    for entry in entries:
        if grab_key(entry,"samaccountname") == "ldapfaculty":
            continue
        row = Table(
            username          = grab_key(entry,'samaccountname'),
            bnumber           = grab_key(entry,'employeeid'),
            lastname          = grab_key(entry,'sn'),
            firstname         = grab_key(entry,'givenname')
        )
        row.save()


def main(user,password):
    pull_database(user, password)
    print("Adding new members")
    add_members()
    
def add_members():
    current_users = User.select(User.username)
    user_list = list()
    for user in current_users:
        user_list.append(user.username)
    users = Faculty.select().where( (Faculty.username << user_list))
    print("Updating %s users" %(str(len(users))))
    for user in users:
        if user.bnumber is None:
            print(user.username)
            continue
        updated_user = User.get(User.username == user.username)
        updated_user.bNumber = user.bnumber
        updated_user.email = user.username+ "@berea.edu"
        updated_user.save()
        
    users = Faculty.select().where(~(Faculty.username << user_list))
    print("Adding %s users" %(str(len(users))))
    for user in users:
        if user.firstname is None or user.lastname is None:
            print(user.username + " has null fields skipping")
            continue
        new_user = User.create(
                username = user.username,
                bNumber = user.bnumber,
                lastName = user.lastname,
                firstName = user.firstname,
                isAdmin = False,
                email = user.username + "@berea.edu",
            )
        new_user.save()
def pull_database(user,password):
    print("Connecting to Database")
    database.connect()
    print("Dropping and creating tables")
    if path.isfile(database_path):
        try:
            database.drop_tables([Faculty, Staff])
        except Exception:
            pass
    database.create_tables([Faculty, Staff])
    print("Connecting to server")
    connection = connect_to_server(user,password)
    print("Grabbing data")
    faculty = grab_faculty(connection)
    # staff = grab_staff(connection)
    print("Dumping Data")
    dump_to_database(faculty, Faculty)
    # dump_to_database(Staff, Staff)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pull and Sync Faculty from LDAP')
    parser.add_argument('--user',required=True, help='Username for LDAP')
    parser.add_argument('--password', required=True, help="Password for LDAP")
    args = parser.parse_args()
    
    main(args.user, args.password)

