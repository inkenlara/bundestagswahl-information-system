--Q1: Sitzverteilung 2021

SELECT p.KurzBezeichnung, s.sitze FROM sitzverteilungbundestag s, partei p
WHERE s.partei = p.parteiid





--Q2: Mitglieder Bundestag 2021

--Teil fuer Direktmandate
with wahlkreis_max as (
    select wahlkreis, max(prozenterststimmen) as maxi
    from wahlkreisprozenterst
    where wahljahr = 2021
    group by wahlkreis
),
direktmandate_wahlkreis as (
    select w.wahlkreis, w.parteikurz
    from wahlkreis_max b, wahlkreisprozenterst w
    where b.wahlkreis = w.wahlkreis 
    and b.maxi = w.prozenterststimmen
),
direktmandate as(
    select k.kandidatid, k.firstname, k.lastname, k.beruf, dw.parteikurz as partei
    from direktmandate_wahlkreis dw, direktkandidaten dk, kandidaten k, partei p
    where dw.wahlkreis = dk.wahlkreis
    and dk.kandidatid = k.kandidatid
    and p.KurzBezeichnung = dw.parteikurz
    and p.parteiid = k.partei
    and k.wahljahr = 2021
),
-- Teil für Listenmandate
-- anzahl sitze pro partei pro bundesland minus die direktmandate, die schon verbraucht wurden
sitze_fuer_liste as(
    select b.partei, b.bundesland, (s.sitze-b.direktmandate) as listensitze
    from sitzverteilungparteienprobundesland s, bundeslandstimmenaggregation b 
    where b.wahljahr = 2021
    and s.partei = b.partei
    and s.bundesland = b.bundesland
),
-- rausloeschen derer aus listenkandidaten, die schon per direktmandat in den BT kommen
liste_ohne_direktmandate as(
    select *
    from listenkandidaten lk
    where lk.kandidatid not in (select kandidatid from direktmandate)
),
-- kandidaten sortieren, um spaeter nur die top X herauszufiltern
reihennummern as(
  select ld.kandidatid, sl.partei, ld.bundesland, ROW_NUMBER() OVER(PARTITION BY sl.partei, sl.bundesland ORDER BY ld.listenplatz ASC) AS row_number
  from liste_ohne_direktmandate ld, sitze_fuer_liste sl, kandidaten k
  where ld.kandidatid = k.kandidatid
  and sl.bundesland = ld.bundesland
  and sl.partei = k.partei
  and k.wahljahr = 2021
),
-- kandidaten, die einen sitz bekommen herausfiltern
listenkandidaten as (select r.kandidatid, sl.partei, sl.bundesland
from sitze_fuer_liste sl, reihennummern r
where sl.partei = r.partei
and sl.bundesland = r.bundesland
and r.row_number <= sl.listensitze)
select * from direktmandate
union
select k.kandidatid, k.firstname, k.lastname, k.beruf, p.KurzBezeichnung as partei
from listenkandidaten l, kandidaten k, partei p
where l.kandidatid = k.kandidatid
and k.wahljahr = 2021
and p.parteiid = k.partei






--Q3: Wahlkreisuebersicht 2021

--wahlbeteiligung
select wahlkreis, (1.00*anzahlwahlende)/anzahlwahlberechtigte as wahlbeteiligung, wahljahr
from wahlkreisaggretation
WHERE wahljahr = 2021
    
--gewaehlte direktkandidaten
with erststimmensieger as (
  select we.wahlkreis, we.wahljahr, we.parteikurz as erststimmensieger, we.wahljahr
  from wahlkreisprozenterst we
  where we.wahljahr = 2021
  and not exists                        
          (select *                    
          from wahlkreisprozenterst we2            
          where we.wahlkreis = we2.wahlkreis  
          and we2.wahljahr = 2021
          and we2.prozenterststimmen > we.prozenterststimmen    
          )
)
select k.kandidatid, k.firstname, k.lastname, e.erststimmensieger, k.wahljahr
from erststimmensieger e, direktkandidaten dk, kandidaten k, partei p
where e.erststimmensieger = p.KurzBezeichnung
and p.parteiid = k.partei
and k.kandidatid = dk.kandidatid
and dk.wahlkreis = e.wahlkreis
and k.wahljahr = 2021

