#Controller for Assign button (roomResolutionView) sending the assignment of a course to new room to database
@app.route("/assignRoom/<cId>", method=["POST"]) #Updating database with new rid for course

def assignRoom(cId=0)  #TODO: refactor in html using <form>
    data = request.form
    room = data["roomButton"]
    course = (Course.get(course.cId = cId)) #Gets course ID from database
    course.room = room
    course.save()  #Updates database
    return(url_for('roomResolution')