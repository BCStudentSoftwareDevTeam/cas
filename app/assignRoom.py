#Controller for Assign button (roomResolutionView) sending the assignment of a course to new room to database
@app.route("/assignRoom/<cId>", method=["POST"]) #Updating database with new rid for course

def assignRoom(cId=0)
    data = request.form
    room = data["roomButton"]
    course = (Course.get(course.cId = cId))
    course.room = room
    course.save()
    return(url_for('roomResolution')