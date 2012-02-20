import sqlalchemy as sa
import datetime as dt

import eiticurator as etc
from eiticurator import Base, DBSession, cc
from eiticurator.benutzerverwaltung.models import *
from eiticurator.benutzerverwaltung.models import PG_SCHEMA, TB_PREFIX

PG_AMA = cc.config['mucam.pg_ama']
PG_MUCAM = cc.config['mucam.pg_mucam']
ECHO = "True" == cc.config['sqlalchemy.echo']

engine_ama = sa.create_engine(PG_AMA, echo=ECHO)
engine_mucam = sa.create_engine(PG_MUCAM, echo=ECHO)

#####################
# staff_data02_export
#####################

class SyncUser(Base):
  __tablename__ = "staff_data02_export"
  __table_args__ = (
      sa.PrimaryKeyConstraint('id'),
      {
      'autoload': True,
      'autoload_with': engine_ama,
      'schema': "admin",
      })

  def __repr__(self):
    return """SyncUser:
      familyname: %s,
      givenname: %s,
      title: %s,
      room: %s,
      phone_number: %s,
      fax: %s,
      institute: %s,
      department: %s,
      since: %s,
      until: %s,
      user_name: %s,
      email: %s,
      function: %s
      """ %(
          self.familyname,
          self.givenname,
          self.title,
          self.room,
          self.phone_number,
          self.fax,
          self.institute,
          self.department,
          self.since,
          self.until,
          self.user_name,
          self.email,
          self.function)

class SyncStaff(Base):
  __tablename__ = "staff"
  __table_args__ = (
      sa.PrimaryKeyConstraint('id'),
      {
      'autoload_with': engine_ama,
      'schema': "admin",
      })

  id = sa.Column(sa.Integer)
  email = sa.Column(sa.String('email'))
  user_name = sa.Column(sa.String('user_name'))


class SyncAliasse(Base):
  __tablename__ = "mailnames_activedirectory"
  __table_args__ = (
      sa.PrimaryKeyConstraint('mail'),
      {
      'autoload': True,
      'autoload_with': engine_mucam,
      'schema': "migration_ironport",
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

def get_session():
  """
  Bemerkung: diese Funktion ist etwas komplizierter, da die session auf drei
  verschiedenen engines basiert.
  """
  engine = etc.get_engine()
  binds = {}
  [binds.update({bv_object:engine}) for bv_object in bv_objects]
  binds[SyncUser] = engine_ama
  binds[SyncAliasse] = engine_mucam
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
  return session

def insert_neu_Mitarbeiter():
  ns = session.query(SyncUser).filter_by(email=None).all()
  for user in ns:
    email = raw_input("Bitte E-Mail fuer %s eingeben: " %(user.familyname))
    uname = raw_input("Bitte uname fuer %s eingeben: " %(user.familyname))
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
        emailadresse = email
        )
    if user.department == "Sozialpolitik":
      oeinheit = "MEA"
    else:
      oeinheit = user.institute
    k = Konto(
        uid = user.id,
        uname = uname,
        passwort_unix = "",
        aktiviert = True,
        oeinheit = oeinheit,
        domain = 'MUCAM',
        beschreibung = "",
        zombie_monate = 3 * int(u.abteilung=="Sozialrecht")
        )
    session.add(u)
    u.konto_object.append(k)
    session.flush()
    session.commit()
