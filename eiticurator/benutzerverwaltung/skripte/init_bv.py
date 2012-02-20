from eiticurator.benutzerverwaltung.ext.mucam import *

if __name__ == '__main__':
  # get ama data
  session = get_session()
  all_users = session.query(SyncUser).all()
 
  # anlegen: organisationseinheiten und domains
  try:
    d = Domain (domain = "MUCAM", beschreibung = "")
    session.add (d)
    session.commit()
    oes = ['MPDL', "MEA", "MPISOC", "PSY"]
    for oe in oes:
      session.add(Organisationseinheit (
          domain = "MUCAM", oeinheit = oe))
    session.commit()
  except:
    session.rollback()
  
  for user in all_users:
    if user.email is not None:
      u = Benutzer(
          nachname = user.familyname,
          vorname = user.givenname,
          titel = user.title,
          raum = user.room_number or '',
          telefon = user.phone_number or '',
          fax = user.fax_number or '',
          einrichtung = user.institute,
          abteilung = user.department,
          funktion = user.function,
          extern_erreichbar = True,
          von = user.since,
          bis = user.until,
          emailadresse = user.email
          )
      session.add(u)
      session.flush()
      print "---------------------- >>>>>> " + u.emailadresse
      print "---------------------- >>>>>> " + str(u.eid)
      d2ap = StaffData02Export_Benutzer_Abbildung(id=user.id, eid=u.eid)
      session.add(d2ap)
      if user.department == "Sozialpolitik":
        oeinheit = "MEA"
      else:
        oeinheit = user.institute
      k = Konto(
        uid = user.id,
        uname = user.user_name,
        passwort_unix = "",
        aktiviert = True,
        oeinheit = oeinheit,
        domain = 'MUCAM',
        beschreibung = "",
        zombie_monate = 3 * int(u.abteilung=="Sozialrecht")
        )
      u.konto_object.append(k)
  session.commit()

  all_aliasse = session.query(SyncAliasse).all()
  for alias in all_aliasse:
    try:
      k = session.query(Konto).filter_by(uid=alias.uid).one()
      k.emailadresse_objects[0].emailadresse_aliasse.append(alias.mail)
      session.commit()
    except sa.orm.exc.NoResultFound, e:
      session.rollback()
      print alias.uid, " kein Konto gefunden."
    except sa.exceptions.IntegrityError, e:
      session.rollback()
      print alias.mail, " war wohl primary..."
