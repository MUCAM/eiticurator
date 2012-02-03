"""
Kleine Dokumentaton:
"""
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
import datetime as dt

from eiticurator import config

Base = declarative_base()

PG_SCHEMA = config['benutzerverwaltung.schema']

if PG_SCHEMA == '':
  PG_SCHEMA = None
  TB_PREFIX = ""
else:
  TB_PREFIX = PG_SCHEMA + '.' # 'TB' = 'table' 


konto_emailadresse_abbildungen = sa.Table(
    'konto_emailadresse_abbildungen',
    Base.metadata,
    sa.Column(
      'uid',
      sa.Integer,
      sa.ForeignKey (TB_PREFIX + 'konten.uid'),
      unique=True
      ),
    sa.Column(
      'eid',
      sa.Integer,
      sa.ForeignKey (TB_PREFIX + 'emailadressen.eid'),
      unique=True
      ),
    sa.PrimaryKeyConstraint('uid', 'eid'),
    schema = PG_SCHEMA
    )


class Domain(Base):
  __tablename__ = 'domains'
  __table_args__ = (
      {'schema': PG_SCHEMA})

  domain = sa.Column(sa.String, primary_key=True)
  beschreibung = sa.Column(sa.Text, nullable=False, default='')


class Organisationseinheit(Base):
  __tablename__ = 'organisationseinheiten'
  __table_args__ = (
      sa.PrimaryKeyConstraint('oeinheit', 'domain'),
      {'schema': PG_SCHEMA}
      )

  oeinheit = sa.Column(sa.String, nullable=False)
  domain = sa.Column(sa.String, sa.ForeignKey(TB_PREFIX + 'domains.domain'))


class Konto(Base):
  __tablename__ = 'konten'
  __table_args__ = (
      sa.ForeignKeyConstraint(
        ['oeinheit', 'domain'],
        [TB_PREFIX + 'organisationseinheiten.oeinheit',
        TB_PREFIX + 'organisationseinheiten.domain']
        ),
      {'schema': PG_SCHEMA}
      )

  uid = sa.Column(sa.Integer, primary_key=True)
  uname = sa.Column(sa.String(20), unique=True, nullable=False)
  passwort_unix = sa.Column(sa.String, nullable=False, default="***")
  passwort_pam = sa.Column(sa.String, nullable=False, default="***")
  aktiviert = sa.Column(sa.Boolean, nullable=False, default=False)
  oeinheit = sa.Column(sa.String, nullable=False)
  domain = sa.Column(sa.String, nullable=False)
  anlegedatum = sa.Column(
      sa.DateTime,
      default=dt.datetime.now(),
      nullable=False
      ) # PR: der default-Wert wird nicht innerhalb der Datenbank gesetzt!
  beschreibung = sa.Column(
      sa.Text, nullable=False, default='')
  zombie_monate = sa.Column(sa.Integer, nullable=False, default=0)
  bearbeitet = sa.Column(sa.DateTime, nullable=False,
      default=dt.datetime.now())

  # many-to-many Konto<->Kontogruppe
  organisationseinheit_object = orm.relationship(
      'Organisationseinheit',
      backref='konto_objects')
  emailadresse_objects = orm.relationship(
      'Emailadresse',
      secondary=konto_emailadresse_abbildungen,
      backref='konto_object'
      )
  funktionskonto_object = orm.relationship(
      'Funktionskonto',
      backref='konto_object'
      )


class Funktionskonto(Base):
  __tablename__ = 'funktionskonten'
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
 
  uid = sa.Column(
      sa.Integer,
      sa.ForeignKey(TB_PREFIX + 'konten.uid'),
      primary_key=True,
      )
  passwort_plain = sa.Column(sa.String, nullable=False, default='')

  
