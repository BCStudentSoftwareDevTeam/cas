from app.models import Building
from app.models import Rooms
from playhouse.migrate import *
from app.models import mainDB

def create_table():
  # create the table
  Building.create_table(True)

def add_buildings():

  # Get all of the Rooms in the system
  buildings = mainDB.execute_sql("SELECT DISTINCT building FROM rooms")

  # Create new buildings
  for building_result in buildings.fetchall():
    building = Building(name=building_result[0])
    building.save()

  rooms = mainDB.execute_sql("SELECT building, rID FROM rooms")

  for room_result in rooms.fetchall():
    building = Building.get(name=room_result[0])
    mainDB.execute_sql("UPDATE rooms SET building_id = ? WHERE rID = ?", (building.bID, room_result[1]))

def migrate_table():
  create_table()
  migrator = SqliteMigrator(mainDB)

  # add column
  foreign_key = IntegerField(null = True)
  #

  migrate(
    migrator.add_column('rooms', 'building_id', foreign_key)
  )

  add_buildings()

  migrate(
    migrator.drop_column('rooms', 'building')
    )


if __name__ == "__main__":
  migrate_table()





