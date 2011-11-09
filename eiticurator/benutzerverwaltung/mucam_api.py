from core import *

DEFAULT_DOMAIN = "mucam"

class Controller(object):
  def __init__(self, echo=False):
    self.engine = sa.create_engine(PG, echo=echo)
    Base.metadata.create_all(self.engine)
    Session = orm.sessionmaker(self.engine)
    self.session = Session()

  def addUserUI(self):
    last_name = raw_input('Nachname: ')
    first_name = raw_input('Vorname: ')
    shown_name = raw_input('Anzeigename: ')
    uid = raw_input('UID: ')
    uname = raw_input('uname: ')
    oeinheit = raw_input('Oeinhein [it, mea, iv, fe, socr, psy, vw, bib, fellow]: ')
    emailaddress = raw_input('eMail-Adresse: ')
    room = raw_input('Raum: ')
    einrichtung = raw_input('Einrichtung: ')
    check = raw_input('Alles korrekt [JA]? ')
    # -----------------------------------------
    if check in ['', 'ja', 'Ja', 'JA', 'yes', 'Yes', 'Yes']:
      self.addUser(last_name,
          first_name,
          shown_name,
          uid,
          uname,
          oeinheit,
          emailaddress,
          room,
          einrichtung)

  def addUser(self,
      last_name,
      first_name,
      shown_name,
      uid,
      uname,
      oeinheit,
      emailaddress,
      room,
      einrichtung):
    konto = Konto(oeinheit=oeinheit, domain=DEFAULT_DOMAIN, uid=uid, uname=uname)
    email = Emailadresse(emailadresse=emailaddress)
    benutzer = Benutzer(
        emailadresse=emailaddress,
        nachname=last_name,
        vorname=first_name,
        anzeigename=shown_name,
        raum=room,
        einrichtung=einrichtung)
    try:
      self.session.add(email)
      self.session.add(konto)
      self.session.add(benutzer)
      self.session.commit()
      print ">>> Angelegt <<<"
    except Exception, e:
      print e
      print "rolling back!"
      self.session.rollback()
  

if __name__ == '__main__':
  '''
  engine = sa.create_engine(PG, echo=True)
  Base.metadata.create_all(engine)
  session = orm.sessionmaker(engine)
  '''
  c = Controller()

  
