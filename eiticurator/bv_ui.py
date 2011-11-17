from models.benutzerverwaltung import *

def getZeichenkette(laenge=10):
  import random
  import string
  zeichen_liste = [random.choice(string.ascii_letters) for x in range(laenge)]
  zeichen = ''.join(zeichen_liste)
  return zeichen

if __name__ == '__main__':
  print "Jetzt geht's los!"
  engine = sa.create_engine('postgresql://rautenbe@ama-prod/mucam', echo=True)
  Base.metadata.create_all(engine)
  Session = orm.sessionmaker(engine)
  session = Session()
  
  # Werte in die Datenbank einfuegen
  domain_name = getZeichenkette(10)
  dom = Domain(domain=domain_name)
  session.add(dom)
  session.commit()
