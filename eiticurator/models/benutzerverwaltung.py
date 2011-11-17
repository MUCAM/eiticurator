"""
Kleine Dokumentaton:
"""
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt

from models import Base

print "benutzerverwaltung"

DB_USER = 'rautenbe'
PG = 'postgresql://' + DB_USER + '@ama-prod/mucam'
PG_SCHEMA = 'sandkasten'
TB_PREFIX = PG_SCHEMA + '.'


konto_gruppe_abbildungen = sa.Table(
    'konto_gruppe_abbildungen',
    Base.metadata,
    sa.Column(
      'uid',
      sa.Integer,
      sa.ForeignKey(TB_PREFIX + 'konten.uid')),
    sa.Column(
      'gid',
      sa.Integer,
      sa.ForeignKey(TB_PREFIX + 'gruppen.gid')),
    sa.PrimaryKeyConstraint('uid', 'gid'),
    schema = PG_SCHEMA
    )

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
      'emailadresse',
      sa.String,
      sa.ForeignKey (TB_PREFIX + 'emailadressen.emailadresse')
      ),
    sa.PrimaryKeyConstraint('uid', 'emailadresse'),
    schema = PG_SCHEMA
    )


class Domain(Base):
  """
  Domain macht das und das
  """
  __tablename__ = 'domains'
  __table_args__ = (
      {'schema': PG_SCHEMA})

  domain = sa.Column(sa.String, primary_key=True)
  beschreibung = sa.Column(sa.Text)

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
  oeinheit = sa.Column(sa.String)
  domain = sa.Column(sa.String)
  anlegedatum = sa.Column(
      sa.DateTime,
      default=dt.datetime.now(),
      nullable=False
      ) # PR: der default-Wert wird nicht innerhalb der Datenbank gesetzt!

  # many-to-many Konto<->Kontogruppe
#  gruppe_objects = orm.relationship(
#      'Gruppe',
#      secondary=konto_gruppe_abbildungen,
#      backref='konto_objects')
  organisationseinheit_object = orm.relationship(
      'Organisationseinheit',
      backref='konto_objects')
  emailadresse_objects = orm.relationship(
      'Emailadresse',
      backref='konto_object'
      )
  funktionskonto_object = orm.relationship(
      'Funktionskonto',
      backref='konto_object'
      )


class Funktionskategorie(Base):
  __tablename__ = 'funktionskategorien'
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )

  funktionskategorie = sa.Column(sa.String, primary_key=True)


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
  anzeigename = sa.Column(sa.String, nullable=False)
  funktionskategorie = sa.Column(
      sa.String,
      sa.ForeignKey(TB_PREFIX + 'funktionskategorien.funktionskategorie'))

  
class Emailadresse(Base):
  __tablename__ = 'emailadressen'
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
  emailadresse = sa.Column(sa.String, primary_key=True)
  emailtyp = sa.Column(sa.String, nullable=False)
  extern_erreichbar = sa.Column(sa.Boolean , nullable=False, default=False)
  uid = sa.Column(sa.ForeignKey(TB_PREFIX + 'konten.uid'))
  __mapper_args__ = {'polymorphic_on': emailtyp}


class VerteilerEmailadresse(Emailadresse):
  __tablename__ = 'verteiler_emailadressen'
  __mapper_args__ = {'polymorphic_identity': 'verteiler'}
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
  emailadresse = sa.Column(
      sa.ForeignKey(TB_PREFIX + 'emailadressen.emailadresse'),
      primary_key=True)

  emailadresse_object = orm.relationship(
      'Emailadresse',
      backref='verteiler_emailadresse_object'
      )


class AliasEmailadresse(Emailadresse):
  __tablename__ = 'alias_emailadressen'
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
  alias_emailadresse = sa.Column(
      sa.ForeignKey(TB_PREFIX + 'emailadressen.emailadresse'),
      primary_key=True)
  real_emailadresse = sa.Column(
      sa.ForeignKey(TB_PREFIX + 'emailadressen.emailadresse'),
      nullable=False)
  __mapper_args__ = {
      'polymorphic_identity': 'alias',
      'inherit_condition':alias_emailadresse==Emailadresse.emailadresse}


class Benutzer(Emailadresse):
  __tablename__ = 'benutzer'
  __mapper_args__ = {'polymorphic_identity': 'benutzer'}
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
  emailadresse = sa.Column(
      sa.String,
      sa.ForeignKey(TB_PREFIX + 'emailadressen.emailadresse'),
      primary_key=True)
  nachname = sa.Column(sa.String, nullable=False) # PR: weitere Bedingungen?
  vorname = sa.Column(sa.String, nullable=False) # PR: weitere Bedingungen?
  titel = sa.Column(sa.String, nullable=False, unique=False)
  anzeigename = sa.Column(sa.String, nullable=False, unique=True)
  raum = sa.Column(sa.String)
  einrichtung = sa.Column(sa.String , nullable=False)

  emailadresse_object = orm.relationship(
      'Emailadresse',
      backref='benutzer_object'
      )


class Funktionsbenutzer(Emailadresse):
  __tablename__ = 'funktionsbenutzer'
  __mapper_args__ = {'polymorphic_identity': 'funktionsbenutzer'}
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
  emailadresse = sa.Column(
      sa.String,
      sa.ForeignKey(TB_PREFIX + 'emailadressen.emailadresse'),
      primary_key=True,)
  name = sa.Column(sa.String, unique=True, nullable=False)


class Gruppe(Base):
  __tablename__ = 'gruppen'
  __table_args__ = (
      sa.PrimaryKeyConstraint('gid', 'name'),
      {'schema': PG_SCHEMA}
      )
  gid = sa.Column(sa.Integer, nullable=False, unique=True)
  name = sa.Column(sa.String(20), nullable=False, unique=True)
  gruppentyp = sa.Column(sa.String, nullable=False)
  __mapper_args__ = {'polymorphic_on': gruppentyp}


class Verteiler(Gruppe):
  __tablename__ = 'verteiler'
  __table_args__ = (
      sa.PrimaryKeyConstraint('gid', 'name'),
      sa.ForeignKeyConstraint(
        ['gid', 'name'],
        [TB_PREFIX + 'gruppen.gid', TB_PREFIX + 'gruppen.name']
        ),
      sa.ForeignKeyConstraint(
        ['emailadresse'],
        [TB_PREFIX + 'verteiler_emailadressen.emailadresse']),
      {'schema': PG_SCHEMA}
      )
  gid = sa.Column(sa.Integer)
  name = sa.Column(sa.String(20))
  emailadresse = sa.Column(sa.String, nullable=False)
  __mapper_args__ = {'polymorphic_identity': 'verteiler'}


if __name__ == '__main__':
  engine = sa.create_engine(PG, echo=True)
  Base.metadata.create_all(engine)
  Session = orm.sessionmaker(engine)
  session = Session()


