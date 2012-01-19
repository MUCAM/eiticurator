import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt

from eiticurator import Base, DBSession, engine
from eiticurator.benutzerverwaltung.models import *
from eiticurator.benutzerverwaltung.models import PG_SCHEMA, TB_PREFIX

#####################
# staff_data02_export
#####################

PG_ama = 'postgresql://postgres@data02/amalie'
engine_ama = sa.create_engine(PG_ama, echo=True)

class SyncUser(Base):
  __tablename__ = "staff_data02_export"
  __table_args__ = (
      sa.PrimaryKeyConstraint('id', 'id'),
      {
      'autoload': True,
      'autoload_with': engine_ama,
      'schema': "admin",
      })

####################
# Benutzerverwaltung
####################

class StaffData02Export_Benutzer_Abbildung(Base):
  __tablename__ = "staff_data02_export_benutzer_abbildungen"
  __table_args__ = (
      {'schema': PG_SCHEMA,
       })
  id = sa.Column(
      sa.Integer,
      primary_key=True)
  eid = sa.Column(
      sa.Integer,
      sa.ForeignKey(TB_PREFIX + 'emailadressen.eid'),
      primary_key=True)


if __name__ == '__main__':
  # get ama data
  binds = {}
  [binds.update({bv_object:engine}) for bv_object in bv_objects]
  binds[SyncUser] = engine_ama
  binds[StaffData02Export_Benutzer_Abbildung] = engine
  DBSession.configure(binds=binds)
  bv_tables = []
  Base.metadata.create_all(engine, [
    StaffData02Export_Benutzer_Abbildung.__table__,
    Benutzer.__table__,
    Domain.__table__,
    Emailadresse.__table__,
    EmailadresseAlias.__table__,
    Funktionskonto.__table__,
    Konto.__table__,
    konto_emailadresse_abbildungen,
    Organisationseinheit.__table__,
    Verteiler.__table__])
  session = DBSession()
  all_users = session.query(SyncUser).all()
 
  # anlegen: organisationseinheiten und domains
  try:
    d = Domain (domain = "MUCAM", beschreibung = "")
    session.add (d)
    session.commit()
    oes = ['MPDL', "MEA", "MPISOC", "PSY"]
    for oe in oes:
      session.add(Organisationseinheit (
          domain = "MUCAM", oeinheit = oe))
    session.commit()
  except:
    session.rollback()
  
  for user in all_users:
    if user.email is not None:
      u = Benutzer(
          nachname = user.familyname,
          vorname = user.givenname,
          titel = user.title,
          raum = user.room_number or '',
          telefon = user.phone_number or '',
          fax = user.fax_number or '',
          einrichtung = user.institute,
          abteilung = user.department,
          funktion = user.function,
          extern_erreichbar = True,
          von = user.since,
          bis = user.until,
          emailadresse = user.email
          )
      session.add(u)
      session.flush()
      print "---------------------- >>>>>> " + u.emailadresse
      print "---------------------- >>>>>> " + str(u.eid)
      d2ap = StaffData02Export_Benutzer_Abbildung(id=user.id, eid=u.eid)
      session.add(d2ap)
      if user.department == "Sozialpolitik":
        oeinheit = "MEA"
      else:
        oeinheit = user.institute
      k = Konto(
        uid = user.id,
        uname = user.user_name,
        passwort_unix = "",
        aktiviert = True,
        oeinheit = oeinheit,
        domain = 'MUCAM',
        beschreibung = "",
        zombie_monate = 3 * int(u.abteilung=="Sozialrecht")
        )
      u.konto_object.append(k)
  session.commit()
