from app.models import Course, RoomPreferences

courses = Course.select().where(Course.rid != None)

for course in courses:
    pref, created = RoomPreferences.get_or_create(course = course.cId)
    
    if pref.pref_1 == None:
        print("pref_1 is none")
        if pref.any_Choice == None:
            print("any_choice is none")
            if pref.none_Choice == None:
                print("none_choice is none")
                pref.any_Choice = 1
    else:
        print("Already had a pref")
        
    # if pref.pref_1 != None and pref.none_Choice == None:
    #     pref.any_Choice = 2
    
    if pref.pref_1 == None:
        
        pref.pref_1 = course.rid
        pref.any_Choice = 2
        
        print("Updated Preference for course {1} to {0}".format(pref.pref_1.rID, course.cId))
    else: 
        print("Course {0} has pref_1 of {1}".format(course.cId, pref.pref_1.rID))
    
    pref.save()
    print("Saved all things for {0}: any_choice: {1}".format(pref.course.cId, pref.any_Choice))
    
    
courses = Course.select().where(Course.rid == None)

prefs = RoomPreferences.select()

for pref in prefs:
    if pref.pref_1 == None and pref.any_Choice == None and pref.none_Choice == None:
        pref.any_Choice = 1
        pref.save()