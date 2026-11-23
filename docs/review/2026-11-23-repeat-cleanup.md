# Repeat clean-up, 2026-11-23

Operator decision, 2026-11-23, answering "Decide on the repeated per-page notes now?": "Remove repeats". Norm ledger
row 5 in lukio-runko: a site-wide fact is stated once on a site page; topic pages do not repeat it. Engine pin
raised to v0.5.1.

Input: the repeat report of the build before this round (228 main-region clusters, each in 3 or more topic
groups). Each cluster was classified by reading its text. **IN** means a stamped disclaimer, reassurance, provenance
note or site-wide fact; **OUT** means task instructions, lesson steps, citations, curriculum text, headings or
subject content, which stay even when repeated. *After* is the cluster in the repeat report of the new build.

Counts: 32 IN, 196 OUT. Build: 0 errors before and after; repeat warnings 230 before (engine v0.5.1 on the
old content), 208 after.

## Not removed, for the operator

- **Privacy lines inside lesson design** (OUT, marked *unsure*): the ground rule "Kukaan ei kerro tunnilla …
  Ryhmätyö tehdään kuvitteellisilla tapauksilla", "Kukaan ei kerro omia suunnitelmiaan ääneen, ellei itse halua" in
  the lesson goal, and table steps such as "Muistuta: HOPSiin kirjataan vain se, minkä opiskelija haluaa jakaa".
  They are the counsellor's ground rules and steps, so this round kept them. If they should go too, the principle
  is already stated once on the front page.
- **HOPSiin lines in topics 13-15** keep "vain se, minkä haluat jakaa" because it is part of the instruction
  sentence; removing it would mean rewording.
- **The timing stamp** "(esimerkki, koulu päättää)" comes from the engine, not from this site.
- **Mielenterveystalo items written for the topic** (02, 03, 04, 13, 14, 15) stay; the mood thresholds and help
  lists are a later round.

## Clusters

