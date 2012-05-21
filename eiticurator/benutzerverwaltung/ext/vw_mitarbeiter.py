import sqlalchemy as sa
import datetime as dt

import eiticurator as etc
from eiticurator import Base, DBSession, cc
from eiticurator.benutzerverwaltung.models import *
from eiticurator.benutzerverwaltung.models import PG_SCHEMA, TB_PREFIX

AKTUALISIERT = cc.config['benutzerverwaltung.vw_mitarbeiter_aktualisiert']
NEU = cc.config['benutzerverwaltung.vw_mitarbeiter_neu']
MITARBEITER = cc.config['benutzerverwaltung.vw_mitarbeiter']
ECHO = "True" == cc.config['sqlalchemy.echo']
SCHEMA = cc.config['benutzerverwaltung.schema']

engine = etc.get_engine()

class MitarbeiterAktualisiert(Base):
  __tablename__ = AKTUALISIERT
  __table_args__ = (
      sa.PrimaryKeyConstraint('eid'),
      {
      'autoload': True,
      'autoload_with': engine,
      'schema': SCHEMA,
      })


class MitarbeiterNeu(Base):
  __tablename__ = NEU
  __table_args__ = (
      sa.PrimaryKeyConstraint('mid'),
      {
      'autoload': True,
      'autoload_with': engine,
      'schema': SCHEMA,
      })

      
class Mitarbeiter(Base):
  __tablename__ = MITARBEITER
  __table_args__ = (
      sa.PrimaryKeyConstraint('mid'),
      {
      'autoload': True,
      'autoload_with': engine,
      'schema': SCHEMA,
      })
