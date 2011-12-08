import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base ()

class Emailaddress(Base):
  __tablename__ = 'emailaddresses'
  emailaddress = sa.Column(sa.String, primary_key=True)
  emailtype = sa.Column(sa.String, nullable=False)
  __mapper_args__ = {'polymorphic_on': emailtype}


class EmailaddressUser(Emailaddress):
  __tablename__ = 'emailaddress_users'
  __mapper_args__ = {'polymorphic_identity': 'user'}
  emailaddress = sa.Column(
      sa.String,
      sa.ForeignKey('emailaddresses.emailaddress'),
      primary_key=True)
  name = sa.Column(sa.String, nullable=False) # PR: weitere Bedingungen?


class EmailaddressAlias(Emailaddress):
  __tablename__ = 'emailaddresses_alias'
  emailaddress = sa.Column(
      sa.String,
      sa.ForeignKey('emailaddresses.emailaddress'),
      primary_key=True)
  real_emailaddress = sa.Column(
      sa.ForeignKey('emailaddresses.emailaddress'),
      nullable=False)
  __mapper_args__ = {
      'polymorphic_identity': 'alias',
      }

  
if __name__ == '__main__':
  engine = sa.create_engine ('sqlite:///email.sqlite', echo=True)
  Base.metadata.bind = engine
  Base.metadata.create_all ()
  Session = orm.sessionmaker (engine)
  session = Session ()
  # add user (works):
  u = EmailaddressUser(name="Testuser", emailaddress="testuser@test.com")
  session.add(u)
  session.commit()
  # --> INSERT INTO emailaddresses (emailaddress, emailtype) VALUES (?, ?)
  # --> ('testuser@test.com', 'user')
  # 'emailaddress' is inserted correctly

  # add alias (throws an IntegrityError):
  a = EmailaddressAlias (
      real_emailaddress="testuser@test.com",
      emailaddress="tu@test.com"
      )
  session.add(a)
  session.commit()
  # --> INSERT INTO emailaddresses (emailtype) VALUES (?)' ('alias',)
  # 'emailaddress' is missing! => IntegrityError
