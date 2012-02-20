from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import engine_from_config

from eiticurator.utils.config import ConfiCurator

cc = ConfiCurator()
config = cc.config
Base = declarative_base()
DBSession = scoped_session(sessionmaker())

cc = ConfiCurator()

def initialize_sql(engine):
  DBSession.configure(bind=engine)
  Base.metadata.bind = engine
  Base.metadata.create_all(engine)

def get_engine():
  return engine_from_config(cc.config, 'sqlalchemy.')

def get_session():
  engine = get_engine()
  initialize_sql(engine)
  session = DBSession()
  return session
