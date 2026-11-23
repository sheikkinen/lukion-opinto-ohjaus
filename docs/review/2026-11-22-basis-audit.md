# Basis audit: judgement

Judge for the basis audit of lukion-opinto-ohjaus, 2026-11-23. The judge wrote none of the edits. Ground: the shared
guideline `lukio-runko/docs/content-guideline.md` (v0.4.0, sections 1-4), the site's CLAUDE.md, `docs/content-contract.md`
with all addenda, and `docs/style-guide.md`. Decision behind the audit: D-014 ("Guideline and audit").

## What was audited

- Topics 01-06: one auditor read them in full, a fixer applied the items, and a verifier re-read them. Verifier: not passed.
- Topics 07-12: one auditor checked them against the YTL pages it opened. Only part of this result reached the judge.
- Topics 13-18: no audit result reached the judge, but the working tree has edits in all 18 topic files (uncommitted).
- Judge's own checks: a build of the working tree and of committed HEAD, line and word counts, a grep of the whole tree
  for the flagged phrases, ten spot-checks of fixed items, two spot-checks of groups the auditors called clean, and two
  tries at Finlex.

## Build

- Working tree: 0 errors, 249 warnings. HEAD: 0 errors, 245 warnings. Every warning is a repeated-text cluster. The
  "0 warnings" target is not met, either before or after this round.
- Four of the new clusters come from this round's own edits: "HOPS on koulun kanssa jaettu asiakirja" (6 topics),
  "Sivuston lähtökohta: reittejä ei laiteta paremmuusjärjestykseen" (6), the § 26 sentence (3-6), and "Kerää laput,
  sekoita ja lue muutama ääneen" (8).
- The largest file has 385 lines, so all are under the 500 cap. Opiskelijalle has 385-548 words, under the 600 cap.

## Findings by type and action (topics 01-06, 33 items as audited)

| Type | Count | Add basis | Label as site's own | Reword as weighing | Reword idiom | Status after fix |
|---|---|---|---|---|---|---|
| No basis | 21 | 9 | 8 | 3 | 1 | resolved by removal or label; none got a new source |
| Basis mismatch | 4 | 4 | - | - | - | law-dependent ones softened, not verified |
| English habit | 5 | - | - | 1 | 4 | resolved in 01-06 only |
| Value graded | 3 | 1 | - | 2 | - | resolved |

07-12, from the part of the result that reached the judge: four mismatches with opened YTL pages (the cancellation
rule, "vaativampi koe", the exception example, the order of the route list) and unlabelled site frameworks. The four
are fixed on disk.

## Spot-checks

Fixed on disk (verified): 10 "vaativampi koe" removed; 10 exception example replaced; 10 cancellation answer now
"ei vapaasti ... perua kirjallisesti takarajaan mennessä"; 09 route list is now in alphabetical order and labelled
"sivuston linjaus"; 02 three questions and 03 five steps carry "Sivuston oma jäsennys"; 02 and 04 model-answer hints
are now discussion openers; no "Kiitä" remains; "yhtä arvokkaita" is now "Sivuston lähtökohta ... samanarvoisia".
Clean groups (agree): the 07 exam structure rules (five exams, mother tongue, a long-syllabus exam) and the retake row
match the YTL pages listed in its front matter.

## What remains

1. **Section 4, safety apparatus (operator rule).** 04, 05 and 18 open "Milloin opinto-ohjaajalle" with a bold
   "Jos olet heti vaarassa ... Soita 112" block. 04 Opiskelijalle line 113 repeats it ("soita hätänumeroon").
   14 topics (03-18) add "Hätätilanteessa soita hätänumeroon" to the Kriisipuhelin link. The guideline allows one
   help block, in terveystieto only. Plain help links with read dates, which the contract requires, may stay.
2. **Section 1, new unverified law claim.** "Lukiolain 26 §:n mukaan HOPS laaditaan oppilaitoksen
   opetushenkilöstön tuella" was added this round in 13-18 (HOPSiin step and lesson plan). Its Finlex link is dated
   22.11.2026, but Finlex served only its site shell to the auditor, the verifier and the judge (two tries each).
   `law` still lists § 25 in all 18 topics and § 26 in 01 and 06. In 02-04, no sentence relies on § 25.
3. **Section 1, HOPS facts.** "HOPS on koulun kanssa jaettu asiakirja" is stated without a basis in 01-12, as is
   "Terveys-, perhe- ja talousasiat eivät kuulu siihen" in 06 Pelisäännöt. Label these as site advice or school
   practice (esimerkki).
4. **Section 4, praise and filler.** The closer "se on hyvä kysymys seuraavaan ohjauskeskusteluun" is still in
   07-18, and "Muista, että" is still in 12. In 04, "rohkeaa" is mild praise.
5. **Section 2, false balance.** 04 runs "Uni ei vaikuta oppimiseen" through the weighing prompt "milloin tämä voisi
   pitää paikkansa". This is an empirical question, so it needs a sourced answer or should be dropped.
6. **01 lesson plan.** It keeps its "tarua" verdicts on the three-group split, but the page labels that split as the
   site's own explanation.
7. **Smaller items.** 02 "Ne eivät ole synnynnäisiä" has no basis. The 02 S2 glossary is unlabelled. 05 says
   "arvot voivat muuttua" and "ei koskaan valmis" with no basis.
8. **Process.** The site has no `docs/norm-ledger.md`; the ledger exists only in the engine. 13-18 changed without
   an audit result reaching review. Nothing is committed.

## Verdict

**reject.** Most of the 01-12 items are resolved, and the build is structurally clean. But the site does not yet
meet guideline section 4: the 112 and hätänumero blocks appear on 15 pages, against an explicit operator rule.
Section 1 is not met either: a new law claim cites a section nobody could open, and the HOPS facts have no basis.
The fixes are small and mechanical. A second round should be judged by a different agent.

## For the operator

- Most of the flagged claims in topics 01-12 are now removed, or marked as the site's own view.
- The emergency lines ("soita 112", "hätänumeroon") are still on 15 pages and must come out.
- No one could open the law text on Finlex, so the HOPS law sentences in 13-18 are unchecked.
- Nothing is committed. One more fix round is needed, and then a new judge.
