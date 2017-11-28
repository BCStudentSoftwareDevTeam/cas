from app.models import *
    
    
mainDB.execute_sql('CREATE TABLE schema_migrations (version integer PRIMARY KEY);')

