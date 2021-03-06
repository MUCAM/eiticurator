# -*- coding: utf-8 -*-
"""
Kleine Dokumentaton:
"""
import textwrap
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
import datetime as dt

from eiticurator import cc, Base


PG_SCHEMA = cc.config['benutzerverwaltung.schema']

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
  passwort_md5 = sa.Column(sa.String, nullable=False, default="***")
  passwort_pam = sa.Column(sa.String, nullable=False, default="***")
  passwort_des = sa.Column(sa.String, nullable=False, default="***")
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
  emailadresse_object = orm.relationship(
      'Emailadresse',
      secondary=konto_emailadresse_abbildungen,
      backref=orm.backref('konto_object', uselist=False),
      uselist=False
      )
  funktionskonto_object = orm.relationship(
      'Funktionskonto',
      backref='konto_object'
      )
    
  def __repr__(self):
    return "%s(%d, %r)" %(
        self.__class__.__name__,
        self.uid,
        self.uname)
  
  def __str__(self):
    res = """
      Kontoinfo:
        uid:            %s
        uname:          %s
        aktiviert:      %s
        oeinheit:       %s
        domain:         %s
        anlegedatum:    %s
        beschreibung:   %s
        zombie_monate:  %s
        bearbeitet:     %s
    """ %(self.uid,
        self.uname,
        self.aktiviert,
        self.oeinheit,
        self.domain,
        self.anlegedatum,
        self.beschreibung,
        self.zombie_monate,
        self.bearbeitet
        )
    return textwrap.dedent(res)

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
  extern_erreichbar = sa.Column(sa.Boolean , nullable=False, default=True)
  __mapper_args__ = {'polymorphic_on': emailtyp}

  emailadresse_alias_objects = orm.relationship(
      'EmailadresseAlias',
      primaryjoin='Emailadresse.eid==EmailadresseAlias.referenz_eid',
      backref='emailadresse_object',
      cascade="all, delete, delete-orphan")

  emailadresse_aliasse = association_proxy(
      'emailadresse_alias_objects',
      'emailadresse')
  
  def __repr__(self):
    return "%s(%r)" %(
        self.__class__.__name__,
        self.emailadresse)

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
    session = orm.object_session(self)
    tmp_alias = self.emailadresse
    tmp_ref = self.emailadresse_object.emailadresse
    self.emailadresse = self.emailadresse + '_tmp'
    session.commit()
    self.emailadresse_object.emailadresse = tmp_alias
    self.emailadresse = tmp_ref
    session.commit()

  def __repr__(self):
    return "%s(%r)" %(
        self.__class__.__name__,
        self.emailadresse)


class Benutzer(Emailadresse):
  """
  Beispiele:
  ==========

  BENUTZER HINZUFÜGEN (alternativ: `benutzerverwaltung.ui.addUser`):
    b = Benutzer(
      nachname="Mustermann",
      vorname="Max",
      titel="Dr.",
      raum=100,
      telefon=100,
      fax=101,
      einrichtung="MPI",
      abteilung="IT",
      funktion="Serveradministrator",
      von=dt.datetime.strptime("1.1.2012", "%d.%m.%Y"),
      bis=dt.datetime.strptime("1.1.2014", "%d.%m.%Y"),
      bearbeitet = dt.datetime.now(),
      emailadresse = "max.mustermann@mpi.de")
    session.add(b)
    session.commit()

  SO KANN MAN EINEN BENUTZER SUCHEN UND INFORMATIONEN SEHEN:
    b = session.query(Benutzer).filter(Benutzer.nachname=="Rautenberg")).one()
    print b

  UNSCHARFE SUCHE:
    b = session.query(Benutzer).filter(Benutzer.nachname.like("Raut%")).one()

  EINE LISTE VON BENUTZERN NACH EINEM BESTIMMTEN KRITERIUM ERSTELLEN:
    b = benutzer_verwaltung = session.query(Benutzer).filter(
      Benutzer.abteilung =="Verwaltung").all()
  """
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

  def __repr__(self):
    return "%s(%r)" %(
        self.__class__.__name__,
        self.nachname)
  
  def __str__(self):
    res = """
      Benutzerinfo:
        Nachname:     %s
        Vorname:      %s
        Titel:        %s
        Raum:         %s
        Telefon:      %s
        FAX:          %s
        Einrichtung:  %s
        Abteilung:    %s
        Funktion:     %s
        von:          %s
        bis:          %s
        E-Mail:       %s
        Aliasse:      %s
    """ %(self.nachname,
        self.vorname,
        self.titel,
        self.raum,
        self.telefon,
        self.fax,
        self.einrichtung,
        self.abteilung,
        self.funktion,
        self.von,
        self.bis,
        self.emailadresse,
        str(self.emailadresse_aliasse),
        )
    res = textwrap.dedent(res)
    if self.konto_object not in [None, '']:
      hinweis = '\n`Benutzer.konto_object` hat folgende Informationen:\n '
      res = res + hinweis + self.konto_object.__str__()
    return res


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
  import datetime
  engine = sa.create_engine('sqlite:///test.sqlite', echo=True)
  Base.metadata.create_all(engine)
  Session = orm.sessionmaker(engine)
  session = Session()

  if False:
    b = Benutzer(
        emailadresse="philipp.rautenberg@mpisoc.mpg.de",
        nachname="Rautenberg",
        vorname="Philipp",
        titel="",
        raum="111",
        telefon="",
        fax="",
        einrichtung="mpisoc",
        abteilung="Verwaltung",
        extern_erreichbar=True,
        von=datetime.datetime.now(),
        bis=datetime.datetime.now())
    b.emailadresse_aliasse.append("p.rautenberg@mpisoc.mpg.de")
    b.emailadresse_aliasse.append("p.r@mpisoc.mpg.de")

  if True:
    b = session.query(Benutzer).filter_by(nachname="Rautenberg").first()
