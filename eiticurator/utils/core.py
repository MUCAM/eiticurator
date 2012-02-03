from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import engine_from_config
from eiticurator import config

sm = sessionmaker()
DBSession = scoped_session(sm)

def getEngineByConfig(config=config):
  return engine_from_config(config, 'sqlalchemy.')