-- prozentuale und absolute Anzahl an Stimmen pro Partei + entwicklung im vergleich zum vorjahr
with vorjahr as (
    select w.wahlkreis, pz.parteikurz, w.anzahlstimmen, pz.prozentzweitstimmen
    from wahlkreisprozentzweit pz, wahlkreiszweitstimmenaggregation w, partei p
    where pz.wahljahr = 2017
    and w.wahljahr = 2017
    and pz.wahlkreis = w.wahlkreis
    and w.partei = p.parteiid
    and p.KurzBezeichnung = pz.parteikurz
)
select w.wahlkreis, pz.parteikurz, w.anzahlstimmen, pz.prozentzweitstimmen, w.anzahlstimmen-v.anzahlstimmen as stimmendifferenz, pz.prozentzweitstimmen-v.prozentzweitstimmen as prozentdifferenz
from wahlkreisprozentzweit pz, wahlkreiszweitstimmenaggregation w, partei p, vorjahr v
where pz.wahljahr = 2021
and w.wahljahr = 2021
and pz.wahlkreis = w.wahlkreis
and w.partei = p.parteiid
and p.KurzBezeichnung = pz.parteikurz
and w.wahlkreis = v.wahlkreis
and p.KurzBezeichnung = v.parteikurz





--Q4: Wahlkreissieger 2021

with erststimmensieger as (
  select we.wahlkreis, we.wahljahr, we.parteikurz as erststimmensieger
  from wahlkreisprozenterst we
  where we.wahljahr = 2021
  and not exists                        
          (select *                    
          from wahlkreisprozenterst we2            
          where we.wahlkreis = we2.wahlkreis  
          and we2.wahljahr = 2021
          and we2.prozenterststimmen > we.prozenterststimmen    
          )
  ),
  zweitstimmensieger as(
    select we.wahlkreis, we.wahljahr, we.parteikurz as zweitstimmensieger
    from wahlkreisprozentzweit we
    where we.wahljahr = 2021
    and not exists                        
          (select *                    
          from wahlkreisprozentzweit we2            
          where we.wahlkreis = we2.wahlkreis  
          and we2.wahljahr = 2021
          and we2.prozentzweitstimmen > we.prozentzweitstimmen    
          )
  )
  select e.wahlkreis,e.wahljahr,e.erststimmensieger,z.zweitstimmensieger
  from erststimmensieger e, zweitstimmensieger z
  where e.wahlkreis = z.wahlkreis



--Q5: Ueberhangsmandate
--aufgabe wurde so interpretiert, dass ueberhangsmandate von schritt 2 im divisorverfahren gemeint sind

select bundesland, partei, direktmandate-sitzkontingente  as ueberhangsmandate
from vorlaufigesitzverteilungparteienprobundesland
where sitzkontingente < direktmandate




--Q6: Knappste Sieger
-- filtere sieger
with sieger as(
    select *
    from wahlkreisprozenterst w1
    where w1.wahljahr = 2021
    and not exists (select * from wahlkreisprozenterst w2 
                    where w2.wahljahr = 2021 
                    and w1.wahlkreis = w2.wahlkreis 
                    and w2.prozenterststimmen > w1.prozenterststimmen)
),
-- filtere zweite
wahlkreisprozenterst_ohne_sieger as(
    select * from wahlkreisprozenterst
    EXCEPT
    select * from sieger    
),
zweite_sieger as(
    select *
    from wahlkreisprozenterst_ohne_sieger w1
    where 
    w1.wahljahr = 2021
    and not exists (select * from wahlkreisprozenterst_ohne_sieger w2 
                    where w2.wahljahr = 2021 
                    and w1.wahlkreis = w2.wahlkreis 
                    and w2.prozenterststimmen > w1.prozenterststimmen)    
), 
--bilde differenz zwischen stimmen
differenz as (
  select s.wahljahr, s.wahlkreis, s.parteikurz, s.prozenterststimmen-zs.prozenterststimmen as differenz, ROW_NUMBER() OVER(PARTITION BY s.parteikurz ORDER BY s.prozenterststimmen-zs.prozenterststimmen ASC) AS row_number
  from sieger s, zweite_sieger zs
  where s.wahlkreis = zs.wahlkreis
)
-- waehle die 10 knappsten abstaende
select k.wahljahr, di.wahlkreis, di.parteikurz, di.differenz, di.row_number, k.kandidatid, k.firstname, k.lastname
from differenz di, kandidaten k, direktkandidaten dk, partei p
where row_number <= 10
and di.parteikurz = p.KurzBezeichnung
and p.parteiid = k.partei
and k.wahljahr = 2021
and k.kandidatid = dk.kandidatid
and di.wahlkreis = dk.wahlkreis

