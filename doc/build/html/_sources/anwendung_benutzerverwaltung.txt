================================
Anwendung der Benutzerverwaltung
================================

Schnelleinstieg
===============

Initialisierung::

  import eiticurator as etc
  from eiticurator.benutzerverwaltung.models import *

An dieser Stelle wird im Arbeitsverzeichnis eine Datei ``eiticurator.ini``
angelegt. Standardmäßig ist dort eine SQLite-Datenbank eingetragen. Ist dies
nicht gewünscht, einfach ``ipython`` verlassen, den entsprechenden Eintrag
ändern, und fertig.
  
Wenn alle notwendigen Modelle geladen sind, kann die session erstellt werden,
um auf die Datenbank zugreifen zu können::

  session = etc.get_session()

Zum vereinfachten Umgang mit den Modellen kann jetzt ein UserInterface-Modul
geladen werden::

  import eiticurator.benutzerverwaltung.ui as ui

Anwendungsbeispiele
-------------------

Hinweis: Hilfe z.B. für die Klasse ``Benutzer`` kann man auch mit dem **?**
bekommen: unter ``ipython``::

  Benutzer?

Benutzer mit Konto anlegen::

  ui.addUser()
  Nachname: Mustermann
  Vorname: Max
  Titel: ...

Benutzer aus der Datenbank laden::
  
  b = session.query(Benutzer).filter(Benutzer.nachname=="Mustermann")).one()
  print b

Benutzer aus der Datenbank laden, Informationen anzeigen und deaktivieren::

  b = session.query(Benutzer).filter(Benutzer.nachname.like("Raut%")).one()
  print b
  b.konto_object.aktiviert = False
  session.commit()

Alle Benutzer einer Abteilung laden::

  benutzer_verwaltung = session.query(Benutzer).filter(
      Benutzer.abteilung =="Verwaltung").all()
  for benutzer in benutzer_verwaltung:
    print benutzer.nachname, benutzer.vorname
