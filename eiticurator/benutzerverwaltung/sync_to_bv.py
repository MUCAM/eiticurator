import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt

from eiticurator import Base, DBSession

############
# einmalsync
############

PG_ama = 'postgresql://postgres@10.1.1.42/amalie'
engine_ama = sa.create_engine(PG_ama, echo=True)

Base_ama = declarative_base()
Base_ama.metadata.bind = engine_ama

class SyncUser(Base_ama):
  __tablename__ = "einmalsync"
  __table_args__ = {
      'autoload': True,
      'schema': "_activedirectory"}

####################
# Benutzerverwaltung
####################

from eiticurator.benutzerverwaltung.models import *


if __name__ == '__main__':
  # get ama data
  Session_ama = orm.sessionmaker(engine_ama)
  session_ama = Session_ama()
  all_users = session_ama.query(SyncUser).all()
  
  # schreibe benutzerverwaltung
  engine = sa.create_engine(PG, echo=True)
  Base.metadata.create_all(engine)
  Session = orm.sessionmaker(engine)
  #Session = DBSession()
  session = Session()

  
  for user in all_users:
    u = Benutzer(
        nachname = user.familyname,
        vorname = user.givenname,
        titel = user.title_name,
        anzeigename = user.givenname + " " + user.familyname,
        raum = user.room_number or '',
        einrichtung = user.institute,
        abteilung = user.department,
        funktion = '',
        since = user.since,
        until = user.until,
        emailadresse = user.email
        )
    session.add(u)
  session.commit()

