import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base

PG_ama = 'postgresql://postgres@10.1.1.42/amalie'
engine_ama = sa.create_engine(PG, echo=True)

Base_ama = declarative_base()
Base_ama.metadata.bind = engine

class SyncUser(Base_ama):
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
