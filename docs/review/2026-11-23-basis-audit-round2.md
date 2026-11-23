# Basis audit, round 2: judgement

Judge for round 2 of the basis audit of lukion-opinto-ohjaus, 2026-11-23. The judge wrote none of the edits. This is
not the round-1 judge. Ground: the shared guideline (`lukio-runko/docs/content-guideline.md`, sections 1-4), the norm
ledger (`lukio-runko/docs/norm-ledger.md`, rows 3-8), the round-1 judgement (`2026-11-22-basis-audit.md`), the site
contract with its new addendum, and the style guide.

## What was checked

- The config result: contract addendum "no help blocks or emergency lines", style guide sections 1, 7 and 10, and
  decision D-015. All three are on disk. The addendum keeps "Milloin opinto-ohjaajalle" as subject content.
- Topics 01-06: fixer, verifier, redo and a second verifier. The second verifier left one item (05, see below).
- Topics 07-18: only part of the group results reached the judge. The judge checked these files on disk directly.
- The judge's own checks: a build of the working tree and of committed HEAD, a cluster-by-cluster comparison of the
  repeat warnings, a grep of all 18 topics, YAML parsing, line counts, the visual novel lines, and ten spot-checks
  against sources the judge opened.

## Build

- Working tree: 0 errors, 234 warnings. HEAD: 0 errors, 245 warnings. The count went down by 11.
- Every warning is a repeat cluster. There are no length or structure warnings.
- 15 cluster texts are new compared with HEAD. None is a new sentence of teaching content:
  - Source-list lines with new read dates (LOPS on ePerusteet, OPH Lukiokoulutus, Finlex, Mielenterveystalo).
  - Privacy reminders that lost their "HOPS on koulun kanssa jaettu asiakirja" prefix: "Kirjaa HOPSiin vain se,
    minkä haluat koulun tietävän" (6 topics), "Muistuta: HOPSiin kirjataan vain se…" (6), "Muistuta tunnin alussa ja
    lopussa…" (6), "HOPSiin: Kirjoita siihen vain se…" (5). The text behind them was already at HEAD. They belong to
    the pending privacy decision.
  - "Voit puhua myös ryhmänohjaajan, erityisopettajan tai opiskeluhuollon kanssa" (12 topics, 07-18). The same line
    was in all 18 topics at HEAD. Group 1 removed it from 01-06; the other groups kept it.
  - `law: Lukiolaki 714/2018 § 26`, now in 12 topics.
- Files are 288-369 lines, under the 500 cap. Front matter parses as YAML in all 18 files.

## Safety apparatus (guideline section 4, ledger rows 3-4)

A grep of all 18 topics found:

- No 112 line, no "hätänumero", no "Hätätilanteessa", no "Jos olet heti vaarassa" block.
- No Sekasin, MIELI Kriisipuhelin or Nuorten Exit, in text or in `official_links`.
- No content_note, in front matter or as a note at the top.
- No "kysyminen ei ole heikkoutta" type line.
- "Kuraattori" appears only as subject content: the LOPS list of student welfare services in 04, S2 glossaries,
  `school_adapts`, and the 04 paper task that lists school staff.
- "Milloin opinto-ohjaajalle" stays in all topics. Its links (Ohjaamo, OPH opiskeluhuolto, Mielenterveystalo
  self-help, Työmarkkinatori, Yhdenvertaisuusvaltuutettu) are dated and are not crisis lines.

Round-1 item 1 is resolved.

## Spot-checks against opened sources

All ten match.

1. 18, post-lukio guidance: matches Finlex, lukiolaki 714/2018, 25 § 4 mom., word for word in substance.
2. 18, HOPS in three parts, drawn up with staff support, updated regularly: matches 26 § 1-2 mom.
3. 01, "vähintään 150 opintopistettä": the OPH Lukiokoulutus page states it.
4. 01, "vähintään 20 op valtakunnallisia valinnaisia": LOPS 2019, chapter Opintojen rakenne.
5. 01, opinto-ohjaus marked S/H: LOPS, chapter Numeroarvosanat ja suoritusmerkinnät.
6. 01 and 06, the student draws up HOPS with the support of teaching and guidance staff: LOPS, chapter
   Opetussuunnitelman laatiminen.
