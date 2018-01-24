from app.models import mainDB
from playhouse.migrate import SqliteMigrator

class Base(object):
  def __init__(self):
    self.migrator = SqliteMigrator(mainDB)
    