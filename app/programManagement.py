from allImports import *
from updateCourse import DataUpdate
from app.logic.authorization import must_be_admin


@app.route("/admin/programManagement/<pid>", methods=["GET"])
@must_be_admin
def adminProgramManagement(pid):
    
    users = User.select().order_by(User.lastName)
    divisions = Division.select()
    programs  = Program.select()
    program = Program.get(Program.pID == pid)
    programChairs = {}
    programChairs[program.pID] = ProgramChair.select().where(ProgramChair.pid == program.pID)
    
    return render_template("editProgram.html",
                            program       = program,
                            programChairs = programChairs,
                            users         = users,
                            divisions     = divisions,
                            programs      = programs)
  