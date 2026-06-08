from sqlalchemy.ext.declarative import declarative_base

# The single source of truth for the database base class
Base = declarative_base()

# All your table models (User, Role, Audit, etc.) should be defined 
# or imported here AFTER the line above.
