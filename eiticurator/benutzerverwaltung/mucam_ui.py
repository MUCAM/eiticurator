# -*- coding: utf-8 -*-
from core import Domain, Organisationseinheit
from eiticurator import DBSession

session = DBSession()

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
      'last_name': raw_input('Nachname: '),
      'first_name': raw_input('Vorname: '),
      'title': raw_input('Titel: '),
      'uid': raw_input('UID: '),
      'uname': raw_input('uname: '),
      'einrichtung': raw_input('Einrichtung: '),
      'room': raw_input('Raum: ')
      }
  user_info['shown_name'] = default_input(
      'Anzeigename', ' '.join([
        user_info['title'],
        user_info['first_name'],
        user_info['last_name']]))
  user_info['domain'] = default_input(
      'Domain',
      "",
      getDomainNames(session)
      )
  user_info['oeinheit'] = default_input(
      'Organisationseinheit',
      default_value = "",
      choices = getOEinheitNames(session)
      )
  user_info['emailaddress'] = default_input(
      'EMail-Adresse',
      user_info['last_name'].lower() + '@'\
          + user_info['einrichtung'].lower() + '.mpg.de'
      )
  user_info['check'] = default_input('Alles korrekt', "ja", None, "?")
  return user_info

def addUser():
  user_info = inputUserDict()
  if user_info['check'].lower() in ['ja', 'yes']:
    addUser(user_info['last_name'],
        user_info['first_name'],
        user_info['shown_name'],
        user_info['uid'],
        user_info['uname'],
        user_info['oeinheit'],
        user_info['domain'],
        user_info['emailaddress'],
        user_info['room'],
        user_info['einrichtung'])
  else:
    print "\n >>> Abbruch <<<"

