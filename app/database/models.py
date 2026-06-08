from sqlalchemy.ext.declarative import declarative_base

# The single source of truth for your database models
Base = declarative_base()

# After defining Base, you can import your models here to register them
# from .user import User
# from .role import Role
