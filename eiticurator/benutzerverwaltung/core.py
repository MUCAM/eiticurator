"""
Kleine Dokumentaton:



"""


import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt

DB_USER = 'rautenbe'
PG = 'postgresql://' + DB_USER + '@ama-prod/mucam'
PG_SCHEMA = 'sandkasten'
TB_PREFIX = PG_SCHEMA + '.'

Base = declarative_base()

konto_kontogruppe_abbildungen = sa.Table(
    'konto_kontogruppe_abbilgungen',
    Base.metadata,
    sa.Column(
      'uid',
      sa.Integer,
      sa.ForeignKey(TB_PREFIX + 'konten.uid')),
    sa.Column(
      'kgid',
      sa.Integer,
      sa.ForeignKey(TB_PREFIX + 'kontogruppen.kgid')),
    sa.PrimaryKeyConstraint('uid', 'kgid'),
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
  kontogruppen = orm.relationship(
      'Kontogruppe',
      secondary=konto_kontogruppe_abbildungen,
      backref='konten')
  organisationseinheit = orm.relationship(
      'Organisationseinheit',
      backref='konten')


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
  extern_erreichbar = sa.Column(sa.Boolean , nullable=False, default=False)


class VerteilerEmailadresse(Base):
  __tablename__ = 'verteiler_emailadressen'
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
  emailadresse = sa.Column(
      sa.String,
      sa.ForeignKey(TB_PREFIX + 'emailadressen.emailadresse'),
      primary_key=True)


class KontoEmailadresse(Base):
  __tablename__ = 'konto_emailadressen'
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
  emailadresse = sa.Column(
      sa.String,
      sa.ForeignKey(TB_PREFIX + 'emailadressen.emailadresse'),
      primary_key=True)
  uid = sa.Column(
      sa.Integer,
      sa.ForeignKey(TB_PREFIX + 'konten.uid'))


class Benutzer(Base):
  __tablename__ = 'benutzer'
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
  emailadresse = sa.Column(
      sa.String,
      sa.ForeignKey(TB_PREFIX + 'emailadressen.emailadresse'),
      primary_key=True)
  nachname = sa.Column(sa.String, nullable=False) # PR: weitere Bedingungen?
  vorname = sa.Column(sa.String, nullable=False) # PR: weitere Bedingungen?
  anzeigename = sa.Column(sa.String, nullable=False, unique=True)
  raum = sa.Column(sa.String)
  einrichtung = sa.Column(sa.String , nullable=False)


class Funktionsbenutzer(Base):
  __tablename__ = 'funktionsbenutzer'
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
  emailadresse = sa.Column(
      sa.String,
      sa.ForeignKey(TB_PREFIX + 'emailadressen.emailadresse'),
      primary_key=True,)
  name = sa.Column(sa.String, unique=True, nullable=False)


class Kontogruppe(Base):
  __tablename__ = 'kontogruppen'
  __table_args__ = (
      {'schema': PG_SCHEMA}
      )
  kgid = sa.Column(sa.Integer, primary_key=True) # PR: weitere Bedingungen?
  name = sa.Column(sa.String(20) , nullable=False)


if __name__ == '__main__':
  engine = sa.create_engine(PG, echo=True)
  Base.metadata.create_all(engine)
  Session = orm.sessionmaker(engine)
  session = Session()


