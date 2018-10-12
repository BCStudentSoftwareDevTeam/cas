from app.models import *
from peewee import *


new_user = User.create(
                    username = "brooksjam",
                    lastName = "Brooks",
                    firstName = "Jamiella",
                    isAdmin = False,
                    email = "brooksjam" + "@berea.edu",
                )
new_user.save()