class Emailadresse(Base):
  __tablename__ = 'emailadressen'
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
  eid = sa.Column(sa.Integer, primary_key=True)
  emailadresse = sa.Column(sa.String, unique=True, nullable=False)
  emailtyp = sa.Column(sa.String, nullable=False)
  extern_erreichbar = sa.Column(sa.Boolean , nullable=False, default=False)
  __mapper_args__ = {'polymorphic_on': emailtyp}

  emailadresse_alias_objects = orm.relationship(
      'EmailadresseAlias',
      primaryjoin='Emailadresse.eid==EmailadresseAlias.referenz_eid',
      backref='emailadresse_object')

  emailadresse_aliasse = association_proxy(
      'emailadresse_alias_objects',
      'emailadresse')


class Verteiler(Emailadresse):
  __tablename__ = 'verteiler'
  __mapper_args__ = {'polymorphic_identity': 'verteiler'}
  __table_args__ = (
      sa.ForeignKeyConstraint(
        ['oeinheit', 'domain'],
        [TB_PREFIX + 'organisationseinheiten.oeinheit',
        TB_PREFIX + 'organisationseinheiten.domain']
        ),
      {'schema': PG_SCHEMA}
      )
  eid = sa.Column(
      sa.ForeignKey(TB_PREFIX + 'emailadressen.eid'),
      primary_key=True)
  oeinheit = sa.Column(sa.String, nullable=False)
  domain = sa.Column(sa.String, nullable=False)
  gname = sa.Column(sa.Text)
  gid = sa.Column(sa.Integer)


class EmailadresseAlias(Emailadresse):
  __tablename__ = 'emailadressen_alias'
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
  eid = sa.Column(
      sa.Integer,
      sa.ForeignKey(TB_PREFIX + 'emailadressen.eid'),
      primary_key=True)
  referenz_eid = sa.Column(
      sa.ForeignKey(TB_PREFIX + 'emailadressen.eid'),
      nullable=False)
  __mapper_args__ = {
      'polymorphic_identity': 'alias',
      'inherit_condition':Emailadresse.eid==eid}

  def __init__(self, emailadresse_alias):
    self.emailadresse = emailadresse_alias

  def set_parent(self):
    tmp = self.emailadresse
    self.emailadresse = 'dummy@dummy.dummy'
    orm.object_session(self).commit()
    self.emailadresse = self.emailadresse_object.emailadresse
    self.emailadresse_object.emailadresse = tmp

class Benutzer(Emailadresse):
  __tablename__ = 'benutzer'
  __mapper_args__ = {'polymorphic_identity': 'primaer'}
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
  eid = sa.Column(
      sa.Integer,
      sa.ForeignKey(TB_PREFIX + 'emailadressen.eid'),
      primary_key=True)
  nachname = sa.Column(sa.String, nullable=False) # PR: weitere Bedingungen?
  vorname = sa.Column(sa.String, nullable=False) # PR: weitere Bedingungen?
  titel = sa.Column(sa.String, nullable=False, default="")
  raum = sa.Column(sa.String, nullable=False)
  telefon = sa.Column(sa.String, nullable=False, default="")
  fax = sa.Column(sa.String, nullable=False, default="")
  einrichtung = sa.Column(sa.String , nullable=False)
  abteilung = sa.Column(sa.Text, nullable=False, default='')
  funktion = sa.Column(sa.Text, nullable=False, default='')
  von = sa.Column(sa.DateTime, nullable=False)
  bis = sa.Column(sa.DateTime, nullable=False)
  bearbeitet = sa.Column(sa.DateTime, nullable=False,
      default=dt.datetime.now())

  emailadresse_object = orm.relationship(
      'Emailadresse',
      backref='benutzer_object'
      )

bv_objects = [
    Benutzer,
    Domain,
    Emailadresse,
    EmailadresseAlias,
    Funktionskonto,
    Konto,
    Verteiler,
    Organisationseinheit]

def initialize_sql(engine):
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

if __name__ == '__main__':
  engine = sa.create_engine(PG, echo=True)
  Base.metadata.create_all(engine)
  Session = orm.sessionmaker(engine)
  session = Session()
