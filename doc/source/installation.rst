================================
Installation von ``eiticurator``
================================

Die Installtion erfolgt in zwei Schritten:

* Vorbereiten des Systems
* Installation des Quellcodes

Systemvorbereitung
==================

Folgende Pakete müssen installiert sein:

* ``git``
* ``python``
* ``python-sqlalchemy``
* ``python-psycopg2`` (nur notwendig, wenn mit PostgrSQL gearbeitet wird)

Debian-Basiert::

  aptitude install git python python-sqlalchemy python-psycopg2

Installation des Quellcodes
===========================

Der Quellcode liegt auf github. Zur installation reicht folgender Befehl::

  git clone https://phippo@github.com/MUCAM/eiticurator.git
  # oder
  git clone git@github.com:MUCAM/eiticurator.git

Jetzt muss nur noch der Python-Path angepasst werden. Empfehlung: Da
normalerweise Repositories nicht extra gesichert werden müssen (sie liegen ja
schon auf einem Repository-Server redundant), kann man sie in einem extra
Verzeichnis sammeln. Zur Verwaltung der user-spezifischen python-Bibliotheken
legt man sich im Home-Verzeichnis ein Unterverzeichnis ``~/lib/python`` an (in der .bashrc: ``export PYTHONPATH=$PYTHONPATH:$HOME/lib/python``) und
verlinkt von dort auf die Repository::

  mkdir ~/lib
  mkdir ~/lib/python
  mkdir ~/Repositories
  mkdir ~/Repositories/github
  cd ~/Repositories/github
  git clone git@github.com:MUCAM/eiticurator.git
  cd ~/lib/python
  ln -s ~/Repositories/github/eiticurator/eiticurator eiticurator


