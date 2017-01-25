from app.models import mainDB
import csv
import sys

'''VARIABLES THAT CAN CHANGE'''
DEBUG = True
#User table details
userTable = 'user'
usersColumnNames   = ('username','firstName','lastName','email','isAdmin','lastEdited')
usernameIndex = 0
#instructorcourse table details
instrTable = 'instructorcourse'
instrColumnNames = ('id','username_id','course_id')
#course table details
courseTable = 'course'
courseID    = 'cId'
#CSV files
csvDuplicates = 'duplicateUsers.csv'
csvOldCourses = 'oldCourses.csv'
'''DEBUG PRINTS'''
def debugExcept(e):
  lineNum = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
  debugPrint(e)
  debugPrint(lineNum)
def debugPrint(x):
  if DEBUG:
    sys.stderr.write(str(x))
    sys.stderr.write('\n')
    sys.stderr.write('-----------------\n')
'''QUERY CREATION'''    
def userSelectQuery():
  #Get the usernames that appear more than once
  query = 'SELECT * FROM '+userTable+' GROUP BY lower('
  query = query+usersColumnNames[usernameIndex]+') HAVING COUNT(*)>1'
  debugPrint('SELECT QUERY: \n'+query)
  return query

def userDeleteQuery(user):
  delete = 'DELETE FROM '+userTable+' WHERE '
  delete = delete+usersColumnNames[usernameIndex] #Add username
  delete = delete+' = \''+user[usernameIndex]+'\';'
  debugPrint('DELETE QUERY: \n'+delete)
  return delete

def removeDuplicateUsers():
  try:
    #Get the lowercase usernames that appear more than once 
    query = userSelectQuery()
    query = mainDB.execute_sql(query) #Execute and Get results
    result = query.fetchall()
    debugPrint(result)
    if result is not None:
      try:
        f = open(csvDuplicates,'wt') #Set up CSV file
        writer = csv.writer(f)
        writer.writerow(usersColumnNames)
        for user in result: #Loop through result
          debugPrint(user)
          if user[usernameIndex] == user[usernameIndex].lower():
            pass #don't delete rows where the username is already lowercase
          else:  #write rows that we are deleteing to csv file
            writer.writerow(user)
            delete = userDeleteQuery(user)
            query  = mainDB.execute_sql(delete)
      except Exception as e:
        debugExcept(e)
      finally:
        f.close
    else:
      msg = 'No duplicate users were found'
      debugPrint(msg)
  except Exception as e:
    debugExcept(e)
    
def cleanInstructorCourse():
  try:
    query  = "SELECT id, username_id, course_id FROM instructorcourse LEFT JOIN course ON course.cId = instructorcourse.course_id WHERE course.cId IS NULL;"
    query  = mainDB.execute_sql(query) #Execute and Get results
    result = query.fetchall()
    if result is not None:
      try:
        f = open(csvOldCourses,'wt') #Set up CSV file
        writer = csv.writer(f)
        writer.writerow(instrColumnNames)
        for row in result: #Loop through result
          writer.writerow(row)
          delete = "DELETE FROM instructorcourse WHERE id = "+str(row[0])+";"
          debugPrint(str(row)+'\n'+delete)
          query = mainDB.execute_sql(delete)
      except Exception as e:
        debugExcept(e)
      finally:
        f.close
    else:
      msg = 'No old course_id found'
      debugPrint(msg)  
  except Exception as e:
    debugExcept(e)
    
def cleanInstructorCourseChange():
  try:
    select = "SELECT * FROM instructorcoursechange WHERE username_id NOT IN (SELECT username FROM user)"
    query  = mainDB.execute_sql(select)
    result = query.fetchall()
    if result is not None:
      for row in result:
        delete = "DELETE FROM instructorcoursechange WHERE id = "+str(row[0])+";"
        debugPrint(str(row)+'\n'+delete)
        query = mainDB.execute_sql(delete) 
  except Exception as e:
    debugExcept(e)
  
def main():
    removeDuplicateUsers()
    cleanInstructorCourse()
    cleanInstructorCourseChange()
    
main();