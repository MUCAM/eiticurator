from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import engine_from_config

from eiticurator.utils.config import LoadConfig

config = LoadConfig('db_setup.ini')
#DBSession = scoped_session(sessionmaker(twophase=True))
DBSession = scoped_session(sessionmaker())
Base = declarative_base()

from benutzerverwaltung.models import *

engine = engine_from_config(config, 'sqlalchemy.')

#def initialize_sql(engine):
#    DBSession.configure(bind=engine)
#    Base.metadata.bind = engine
#    Base.metadata.create_all(engine)

#initialize_sql(engine)
#session = DBSession ()
