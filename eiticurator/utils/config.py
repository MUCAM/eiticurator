"""
Source:
`<http://code.activestate.com/recipes/65334-use-good-old-ini-files-for-configuration/>`_
"""

import ConfigParser
import string

import os
DB_SETUP = 'db_setup.ini'
this_dir, this_filename = os.path.split(__file__)
DB_SETUP_PATH = os.path.join(this_dir, DB_SETUP)

def LoadConfig(filename=DB_SETUP, config={}):
  """
  returns a dictionary with key's of the form
  <section>.<option> and the values 
  """
  if not os.path.exists(filename):
    import textwrap
    ausgabe = """
      Es wurde keine .ini-Datei im Arbeitsverzeichnis gefunden.
      verwende deshalb SQLite-Datei `eiticurator.sqlite`."""
    print (textwrap.dedent(ausgabe))
    filename = DB_SETUP_PATH
  config = config.copy()
  cp = ConfigParser.ConfigParser()
  cp.read(filename)
  for sec in cp.sections():
    name = string.lower(sec)
    for opt in cp.options(sec):
      config[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
  return config


if __name__=="__main__":
  print LoadConfig("db_setup.ini")

