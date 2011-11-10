from core import *

DEFAULT_DOMAIN = "mucam"

class Controller(object):
  def __init__(self, echo=False):
    self.engine = sa.create_engine(PG, echo=echo)
    Base.metadata.create_all(self.engine)
    Session = orm.sessionmaker(self.engine)
    self.session = Session()

  def addUser(self,
      last_name,
      first_name,
      shown_name,
      uid,
      uname,
      oeinheit,
      domain,
      emailaddress,
      room,
      einrichtung):
    konto = Konto(
        oeinheit=oeinheit,
        domain=domain,
        uid=uid,
        uname=uname)
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
      self.session.add(benutzer)
      self.session.add(konto)
      self.session.commit()
      print "\n>>> %s Angelegt <<<" %(benutzer.anzeigename)
    except Exception, e:
      print e
      print "\n>>> Rollback <<<"
      self.session.rollback()
  

if __name__ == '__main__':
  '''
  engine = sa.create_engine(PG, echo=True)
  Base.metadata.create_all(engine)
  session = orm.sessionmaker(engine)
  '''
  c = Controller()

  