7. 04, opiskeluhuolto is "ensisijaisesti ennaltaehkäisevää yhteisöllistä työtä": LOPS, chapter Opiskeluhuolto.
8. 10, the registration verdict ("ei vapaasti … sitova … peruuttaa kirjallisesti takarajaan mennessä … painava
   syy"): the YTL Ilmoittautuminen page states each part.
9. 10, the exam structure (five exams, mother tongue, at least one long syllabus): the YTL Tutkinnon rakenne page.
10. Removed items stay removed: no "hyvä kysymys" closer in 07-18, no "Muista, että" in 12, no "rohkeaa" in 04, no
    "Uni ei vaikuta oppimiseen", no "ei koskaan valmis" in 05. 06 Pelisäännöt reads "Sivuston ohje".

A note on Finlex. Round 1 and the group 1 agents got only the Finlex site shell. A plain download of the Finlex page
does contain the full law text, inside the page data. The judge read 25 § and 26 § that way. So the 18 law sentences
are verified. The section numbers are correct.

## Round-1 items

| # | Item | Status |
|---|---|---|
| 1 | 112, hätänumero and crisis blocks | resolved in all 18 topics |
| 2 | Unverified law claims | resolved: 01-06 now cite LOPS chapters; 13-17 dropped the 26 § sentence; 18 keeps 25 § and 26 §, which the judge verified on Finlex |
| 3 | "HOPS on koulun kanssa jaettu asiakirja", 06 Pelisäännöt | resolved: removed, or labelled "Sivuston ohje" |
| 4 | Praise and filler | resolved: no "hyvä kysymys", "Kiitä", "rohkeaa" or "Muista, että" left |
| 5 | False balance on sleep | resolved: the statement is gone, and 04 now uses the 03-style prompt |
| 6 | 01 "tarua" verdicts | resolved: they cite LOPS |
| 7 | 02 and 05 small items | resolved |
| 8 | Process | the ledger lives in lukio-runko, as intended; nothing is committed |

## What remains (small wording issues)

1. **Reassurance lines left in student text.** The same kind group 1 removed from 01-04:
   - 05: "Valintoja ei tarvitse tehdä nyt." (flagged by the second verifier, not yet removed)
   - 07: "Sinun ei tarvitse päättää kaikkea nyt." The next sentence ("luonnos, jota päivität myöhemmin") carries the
     content and can stand alone.
   - 17: "Sinun ei tarvitse osata kaikkea." Keep "Ensimmäinen suunnitelma saa olla karkea" only if it carries
     information.
2. **"Voit puhua myös ryhmänohjaajan, erityisopettajan tai opiskeluhuollon kanssa"** is still in 07-18 (12 topics),
   while 01-06 removed it. Remove it in 07-18 too. It is a repeat, and the rule prefers removal.
3. **Law entries no sentence uses.** 07-17 keep `law: Lukiolaki 714/2018 § 25/26`, and 13-17 keep a Finlex
   `official_links` entry, but no sentence in those topics relies on the law. The source is real and readable, so
   this is not an invented source. Remove the entries, or keep them only where a sentence uses them.
4. **Mood thresholds without a basis.** "Milloin opinto-ohjaajalle" in 01-05 keeps triggers such as "alakuloinen
   suurimman osan päivistä yli kaksi viikkoa" (01, 04) and "tuntenut itsesi arvottomaksi … yli kaksi viikkoa" (05).
   They read like a screening rule, and no source is cited. 13-18 removed the same kind of threshold. The section is
   subject content, so the judge lists this for the operator, not as a defect.

## Pending operator decisions (not changed, not judged)

- Repeated privacy notes: "Niitä ei tarvitse näyttää kenellekään", "Kirjoita siihen vain se, minkä haluat jakaa",
  "mitään ei tarvitse kertoa muille", "Kenenkään ei tarvitse vastata ääneen", 05 "Muistio on sinun omasi…", and the
  HOPS privacy reminders in the lesson plans (ledger row 5).
- Notes about fictional materials ("kaikki henkilöt ovat kuvitteellisia").
- Unofficial scoring notes.
- 04 counsellor preparation: "Lue läpi koulun kriisisuunnitelma…". It is school practice, not a student help block.
- The mood thresholds in item 4 above.
- Visual novel lines: one "Pelaa aiheesta visual novel" line in each of the 18 topics, untouched.

## Verdict

**accept-with-minors.** Every guideline item from round 1 is fixed. No help block, 112 line, crisis line or content
note is left. The build has 0 errors, and the repeat warnings went down from 245 to 234. Ten spot-checks match their
sources. What remains is wording: three reassurance lines, one repeated referral line, unused law entries, and
thresholds for the operator to decide.

## For the operator

- The emergency lines and crisis blocks are gone from all 18 pages.
- The law sentences in topic 18 were checked against the law text and are correct.
- A few "you don't have to…" lines and one repeated "talk to staff" line remain. They are small and quick to remove.
- Please decide on the privacy notes and on the "more than two weeks" mood triggers in topics 01-05.
- Nothing is committed.

## 23.11.2026, round 3

Judge for round 3. The judge wrote none of the edits. The fixer worked on round-2 items 2 and 3 only. Ground: the
shared guideline (sections 1-4), the norm ledger (rows 3-7), the site's CLAUDE.md and the round-2 judgement above.

### Round-2 items on disk

| # | Item | Status |
|---|---|---|
| 1 | Reassurance lines in 05, 07, 17 | not changed; one-off reassurances are operator-pending this round, so not judged |
| 2 | Referral line "Voit puhua myös ryhmänohjaajan…" in 07-18 | fixed: in no topic file and on no built page |
| 3 | Unused law entries | fixed: 07-17 lost `Lukiolaki 714/2018 § 25/26`; 13-17 lost the Finlex entry; 18 keeps both, and its 25 § and 26 § sentences are intact. The Finlex link is now on 18 (two pages), lahteet and opetussuunnitelma only |
| 4 | Mood thresholds in 01-05 | operator-pending, not changed |

07 and 10 keep `law: Laki ylioppilastutkinnosta 502/2019`. No sentence names the law, but the exam rules these topics
teach (registration, structure) are YTL rules made under it, and those sentences cite YTL pages. The judge accepts
the entry as a front-matter basis. The operator may drop it.

### New defect from this round (minor)

In 07-12 the referral line was the only thing between the "Varaa aika opinto-ohjaajalle, jos" list and the Ohjaamo
link (round 2 had already removed the "Apua saat myös:" label in these six topics). With the line gone, the Ohjaamo
link is now the last item of the trigger list. The built pages show it as one `<ul>`, so it reads "jos … Etsi lähin
Ohjaamo". Fix: delete the Ohjaamo bullet in 07-12 (Ohjaamo stays in each topic's `official_links`). Do not add a label
back: "Apua saat myös:" is already in 12 topics.

### Checks

- Build into the judge's own folder: 0 errors, 231 warnings (round 2: 234). All warnings are repeat clusters.
- Repeat clusters: the fixer's script only deletes text. Compared with HEAD, no cluster in 5 or more topics is new
  except the source-list read dates and the privacy reminders round 2 already listed. The four new 3-topic clusters
  are older text, below the threshold. This round added no repeat cluster.
- Grep of all topics and data for 112, hätänumero, Sekasin, kriisipuhelin, "ohjaa opiskeluterveydenhuoltoon",
  kuraattorin yhteystiedot and content_note: nothing. The only near hit is 04, the LOPS sentence on the right to
  opiskeluterveydenhuolto, which is subject content. `yearly-facts.yaml` has no helpline or 112 entry.
- Built pages: no standalone "112" anywhere in the out folder. This site has no 08-mielenterveys page.
- Front matter parses as YAML in all 18 topics; the data files parse. Files are 288-365 lines.
- Visual novel lines intact: one "Pelaa aiheesta" line and four visual novel references in each of the 18 topics.
- No local path or e-mail in content or data. CLAUDE.md, decisions and docs other than this file are as round 2 left
  them. Nothing is committed.

### For the operator to decide

- "Apua saat myös:" lists stay in 01-06 and 13-18. Most link Ohjaamo, OPH opiskeluhuolto or Työmarkkinatori, and
  several link Mielenterveystalo: nuoret (self-care programmes). They hold no 112 or crisis line, and round 2 counted
  them as part of the "Milloin opinto-ohjaajalle" subject content. They are close to the help-block pattern of ledger
  row 3. Decide whether the Mielenterveystalo links stay.
- Round-2 items 1 and 4 and the other pending items are unchanged.

### Verdict

**accept-with-minors.** Round-2 items 2 and 3 are fixed on disk and in the build, and no help block, 112 line,
helpline or content note is left. The build has 0 errors, and this round added no repeat cluster. One minor defect
came from the deletion: in 07-12 the Ohjaamo link has joined the "Varaa aika… jos" list. Delete that bullet.
