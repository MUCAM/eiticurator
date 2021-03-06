import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt

from eiticurator import Base, DBSession
from eiticurator.benutzerverwaltung.models import *

DB_USER = 'rautenbe'

PG = 'postgresql://' + DB_USER + '@ama-prod/mucam'
engine = sa.create_engine(PG, echo=True)

####################
# Benutzerverwaltung
####################



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

  # anlegen: organisationseinheiten und domains
  """
  d = Domain (domain = "MUCAM", beschreibung = "")
  session.add (d)
  session.commit()
  oes = ['MPDL', "MEA", "MPISOC"]
  for oe in oes:
    session.add(Organisationseinheit (
        domain = "MUCAM", oeinheit = oe))
  session.commit()
  """
  
  for user in all_users:
    print user
    u = Benutzer(
        nachname = user.familyname,
        vorname = user.givenname,
        titel = user.title_name,
        anzeigename = user.givenname + " " + user.familyname,
        raum = user.room_number or '',
        telefon = user.phone_number or '',
        fax = user.fax_number or '',
        einrichtung = user.institute,
        abteilung = user.department,
        funktion = '',
        von = user.since,
        bis = user.until,
        emailadresse = user.email
        )
    session.add(u)
    k = Konto(
      uid = user.id,
      uname = user.user_name,
      passwort_md5 = "",
      passwort_pam = user.password,
      passwort_des = "",
      aktiviert = True,
      oeinheit = user.institute,
      domain = 'MUCAM',
      anlegedatum = user.creation_time,
      beschreibung = "",
      zombie_monate = 3 * int(u.einrichtung=="MPISOC")
      )
    u.konto_objekt = k
  session.commit()
