import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base ()

user_group_maps = sa.Table(
    'user_group_maps',
    Base.metadata,
    sa.Column('user_key', sa.ForeignKey('users.user_key')),
    sa.Column('group_key', sa.ForeignKey('groups.group_key')),
    )

class User(Base):
    __tablename__ = 'users'
    #columns:
    user_key = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Unicode(16), unique=True)

    groups = orm.relationship(
        'Group',
        secondary=user_group_maps,
        backref='users')

    def __repr__(self):
      return "User(%s)" %(self.name)

class Group(Base):
    __tablename__ = 'groups'
    # columns
    group_key = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Unicode(16), unique=True)
    # relations

    def __repr__(self):
      return "Group(%s)" %(self.name)

class Test(object):
  def __init__(self, a):
    self._a = a
  def getA(self):
    return self._a
  def setA(self, value):
    if value>0:
      self._a = value
    else:
      print "a nicht groesser 0!"
  a = property(getA, setA)


if __name__ == '__main__':
  # verbinde zur Datenbank und erstelle Tabellen, falls noetig:
  #
  # ---------------------------------------------------
  # SQLITE, check mittels Firefox-Addon 'SQLite Manager'
  # >>> engine = sa.create_engine ('sqlite:///userdb.sqlite', echo=False)
  #
  # -----------------------------
  # PostgreSQL, check mit pgadmin
  engine = sa.create_engine ('postgresql://rautenbe@ama-prod/mucam')
  # ----------------------------------------------------
  Base.metadata.bind = engine
  Base.metadata.create_all ()
  Session = orm.sessionmaker (engine)
  session = Session ()

  # spiele mit Objekten:
  rl = User(name='Ronny')
  pr = User(name='Philipp')
  t = User(name="Thomas")
  it = Group(name="IT-Abteilung")
  ht = Group(name="Haustechnik")
  vw = Group(name="Verwaltung")
  session.add(vw)
  vw.users.append(rl)
  vw.users.append(pr)
  vw.users.append(t)
  pr.groups.append(it)
  rl.groups.append(it)
  t.groups.append(ht)

  print it.users
  print rl.groups
  session.commit()

  
