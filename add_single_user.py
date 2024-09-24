from app.models.models import User
from peewee import *


new_user = User.create(
                    username = "jonesam",
                    lastName = "Jones",
                    firstName = "Amy",
                    isAdmin = False,
                    email = "jonesam@berea.edu",
                )
new_user.save()