| Sample (first 80 chars) | Groups | IN/OUT | Reason | Action | Stated once | After |
|---|---|---|---|---|---|---|
| Lukiolaisella on oikeus oppimisen tukeen ja erityisopetukseen, ja oikeutta tukee | 19 | IN | site-wide fact stamped on every topic (yearly fact) | removed from all topics' yearly_facts; fact deleted from data/yearly-facts.yaml | /opetussuunnitelma/, Opinto-ohjaus lyhyesti, with the OPH links | gone |
| Etsi lähin Ohjaamo, Ohjaamot. Luettu 21.11.2026. | 19 | OUT | source citation | entry removed only where the page no longer uses the source | - | 6 groups |
| Oppimisen tuen uudistus, Opetushallitus. Luettu 21.11.2026. | 19 | OUT | source citation | entry removed only where the page no longer uses the source | - | 4 groups |
| Pelisäännöt ja oletusten tarkistus | 18 | OUT | heading, phase name or UI label | none | - | 18 groups |
| Tarina perustuu tämän aiheen sisältöön, ja sen voi pelata selaimessa myös puheli | 18 | IN | generic visual-novel blurb sentence | sentence removed; every link and chapter title kept | /polku/ | gone |
| Pohdi yksi Pohdinnan kysymyksistä ja tee itsearviointi (5 min). | 18 | OUT | task instruction or lesson step | none | - | 18 groups |
| HOPS-askel ja exit | 18 | OUT | heading, phase name or UI label | none | - | 18 groups |
| Tehtävä 1 (15 min) ja Tehtävä 2 (10 min) yksin tai parin kanssa. | 18 | OUT | task instruction or lesson step | none | - | 18 groups |
| Kysymyksiä ja keskeneräisten loppuun. | 18 | OUT | task instruction or lesson step | none | - | 18 groups |
| Jos huomaat oletuksen, muotoile esimerkki uudelleen. | 18 | OUT | task instruction or lesson step | none | - | 18 groups |
| Lukion opetussuunnitelman perusteet 2019, OPH-2263-2019. Tarkistettu 21.11.2026. | 18 | OUT | source citation | none | - | 18 groups |
| Neuvontakanavien aukioloajat ja paikalliset ohjauspalvelut katsotaan palvelujen  | 18 | IN | guidance_services fact stamped on every topic | kept only in 08 (ohjauspalvelut) and 15 (haku), where it is the subject | /lahteet/ (yearly-facts table); topics 08 and 15 | 3 groups |
| Aihe 01 · opinto-ohjaajalle | 18 | OUT | heading, phase name or UI label | none | - | 18 groups |
| Opetussuunnitelma: tämä aihe palvelee | 18 | OUT | heading, phase name or UI label | none | - | 18 groups |
| Lukiolaisella on oikeus oppimisen tukeen ja erityisopetukseen, ja oikeutta tukee | 18 | IN | site-wide fact stamped on every topic (yearly fact) | removed from all topics' yearly_facts; fact deleted from data/yearly-facts.yaml | /opetussuunnitelma/, Opinto-ohjaus lyhyesti, with the OPH links | gone |
| Näitä tietoja ei kopioida tälle sivulle. Katso arvo virallisesta lähteestä. | 18 | IN | engine note stamped per topic | removed by lukio-runko v0.5.1 (pin raised) | /polku/ (Omat tietosi) and the front page already say where the mark is stored | gone |
| Opintopolku ei anna henkilökohtaista opinto- tai uraneuvontaa korkeakouluhakijoi | 18 | IN | guidance_services fact stamped on every topic | kept only in 08 (ohjauspalvelut) and 15 (haku), where it is the subject | /lahteet/ (yearly-facts table); topics 08 and 15 | 3 groups |
| Opintopolun neuvonta ja ohjaus -sivu kokoaa neuvontapalvelujen yhteystiedot ja l | 18 | IN | guidance_services fact stamped on every topic | kept only in 08 (ohjauspalvelut) and 15 (haku), where it is the subject | /lahteet/ (yearly-facts table); topics 08 and 15 | 3 groups |
| Kierrä ja kysy avoimia kysymyksiä. | 18 | OUT | task instruction or lesson step | none | - | 18 groups |
| Lue osio Opiskelijalle (7 min). | 18 | OUT | task instruction or lesson step | none | - | 18 groups |
| Sanamuoto on Lukion opetussuunnitelman perusteista 2019 sellaisenaan. | 18 | OUT | attribution of quoted curriculum text (engine) | none | - | 18 groups |
| Aikaa kuluu: noin 40 minuuttia. | 18 | OUT | heading, phase name or UI label | none | - | 18 groups |
| Kirjoita vastaukset omaan muistioosi. Niitä ei tarvitse näyttää kenellekään. | 18 | IN | privacy reassurance on every Pohdinta | reassurance sentence removed; the instruction stays | /polku/ | gone |
| Itsearviointi. Arvioi jokainen kohta asteikolla En vielä · Osittain · Melko hyvi | 18 | OUT | task instruction or lesson step | none | - | 18 groups |
| Merkintä tallentuu vain tähän selaimeen, kun painat painiketta. Itseopiskelupolk | 18 | IN | engine note stamped per topic | removed by lukio-runko v0.5.1 (pin raised) | /polku/ (Omat tietosi) and the front page already say where the mark is stored | gone |
| Ohjaa puhumaan tapauksesta, ei omasta tilanteesta. | 17 | OUT | lesson design: ground rule, lesson goal or table step (unsure, see report) | none | - | 17 groups |
| Ryhmätyö tehdään kuvitteellisilla tapauksilla. | 17 | OUT | lesson design: ground rule, lesson goal or table step (unsure, see report) | none | - | 17 groups |
| Opintopolun neuvonta ja ohjaus -sivu kokoaa neuvontapalvelujen yhteystiedot ja l | 17 | IN | guidance_services fact stamped on every topic | kept only in 08 (ohjauspalvelut) and 15 (haku), where it is the subject | /lahteet/ (yearly-facts table); topics 08 and 15 | gone |
| Tee Tehtävä 1 (15 min) ja Tehtävä 2 (10 min). Tehtävä 3 on lisätehtävä, jos halu | 17 | OUT | task instruction or lesson step | none | - | 17 groups |
| Varaa aika opinto-ohjaajalle, jos | 17 | OUT | Milloin opinto-ohjaajalle, topic-specific pointer | none | - | 17 groups |
| Tapaukset (kaikki henkilöt ovat kuvitteellisia): | 17 | IN | fictional-material disclaimer on every case list | label shortened to *Tapaukset:* | front page, Näin sivustoa käytetään | gone |
| 45 min, 60 min, 75 min | 17 | OUT | heading, phase name or UI label | none | - | 17 groups |
| Jos koulusi käyttää sähköistä HOPSia, tee merkintä sinne koulun ohjeen mukaan (e | 17 | OUT | task instruction; (esimerkki) marks school practice (CLAUDE.md rule 3) | none | - | 17 groups |
| Yksin tai parin kanssa. | 16 | OUT | task instruction or lesson step | none | - | 16 groups |
| Varaa nimettömiä lappuja virittäytymiseen ja exitiin. | 16 | OUT | task instruction or lesson step | none | - | 16 groups |
| Exit sähköisesti tunnin jälkeen. | 15 | OUT | task instruction or lesson step | none | - | 15 groups |
| jatko-opinto- ja urasuunnitelma | 13 | OUT | heading, phase name or UI label | none | - | 13 groups |
| Tehtävä 3 (10 min) kolmen hengen ryhmissä kuvitteellisilla tapauksilla. | 12 | OUT | task instruction or lesson step | none | - | 12 groups |
| Tuki: Oppimisen tuen säännöt uudistuivat. Katso Opetushallituksen sivu Oppimisen | 12 | IN | generic learning-support referral stamped in Eriyttäminen | removed (topic 15 keeps its own exam-arrangement sentence); orphaned OPH source entries removed | /opetussuunnitelma/ | gone |
| Tee halutessasi sanataulukko, jossa vasemmalla on suomenkielinen sana ja oikeall | 12 | OUT | task instruction or lesson step | none | - | 12 groups |
| Kenelle opiskelija varaa ohjausajan ja miten (opinto-ohjaaja, ryhmänohjaaja, eri | 11 | OUT | school_adapts item (school practice marked as example) | none | - | 11 groups |
| Vastaa yleisiin kysymyksiin, ohjaa henkilökohtaiset ohjausaikaan. | 11 | OUT | task instruction or lesson step | none | - | 11 groups |
| 1. vuosi, syksy (esimerkki, koulu päättää) | 11 | IN | (esimerkki, koulu päättää) stamped on the timing row | not changed here: the text comes from the engine (views_topic.timing_text); reported | footer, front page and /opetussuunnitelma/ (Koulu päättää) already say it | 11 groups |
| Yksi tapaus koko ryhmälle yhdessä. | 11 | OUT | task instruction or lesson step | none | - | 11 groups |
| Kukaan ei kerro omia suunnitelmiaan ääneen, ellei itse halua. | 10 | OUT | lesson design: ground rule, lesson goal or table step (unsure, see report) | none | - | 10 groups |
| Väitteet paperilla, opiskelija vastaa yksin. | 10 | OUT | task instruction or lesson step | none | - | 10 groups |
| Kirjaus paperille, siirto HOPSiin myöhemmin. | 10 | OUT | task instruction or lesson step | none | - | 10 groups |
| Mielenterveystalo: nuoret, Mielenterveystalo.fi. Luettu 21.11.2026. | 10 | OUT | source citation | entry removed only where the page no longer uses the source | - | 7 groups |
| Opintopolku, Opetushallitus (Opintopolku). Luettu 21.11.2026. | 9 | OUT | source citation | none | - | 9 groups |
| S2 ja selkeä kieli: Käy sanasto läpi ennen tehtäviä. | 9 | OUT | task instruction or lesson step | none | - | 9 groups |
| Exit-lappu: yksi kysymys ohjaajalle (nimetön tai nimellä, opiskelija valitsee). | 9 | OUT | task instruction or lesson step | none | - | 9 groups |
| Vastaa yleisiin kysymyksiin, ohjaa henkilökohtaiset asiat ohjausaikaan. | 9 | OUT | task instruction or lesson step | none | - | 9 groups |
| Yksi yhteinen tapaus koko ryhmälle. | 9 | OUT | task instruction or lesson step | none | - | 9 groups |
| Ohjaa henkilökohtaiset asiat ohjausaikaan. | 9 | OUT | task instruction or lesson step | none | - | 9 groups |
| Ohjaa puhumaan tapauksista, ei omista suunnitelmista. | 8 | OUT | lesson design: ground rule, lesson goal or table step (unsure, see report) | none | - | 8 groups |
| Työmarkkinatori, KEHA-keskus (Työmarkkinatori). Luettu 21.11.2026. | 8 | OUT | source citation | none | - | 8 groups |
| Tehtävä 3 pareittain yhdellä kuvitteellisella tapauksella (8 min). | 8 | OUT | task instruction or lesson step | none | - | 8 groups |
| Tehtävän 1 vaihe 5 kotiin. | 8 | OUT | task instruction or lesson step | none | - | 8 groups |
| Kerro, miten ohjausaika varataan (esimerkki). | 8 | OUT | task instruction or lesson step | none | - | 8 groups |
| Työnhaun ja työllisyyspalvelujen asiointi tapahtuu Työmarkkinatorilla, ja palvel | 8 | OUT | yearly fact cited by the topics whose subject it is | none | - | 8 groups |
| Lue muutama lappu ääneen. | 8 | OUT | task instruction or lesson step | none | - | 8 groups |
| Kerää laput, sekoita ja lue muutama ääneen. | 8 | OUT | task instruction or lesson step | none | - | 8 groups |
| Mieti hiljaa itseksesi: mikä tapauksessa muistutti omaa tilannettasi, mikä ei? | 8 | OUT | task instruction or lesson step | none | - | 8 groups |
| Lue vain kaksi lappua. | 8 | OUT | task instruction or lesson step | none | - | 8 groups |
| Työnhaun ja työllisyyspalvelujen asiointi tapahtuu Työmarkkinatorilla, ja palvel | 7 | OUT | yearly fact cited by the topics whose subject it is | none | - | 7 groups |
| Kirjoittakaa kaksi kysymystä tapauksen opiskelijalle. | 7 | OUT | task instruction or lesson step | none | - | 7 groups |
| 1. vuosi, kevät (esimerkki, koulu päättää) | 7 | IN | (esimerkki, koulu päättää) stamped on the timing row | not changed here: the text comes from the engine (views_topic.timing_text); reported | footer, front page and /opetussuunnitelma/ (Koulu päättää) already say it | 7 groups |
| Sähköinen nimetön sanapilvi koulun omalla välineellä. | 7 | OUT | task instruction or lesson step | none | - | 7 groups |
| Kirjaus loppuun kotona. Exit sähköisesti tunnin jälkeen. | 7 | OUT | task instruction or lesson step | none | - | 7 groups |
| Yksi kuvitteellinen tapaus Tehtävästä 3 koko ryhmälle yhdessä. | 6 | OUT | task instruction or lesson step | none | - | 6 groups |
| Studyinfo (Opintopolun englanninkielinen osa), Opetushallitus (Opintopolku). Lue | 6 | OUT | source citation | none | - | 6 groups |
| Terveys, perhe ja tuen tarve jäävät omaan muistioon, ellei opiskelija itse halua | 6 | OUT | lesson design: ground rule, lesson goal or table step (unsure, see report) | none | - | 6 groups |
| Opiskeluhuolto, Opetushallitus. Luettu 21.11.2026. | 6 | OUT | source citation | entry removed only where the page no longer uses the source | - | 3 groups |
| Kirjaa HOPSiin vain se, minkä haluat koulun tietävän. | 6 | IN | student-facing HOPS privacy reassurance stamped in Itseopiskelun askel | privacy sentences removed; what to write stays | /polku/ | gone |
| Yliopistojen todistusvalinnan pisteytys ja ammattikorkeakoulujen valintaperustee | 6 | OUT | yearly fact cited by the topics whose subject it is | none | - | 6 groups |
| Pidä keskustelu tapauksessa, ei opiskelijoiden omissa tilanteissa. | 6 | OUT | lesson design: ground rule, lesson goal or table step (unsure, see report) | none | - | 6 groups |
| Etsi lähin Ohjaamo (luettu 21.11.2026): ohjausta nuorille opiskeluun, työhön ja  | 6 | IN | generic Ohjaamo item in Apua saat myös | removed except topic 18 (support after lukio is its subject); orphaned source entries removed | /polku/ | gone |
| Kukaan ei vastaa henkilökohtaiseen kysymykseen ääneen. | 6 | IN | generic privacy note above every open-question bank | paragraph removed; the questions stay | front page, Näin sivustoa käytetään | gone |
| Käsittele vain ensimmäinen väite. | 6 | OUT | task instruction or lesson step | none | - | 6 groups |
| S2 ja selkeä kieli: Käy sanasto läpi ennen Tehtävää 1. | 6 | OUT | task instruction or lesson step | none | - | 6 groups |
| Muistuta tunnin alussa ja lopussa, että HOPSiin kirjataan vain se, minkä opiskel | 6 | OUT | lesson design: ground rule, lesson goal or table step (unsure, see report) | none | - | 6 groups |
| Etsi lähin Ohjaamo (luettu 23.11.2026): ohjausta alle 30-vuotiaille opiskeluun,  | 6 | IN | generic Ohjaamo item in Apua saat myös | removed except topic 18 (support after lukio is its subject); orphaned source entries removed | /polku/ | gone |
| Kysymykset sopivat yksityiseen kirjoittamiseen, vapaaehtoiseen pariin tai yleise | 6 | IN | generic privacy note above every open-question bank | paragraph removed; the questions stay | front page, Näin sivustoa käytetään | gone |
| Kysymykset on tarkoitettu ensin yksityiseen kirjoittamiseen omaan muistioon. | 6 | IN | generic privacy note above every open-question bank | paragraph removed; the questions stay | front page, Näin sivustoa käytetään | gone |
| Terveyteen, perheeseen ja tuen tarpeeseen liittyvät ajatukset voit pitää omassa  | 6 | IN | student-facing HOPS privacy reassurance stamped in Itseopiskelun askel | privacy sentences removed; what to write stays | /polku/ | gone |
| Muistuta: HOPSiin kirjataan vain se, minkä opiskelija haluaa jakaa. | 6 | OUT | lesson design: ground rule, lesson goal or table step (unsure, see report) | none | - | 6 groups |
| Salli kuulokkeet ja oma rauhallinen paikka. | 6 | OUT | task instruction or lesson step | none | - | 6 groups |
| HOPSiin: Kirjoita siihen vain se, minkä haluat jakaa. | 5 | IN | student-facing HOPS privacy reassurance stamped in Itseopiskelun askel | privacy sentences removed; what to write stays | /polku/ | gone |
| Exit-lappu: yksi kysymys, jonka haluavat kysyä ohjauksessa (nimetön tai nimellä, | 5 | OUT | task instruction or lesson step | none | - | 5 groups |
| Merkitse, että suunnitelma on alustava. | 5 | OUT | task instruction or lesson step | none | - | 5 groups |
| Kysymykset on tarkoitettu ensin yksityiseen kirjoittamiseen omaan muistioon. Ryh | 5 | IN | generic privacy note above every open-question bank | paragraph removed; the questions stay | front page, Näin sivustoa käytetään | gone |
| Tehtävä 3 pareittain yhdellä kuvitteellisella tapauksella (8 min). Kirjoittakaa  | 5 | OUT | task instruction or lesson step | none | - | 5 groups |
| Kerää laput, sekoita ja lue muutama ääneen. Älä korjaa vielä. | 5 | OUT | task instruction or lesson step | none | - | 5 groups |
| Voit myös keksiä paperille oman kuvitteellisen tapauksen. | 5 | OUT | task instruction or lesson step | none | - | 5 groups |
| Yksi yhteinen tapaus koko ryhmälle tai Tehtävä 3 kotiin. | 5 | OUT | task instruction or lesson step | none | - | 5 groups |
| Lue kaksi lappua ääneen. Älä arvioi. | 5 | OUT | task instruction or lesson step | none | - | 5 groups |
| Kirjaus loppuun kotona. Exit-kysymys tunnin jälkeen. | 5 | OUT | task instruction or lesson step | none | - | 5 groups |
| Tehtävä 1 (15 min) yksin. | 5 | OUT | task instruction or lesson step | none | - | 5 groups |
| Tee sitten tehtävän vaiheet hänelle. | 5 | OUT | task instruction or lesson step | none | - | 5 groups |
| Käy läpi kaksi ensimmäistä väitettä. | 5 | OUT | task instruction or lesson step | none | - | 5 groups |
| Voit käyttää myös sivun tapauksia tai tehdä tehtävän keskustellen parin kanssa. | 5 | OUT | task instruction or lesson step | none | - | 5 groups |
| Yliopistojen todistusvalinnan pisteytys ja ammattikorkeakoulujen valintaperustee | 5 | OUT | yearly fact cited by the topics whose subject it is | none | - | 5 groups |
| Kytke lappujen huolet väitteisiin. | 5 | OUT | task instruction or lesson step | none | - | 5 groups |
| Avaa kuva suurempana (kuva avautuu omalle sivulleen, ja sitä voi lähentää) | 5 | OUT | heading, phase name or UI label | none | - | 5 groups |
| Lukion opetussuunnitelman perusteet 2019 (ePerusteet), Opetushallitus. Luettu 23 | 5 | OUT | source citation | none | - | 5 groups |
| Exit-kysymys sähköisesti tunnin jälkeen. | 4 | OUT | task instruction or lesson step | none | - | 4 groups |
| Tehtävät onnistuvat myös tyhjällä paperilla. | 4 | IN | site-wide fact: tasks work on paper | sentence removed from Valmistelu | front page, Näin sivustoa käytetään | gone |
| Kerää lista vain taululle. | 4 | OUT | task instruction or lesson step | none | - | 4 groups |
| Todistusvalinta ammattikorkeakouluihin, Ammattikorkeakouluun.fi. Luettu 21.11.20 | 4 | OUT | source citation | none | - | 4 groups |
| Aloituspaikkojen määrät ja ensikertalaiskiintiön osuus vaihtelevat haun ja koulu | 4 | OUT | yearly fact cited by the topics whose subject it is | none | - | 4 groups |
| Yhteishakujen hakuajat vaihtelevat vuosittain, ja ne katsotaan Opintopolun hakua | 4 | OUT | yearly fact cited by the topics whose subject it is | none | - | 4 groups |
| Tehtävän 2 vaiheet kotiin. | 4 | OUT | task instruction or lesson step | none | - | 4 groups |
| Koulutusväylät ja muut reitit lukion jälkeen | 4 | OUT | heading, phase name or UI label | none | - | 4 groups |
| Tehtävä 1 (15 min) ja Tehtävä 2 (10 min) yksin. | 4 | OUT | task instruction or lesson step | none | - | 4 groups |
| Kirjoita ajatus vain itsellesi. | 4 | OUT | task instruction or lesson step | none | - | 4 groups |
| Yliopistovalinnat.fi, Yliopistovalinnat.fi (suomalaiset yliopistot). Luettu 21.1 | 4 | OUT | source citation | none | - | 4 groups |
| Ohjaa puhumaan tapauksista, ei omista tilanteista. | 4 | OUT | lesson design: ground rule, lesson goal or table step (unsure, see report) | none | - | 4 groups |
| Opintopolun voi lukea myös englanniksi (Studyinfo); käytä sitä rinnalla, jos suo | 4 | OUT | task instruction or lesson step | none | - | 4 groups |
| osaa suunnitella tulevaisuuttaan sekä tuntee koulutusvaihtoehtoja ja työelämän m | 4 | OUT | curriculum code text | none | - | 4 groups |
| Lue muutama lappu ääneen. Älä arvioi. | 4 | OUT | task instruction or lesson step | none | - | 4 groups |
| Lukiokoulutus, Opetushallitus. Luettu 23.11.2026. | 4 | OUT | source citation | none | - | 4 groups |
| Tehtävän 1 vaiheet 4 ja 5 kotiin. | 4 | OUT | task instruction or lesson step | none | - | 4 groups |
| Kirjoita ajatus vain itsellesi paperille. | 4 | OUT | task instruction or lesson step | none | - | 4 groups |
| Ryhmä kirjoittaa kaksi kysymystä tapaukselle. | 4 | OUT | task instruction or lesson step | none | - | 4 groups |
| henkilökohtainen opintosuunnitelma: opiskelu-, ylioppilastutkinto- sekä jatko-op | 4 | OUT | curriculum code text | none | - | 4 groups |
| Käy läpi kaksi väitettä. | 4 | OUT | task instruction or lesson step | none | - | 4 groups |
| Valintakokeiden ajankohdat vaihtelevat koulutuksen ja haun mukaan, ja ne katsota | 3 | OUT | yearly fact cited by the topics whose subject it is | none | - | 3 groups |
| 15 Haku ja valinta: yhteishaku, todistusvalinta, valintakokeet | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| Tehtävä 3 pareittain yhdellä kuvitteellisella tapauksella (vaiheet 1–4). | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Yhteishakujen hakuajat vaihtelevat vuosittain, ja ne katsotaan Opintopolun hakua | 3 | OUT | yearly fact cited by the topics whose subject it is | none | - | 3 groups |
| Kysymykset ovat yksityiseen kirjoittamiseen tai vapaaehtoiseen pariin. Kenenkään | 3 | IN | generic privacy note above every open-question bank | paragraph removed; the questions stay | front page, Näin sivustoa käytetään | gone |
| Paperipohja ilman laitetta. Pari voi tehdä yhdessä. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Tuleeko sinusta ylioppilas? (koeyhdistelmien kokeilu), Ylioppilastutkintolautaku | 3 | OUT | source citation | none | - | 3 groups |
| Opit huomaamaan oman osaamisesi, kertomaan siitä omin sanoin ja kirjaamaan sen n | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Opit löytämään luotettavaa tietoa jatko-opinnoista ja työelämästä sekä tuntemaan | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Lukion opetussuunnitelman perusteet 2019 on voimassa oleva valtakunnallinen opet | 3 | OUT | yearly fact cited by the topics whose subject it is | none | - | 3 groups |
| Opit tunnistamaan, mikä auttaa sinua jaksamaan, ja tiedät, mistä saat apua, kun  | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Opit, miten lukio-opinnot on rakennettu ja miten arki lukiossa toimii, ja teet o | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Opit, mitä henkilökohtainen opintosuunnitelma on, ja teet ensimmäisen luonnoksen | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| S2 ja selkeä kieli: Käy alla oleva sanasto läpi ennen Tehtävää 1. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Opit, miten valintasi vaikuttavat jatko-opintoihin hakeutumiseen, ja tutustut op | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Opit, mitä työelämätaitoja tarvitset, ja harjoittelet työpaikan hakemista kesäty | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Kerro, että väitteet ovat keskustelun avauksia. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Exit-lappu: yksi kysymys (nimetön tai nimellä, opiskelija valitsee). | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Mielenterveystalo: nuoret (luettu 23.11.2026): tietoa ja omahoito-ohjelmia nuori | 3 | IN | generic Mielenterveystalo item (same text on 16-18) | removed from 16-18; items written for the topic stay | not restated: no help pointers on site pages (norm ledger row 3) | gone |
| Täydennä lista itse ja siirry eteenpäin. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Tulosta tapauskortit tai kirjoita tapaukset taululle. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Kysy mieluummin: "Mitä toivoisit, että valintasi mahdollistavat?" | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| 05 Itsetuntemus, vahvuudet ja arvot | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| 06 Henkilökohtainen opintosuunnitelma ja kurssivalinnat | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| Aloituspaikkojen määrät ja ensikertalaiskiintiön osuus vaihtelevat haun ja koulu | 3 | OUT | yearly fact cited by the topics whose subject it is | none | - | 3 groups |
| Opit, mistä ylioppilastutkinto koostuu, ja teet ensimmäisen version omasta yo-su | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| jatko-opintojen ja tulevaisuuden suunnittelu, jatko-opintoihin hakeutuminen Suom | 3 | OUT | curriculum code text | none | - | 3 groups |
| Päivität HOPSisi kolme osaa ja suunnittelet ylioppilaskokeiden hajautuksen niin, | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Kokoat jatko-opinto- ja urasuunnitelmasi, varaudut muutoksiin ja tiedät, mistä s | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Kerää laput ja lue muutama ääneen. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Ilmoittautuminen, Ylioppilastutkintolautakunta. Luettu 21.11.2026. | 3 | OUT | source citation | none | - | 3 groups |
| Tehtävä 2 tehdään aina. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Opit tuntemaan kansainvälisiä koulutus- ja työvaihtoehtoja, etsimään tietoa niis | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Tutustut työelämän ja yrittäjyyden eri muotoihin ja opit pohtimaan, mitä taitoja | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| lukio-opintojen kannalta kulloinkin ajankohtaiset asiat | 3 | OUT | curriculum code text | none | - | 3 groups |
| Lukion opetussuunnitelman perusteet 2019, Opetushallitus. Luettu 21.11.2026. | 3 | OUT | source citation | none | - | 3 groups |
| Tuki: Oppimisen tuesta kerrotaan lisää Opetushallituksen sivulla Oppimisen tuen  | 3 | IN | generic learning-support referral stamped in Eriyttäminen | removed (topic 15 keeps its own exam-arrangement sentence); orphaned OPH source entries removed | /opetussuunnitelma/ | gone |
| Opit sanoittamaan vahvuuksiasi ja kiinnostuksen kohteitasi ja huomaat, mikä sinu | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Kysymykset ovat yksityiseen kirjoittamiseen tai vapaaehtoiseen parikeskusteluun. | 3 | IN | generic privacy note above every open-question bank | paragraph removed; the questions stay | front page, Näin sivustoa käytetään | gone |
| Moduulin tavoitteena on, että opiskelija | 3 | OUT | curriculum code text | none | - | 3 groups |
| Osaamisen tunnistaminen, sanoittaminen ja dokumentointi | 3 | OUT | curriculum code text | none | - | 3 groups |
| 08 Tietolähteet ja ohjauspalvelut | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| S2 ja selkeä kieli: Käy sanasto läpi ennen tehtäviä. Tee halutessasi sanataulukk | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Ylioppilaskokeisiin ilmoittaudutaan oman lukion kautta, ilmoittautuminen on sito | 3 | OUT | yearly fact cited by the topics whose subject it is | none | - | 3 groups |
| Todistusvalinta yliopistoihin, Yliopistovalinnat.fi (suomalaiset yliopistot). Lu | 3 | OUT | source citation | none | - | 3 groups |
| Paperi ja kynä riittävät. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Ylioppilastutkinnon koepäivät vahvistaa Ylioppilastutkintolautakunta erikseen ku | 3 | OUT | yearly fact cited by the topics whose subject it is | none | - | 3 groups |
| Tutkintomaksut, Ylioppilastutkintolautakunta. Luettu 21.11.2026. | 3 | OUT | source citation | none | - | 3 groups |
| Opit suunnittelemaan viikkosi niin, että opiskelulle, levolle ja muulle elämälle | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Kelan opiskelusivu (opintotuki), Kela. Luettu 21.11.2026. | 3 | OUT | source citation | none | - | 3 groups |
| Virittäytyminen ja aiemman tiedon aktivointi | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| Kirjaus loppuun kotona. Tehtävä 3, Pohdinta ja exit sähköisesti tunnin jälkeen. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Ammattikorkeakouluun.fi, Ammattikorkeakouluun.fi. Luettu 21.11.2026. | 3 | OUT | source citation | none | - | 3 groups |
| sinulla ei ole vielä suuntaa lukion jälkeen ja se painaa mieltäsi | 3 | OUT | Milloin opinto-ohjaajalle, topic-specific pointer | none | - | 3 groups |
| Opiskelija voi tehdä tehtävät myös pelkällä paperilla. | 3 | IN | site-wide fact: tasks work on paper | sentence removed from Valmistelu | front page, Näin sivustoa käytetään | gone |
| Kutsuntojen ajankohdat ja ikäluokka sekä naisten vapaaehtoisen asepalveluksen ha | 3 | OUT | yearly fact cited by the topics whose subject it is | none | - | 3 groups |
| 04 Hyvinvointi ja opiskelukyky | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| 14 Koulutusväylät ja muut reitit lukion jälkeen | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| Opintoraha, asumislisä, opintolaina, niiden tulorajat ja koulumatkatuki määräyty | 3 | OUT | yearly fact cited by the topics whose subject it is | none | - | 3 groups |
| Jätä koulun oma käytäntö pois ja kerro se exitin yhteydessä. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Tuki: Lue lisää Opetushallituksen sivulta Oppimisen tuen uudistus ja kysy koulus | 3 | IN | generic learning-support referral stamped in Eriyttäminen | removed (topic 15 keeps its own exam-arrangement sentence); orphaned OPH source entries removed | /opetussuunnitelma/ | gone |
| 12 Muuttuva työelämä, yrittäjyys ja ennakointi | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| Ammatinvalinta ja urasuunnittelu, KEHA-keskus (Työmarkkinatori). Luettu 21.11.20 | 3 | OUT | source citation | none | - | 3 groups |
| Lyhyemmissä versioissa tuotos on pienempi. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Kirjataan vain se, mikä on valmista. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Kokeiden uusiminen, Ylioppilastutkintolautakunta. Luettu 21.11.2026. | 3 | OUT | source citation | none | - | 3 groups |
| Pidä keskustelu tapauksessa, ei opiskelijoiden omissa tilanteissa. Kirjoita kysy | 3 | OUT | lesson design: ground rule, lesson goal or table step (unsure, see report) | none | - | 3 groups |
| 11 Osaamisen tunnistaminen, sanoittaminen ja dokumentointi | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| Älä ehdota "oikeaa" reittiä. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Opit, miten jatko-opintoihin haetaan ja miten opiskelijat valitaan, ja teet oman | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| 16 Kansainvälisyys ja monikulttuurinen toimintaympäristö: opiskelu ja työ ulkoma | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| Kirjaus ja exit kotona. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Pidä keskustelu tapauksessa, ei opiskelijoiden omissa tilanteissa. Kirjoita ehdo | 3 | OUT | lesson design: ground rule, lesson goal or table step (unsure, see report) | none | - | 3 groups |
| 17 Oma talous, opintotuki ja asuminen | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| 07 Ylioppilastutkinto ja alustava yo-suunnitelma | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| saa tukea elämänsuunnitteluun ja -hallintaan sekä koulutukseen ja uravalintoihin | 3 | OUT | curriculum code text | none | - | 3 groups |
| Koepäivät, Ylioppilastutkintolautakunta. Luettu 21.11.2026. | 3 | OUT | source citation | none | - | 3 groups |
| Tutustut lukion jälkeisiin reitteihin vaihtoehtoina ja kirjaat omat kiinnostukse | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Tutkinnon rakenne, Ylioppilastutkintolautakunta. Luettu 21.11.2026. | 3 | OUT | source citation | none | - | 3 groups |
| Kysy koulusi omasta käytännöstä opinto-ohjaajalta (esimerkki). | 3 | IN | generic learning-support referral stamped in Eriyttäminen | removed (topic 15 keeps its own exam-arrangement sentence); orphaned OPH source entries removed | /opetussuunnitelma/ | gone |
| HOPSiin he kirjaavat vain sen, minkä haluavat jakaa koulun kanssa. | 3 | OUT | lesson design: ground rule, lesson goal or table step (unsure, see report) | none | - | 3 groups |
| Europass, Euroopan unioni (Europass). Luettu 21.11.2026. | 3 | OUT | source citation | none | - | 3 groups |
| asettaa valintojaan tärkeysjärjestykseen suhteessa omiin suunnitelmiinsa | 3 | OUT | curriculum code text | none | - | 3 groups |
| Opit tunnistamaan omat tapasi oppia ja kokeilet työtapoja, jotka auttavat lukio- | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Tehtävä 1 kotiin ja Tehtävä 2 heti. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| 03 Ajankäyttö ja arjen hallinta | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| Sivuston ohje: kirjaa siihen vain se, minkä haluat koulun tietävän. | 3 | IN | student-facing HOPS privacy reassurance stamped in Itseopiskelun askel | privacy sentences removed; what to write stays | /polku/ | gone |
| 02 Opiskelutaidot ja oppimaan oppiminen | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| Ohjaa puhumaan tapauksista, ei omista suunnitelmista. Kokoa kysymykset taululle. | 3 | OUT | lesson design: ground rule, lesson goal or table step (unsure, see report) | none | - | 3 groups |
| 09 Valinnat ja jatko-opintopolut | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| Erityisjärjestelyt, Ylioppilastutkintolautakunta. Luettu 21.11.2026. | 3 | OUT | source citation | none | - | 3 groups |
| Kerro koulun oma käytäntö (esimerkki). | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| 18 Jatko-opinto- ja urasuunnitelma ja siirtymä lukion jälkeen | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| Tehtävä 3 (10 min) pienryhmissä kuvitteellisilla tapauksilla. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Varaa nimettömiä lappuja virittäytymiseen ja exitiin. Tapauskortit ovat vapaaeht | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| 13 Työelämätaidot ja työnhaku: kesätyö, hakemus, haastattelu | 3 | OUT | heading, phase name or UI label | none | - | 3 groups |
| Suomen kansanopistoyhdistys, Suomen Kansanopistoyhdistys. Luettu 21.11.2026. | 3 | OUT | source citation | none | - | 3 groups |
| Kerro, että väitteet ovat keskustelun avauksia, ja kytke lappujen asiat väitteis | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
| Ylioppilaskokeista peritään tutkintomaksuja, ja niiden suuruus vahvistetaan erik | 3 | OUT | yearly fact cited by the topics whose subject it is | none | - | 3 groups |
| Ilman laitetta: Kaikki kolme tehtävää onnistuvat paperilla ja kynällä. | 3 | OUT | the topic's own no-device version (contract item 6) | none | - | 3 groups |
| Opit tekemään oman talouden suunnitelman, tunnistamaan opintotuen osat ja mietti | 3 | OUT | topic summary shown in listings | none | - | 3 groups |
| Kirjoita yksi kysymys, jonka voisit kysyä opinto-ohjaajalta. | 3 | OUT | task instruction or lesson step | none | - | 3 groups |