-- Q6: wahlkreise, in der jede partei am knappsten verloren hat

-- filtere sieger
with sieger as(
    select *
    from wahlkreisprozenterst w1
    where w1.wahljahr = 2021
    and not exists (select * from wahlkreisprozenterst w2 
                    where w2.wahljahr = 2021 
                    and w1.wahlkreis = w2.wahlkreis 
                    and w2.prozenterststimmen > w1.prozenterststimmen)
),
-- differenz zwischen gewinner und parteien
differenz as(
    select w.wahljahr, w.wahlkreis, w.parteikurz, s.prozenterststimmen-w.prozenterststimmen as differenz
    from wahlkreisprozenterst w, sieger s
    where w.wahljahr = 2021
    and s.wahljahr = 2021
    and w.parteikurz not in (select parteikurz from sieger) 
    and w.wahlkreis = s.wahlkreis
),
-- suche fuer jede partei wahlkreis mit kleinster differenz
kleinste_differenz as (select d1.wahljahr, d1.parteikurz, d1.wahlkreis ,d1.differenz
from differenz d1
where not exists (
    select *
    from differenz d2
    where d1.parteikurz = d2.parteikurz
    and d2.differenz < d1.differenz
     )
)
-- join mit kandidaten
select k.wahljahr, kd.wahlkreis, kd.parteikurz, kd.differenz, k.kandidatid, k.firstname, k.lastname
from kleinste_differenz kd, kandidaten k, direktkandidaten dk, partei p
where kd.parteikurz = p.KurzBezeichnung
and p.parteiid = k.partei
and k.wahljahr = 2021
and k.kandidatid = dk.kandidatid
and kd.wahlkreis = dk.wahlkreis



--Q7: Wahlkreisuebersicht (Einzelstimmen)

--betrachte wahlkreise 1-5 (erst mal nur 1)
--wahlbeteiligung 
with anzahlwahlberechtigte as (select anzahlwahlberechtigte, wahlkreis from wahlkreisaggretation where wahljahr = 2021 and wahlkreis = 1),
wahlende as 
    (select count(*) as wahlende
    from anzahlwahlberechtigte a, zweitstimmen zw
    where zw.wahlkreis = 1)
select wahlkreis, (1.0*wahlende)/anzahlwahlberechtigte as wahlbeteiligung
from anzahlwahlberechtigte, wahlende

--gewaehlten direktkandidaten
with stimmen_pro_partei as (
  select partei, count(*) as stimmen
  from erststimmen
  where wahlkreis = 1
  group by partei
)
select k.kandidatid, k.firstname, k.lastname, s.partei, k.wahljahr
from stimmen_pro_partei s, direktkandidaten dk, kandidaten k
where stimmen = (select max(stimmen) from stimmen_pro_partei)
and s.partei = k.partei
and k.wahljahr= 2021
and k.kandidatid = dk.kandidatid
and dk.wahlkreis = 1

--prozentualer und absolute anzahl an stimmen pro partei

with stimmen_gesamt as(
    select (count(*)- (select count(*) from zweitstimmen where wahlkreis = 1 and partei = -1)) as stimmen_gesamt
    from zweitstimmen
    where wahlkreis = 1
),
    stimmen_pro_partei as(
    select partei, count(*) as stimmen_pro_partei
    from zweitstimmen
    where wahlkreis = 1
    group by partei
)
select 1 as wahlkreis, partei, stimmen_pro_partei, (1.00*stimmen_pro_partei)/stimmen_gesamt as stimmen_prozentual
from stimmen_pro_partei, stimmen_gesamt
where partei = p.parteiid
and wk.wahlkreisid = 1
and p.parteiid != -1
