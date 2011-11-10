import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base

PG = 'postgresql://postgres@10.1.1.42/amalie'
engine = sa.create_engine(PG, echo=True)

Base = declarative_base()
Base.metadata.bind = engine

class SyncUser(Base):
  __tablename__ = "einmalsync"
  __table_args__ = {
      'autoload': True,
      'schema': "_activedirectory"}

if __name__ == '__main__':
  Session = orm.sessionmaker(engine)
  session = Session()
  all_users = session.query(SyncUser).all()
  for user in all_users:
    print user.familyname, user.institute, user.phone_number, "..."
  print "\n>>> jetzt brauchen wir es nur noch an addUser() uebergeben!"
