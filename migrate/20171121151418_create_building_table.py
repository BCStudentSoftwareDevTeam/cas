"""
  everything that should be migrated happens there
  to migrate use playhouse
  http://docs.peewee-orm.com/en/latest/peewee/database.html#schema-migrations
"""
    
from app.models import *
from playhouse.migrate import *
from .base import Base


class create_building_table(Base):
    def __init__(self):
      Base.__init__(self)

    def up(self):
        """ migrates file to new schema """
        # preparation code goes here
        
        self.create_table()
  
        # add column
        foreign_key = IntegerField(null = True)
        # 

        migrate(
          self.migrator.add_column('rooms', 'building_id', foreign_key)
        )
  
        self.add_buildings()
  
        migrate(
          self.migrator.drop_column('rooms', 'building')
        )
        
        
    def down(self):
        """ reverts migration """
        # preparation code goes here
        migrate(
             # schema migration happens here
        )
    
    def create_table(self):
      # create the table
      Building.create_table(True)
      
    def add_buildings(self):
  
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
    
  
  