# -*- coding: utf-8 -*-
import datetime as dt
from eiticurator.benutzerverwaltung.models import *
from eiticurator import DBSession
from eiticurator.utils.miscellaneous import default_input

session = DBSession()
TIME_FORMAT = "%d.%m.%Y"

def getDistinctValues(attr):
  einrichtungen = []
  q = session.query(attr).distinct()
  for tupel in q.all():
    einrichtungen.append(tupel[0].encode('utf-8'))
  return einrichtungen

def getDomainNames():
  domains = session.query(Domain).all()
  return [domain.domain for domain in domains]

def getOEinheitNames():
  oeinheiten = session.query(Organisationseinheit).all()
  return [oeinheit.oeinheit for oeinheit in oeinheiten]

def inputUserDict():
  """
  Bemerkung: `session` wird benötigt, da aus der Datenbank z.B. Domains geladen
  werden, um bei Eingabe schon Vorschläge machen zu können.
  """
  user_info = {
      'nachname': raw_input('Nachname: '),
      'vorname': raw_input('Vorname: '),
      'titel': raw_input('Titel: '),
      'uid': raw_input('UID: '),
      'uname': raw_input('uname: '),
      'raum': raw_input('Raum: '),
      }
  user_info['einrichtung'] = default_input(
      'Einrichtung',
      "",
      getDistinctValues(Benutzer.einrichtung)
      )
  user_info['abteilung'] = default_input(
      'Abteilung',
      "",
      getDistinctValues(Benutzer.abteilung)
      )
  user_info['funktion'] = default_input(
      'Funktion',
      "",
      getDistinctValues(Benutzer.funktion)
      )
  user_info['von'] = default_input(
      'von',
      dt.datetime.now().strftime(TIME_FORMAT),
      )
  user_info['bis'] = raw_input('bis: ')
  user_info['domain'] = default_input(
      'Domain',
      "",
      getDomainNames()
      )
  user_info['oeinheit'] = default_input(
      'Organisationseinheit',
      default_value = "",
      choices = getOEinheitNames()
      )
  user_info['emailadresse'] = default_input(
      'EMail-Adresse',
      user_info['nachname'].lower() + '@'\
          + user_info['einrichtung'].lower() + '.mpg.de'
      )
  user_info['aktiviert'] = default_input(
      'aktiviert',
      "ja",
      ['ja', 'nein']
      )
  user_info['zombie_monate'] = raw_input('Zombie-Monate: ')
  user_info['check'] = default_input('Alles korrekt', "ja", None, "?")
  return user_info

def addUser():
  user_info = inputUserDict()
  if user_info['check'].lower() in ['ja', 'yes', 'j', 'y']:
    b = Benutzer(
        nachname=user_info['nachname'],
        vorname=user_info['vorname'],
        titel=user_info['titel'],
        einrichtung=user_info['einrichtung'],
        abteilung=user_info['abteilung'],
        funktion=user_info['funktion'],
        emailadresse=user_info['emailadresse'],
        raum=user_info['raum'],
        von=dt.datetime.strptime(user_info['von'], TIME_FORMAT),
        bis=dt.datetime.strptime(user_info['bis'], TIME_FORMAT))
    k = Konto(
        uid = user_info['uid'],
        uname = user_info['uname'],
        aktiviert = user_info['aktiviert'] == 'ja',
        oeinheit=user_info['oeinheit'],
        domain = user_info['domain'],
        zombie_monate = user_info['zombie_monate'])
    b.konto_object = k
    try:
      session.add(b)
      session.commit()
    except Exception, e:
      print e
      session.rollback()
      print "Rollback durchgeführt."
  else:
    print "\n >>> Abbruch <<<"

