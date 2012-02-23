create_info_benutzer = """CREATE VIEW info_benutzer AS
  SELECT
    benutzer.eid,
    nachname,
    vorname,
    titel,
    telefon,
    fax,
    raum,
    einrichtung,
    abteilung,
    funktion,
    emailadresse,
    extern_erreichbar,
    von,
    bis
  FROM
      benutzer
    INNER JOIN
      emailadressen
    ON (benutzer.eid = emailadressen.eid);"""

create_info_benutzer_konten = """CREATE VIEW info_benutzer_konten AS
  SELECT
    b.eid,
    k.uname,
    b.nachname,
    b.vorname,
    b.titel,
    b.raum,
    b.telefon,
    b.fax,
    b.einrichtung,
    b.abteilung,
    b.funktion,
    b.emailadresse,
    b.extern_erreichbar,
    b.von,
    b.bis,
    k.aktiviert,
    k.oeinheit,
    k.domain,
    k.anlegedatum,
    k.beschreibung,
    k.zombie_monate,
    k.bearbeitet
  FROM
    info_benutzer b,
    konten k,
    konto_emailadresse_abbildungen kea
  WHERE
    b.eid = kea.eid AND k.uid = kea.uid;"""
