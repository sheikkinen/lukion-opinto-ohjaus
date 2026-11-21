# Brief 004: judgement

**Judge:** Opus, outside the authors. I wrote nothing in this project. Date: 2026-11-21.
**Ruled from files:** `prompts/004-lesson-quality.md`, `CLAUDE.md`, `docs/review/2026-11-21-brief-002-open-items.json`,
`content/topics/*.md`, `data/`. I made no web reads, so legal points are ruled against what the topics, the earlier
facts check and the brief record. Nothing was edited except this file, and nothing was committed.

## Verdict: accept-with-minors

The brief's expected result holds. Every 75, 60 and 45 minute table adds up, and topic 07 also has a 90 minute table.
The goal task is kept in every variant, or the Tavoite line says what the shorter plan leaves out. Task times vary.
No offline alternative needs a counsellor's printer. The HOPS privacy line ("koulun kanssa jaettu") appears 3 to 6
times in each of the 18 topics. A gender-aware assumption check is in all 18 plans. The round 1 and 2 must-fix items I
spot-checked are fixed: Mira in 14, the siviilipalvelus wording in 14 and 18, the "tuki ei katoa" line in 16, step 4 in
16's 60-minute plan, and 01's HOPS row, which now uses Tehtävä 1.

None of the seven final open items blocks acceptance. Two of them (6 and 7) are wrong statements about the curriculum
and the law. Each is a one-line fix and should be made before the push, as the publishing check requires.

**Build:** `python -m pipeline.build` gave 0 errors and 21 warnings. All 21 are "no picture file yet" in
`data/images.yaml`, which brief 003 owns. **Tests:** `python -m pytest` gave 82 passed.
**Read in full:** 05 (01–06), 07, 09 (07–12), 13 (13–15) and 18 (16–18), including their plans and offline
alternatives. I spot-checked 01, 02, 14, 15 and 16 by grep.

## Final recheck's open items

| # | Item | Real? | Blocks publishing? | Ruling |
|---|---|---|---|---|
| 1 | Offline alternatives that say "tältä sivulta" or "tällä sivulla" (01–06 T3, 13 T1/T2/T3, 14 T1/T3, 15 T3, 16, 17, 18) | Partly | No | 01–06 already say "tai kopioi ne paperille", which is the fix the item asks for. A student following the task is already reading the page, and none of these needs a printout. 13–18 lack the copy instruction ("Lue tapaukset tältä sivulta"). That is a wording fault, not a task the student cannot do. Add "kopioi tapaus paperille ensin" or the 07–12 invent-a-case line. |
| 2 | 05 Tavoite and HOPSiin promise "yksi asia, jonka haluat oppia", which no required task produces | Yes | No | Confirmed. Only Pohdinta 3 asks for it, and it is one of three choices. Add one line to Tehtävä 1 step 5 ("…ja yksi asia, jonka haluat oppia"), or drop the promise. |
| 3 | Outcomes that no required task practises (03 o2/o4, 04 o2, 05 o3, 06 o4, 18 o5) | Yes, thin coverage | No | Confirmed for 05 o3 (beliefs and people appear only in the optional Oskari case) and 18 o5 (Niko in optional Task 3, but the Tukea section and the 45/60/75 claim answers cover the rule). The others are read or reflected on, not done. The style guide asks for practice, so fold one step into an existing task. This is not a safety or truth problem. |
| 4 | 45-minute plans that contradict their own goal (18, 13, 15, 01, 14, 09) | Mostly | No | **01 is stale:** the HOPS row now uses Tehtävä 1's map and sends Tehtävä 2 home. **18 is real:** a 7-minute row holds three HOPS lines, step 5 and the exit. It is tight but possible, so add 2 minutes from Työskentely or move step 5 into it. **13 is real:** the Tavoite, the row and "Jos aika loppuu" give three different products. **15 is real:** the HOPS row asks for the pääsyvaatimus from step 4, which is not done. **14 is real:** the Tavoite does not name what moves home. **09 is minor:** Task 2 lists Task 1 notes, but its steps work without them. All are alignment edits. A counsellor can still teach each lesson and reach the core goal. |
| 5 | Yo-tutkinto rule "neljä koetta vähintään kolmesta ryhmästä" said to overstate Laki 502/2019 § 10 | Partly | No | The 07 and 10 wording matches the YTL page "Tutkinnon rakenne", which the round 1 facts check read and confirmed, and the text links it with "tarkista aina". With today's tests, "äidinkieli + four tests from at least three groups" requires the same as "äidinkieli + three groups + any fifth". So the claim that the text overstates the rule is not established from the files. Two points are real: the § 11 exception (äidinkieli in place of a language test) is missing, and "pitkän oppimäärän" is YTL's "vaativampi koe" in plain words. Add one line, "poikkeuksista katso YTL". Not a rule-3 breach. |
| 6 | 01 splits "valtakunnalliset valinnaiset opinnot" into "syventävät ja soveltavat" | Yes | Fix before push (one line) | LOPS 2019 and `data/curriculum.yaml` have no such split. It is LOPS 2015 terminology, so this presents a curriculum structure that is not in the perusteet (rule 3). Remove it at 01:88 and in the glossary at 01:270, and reword "yhteisiä kaikille lukioille" to "valtakunnallisesti määriteltyjä; koulu päättää, mitkä tarjoaa". Citing asetus 810/2018 in `law` (01, 18) is a minor. **Note for brief 003:** the same split is in `data/images.yaml` (dg card two) and in `images.run.yaml`. |
| 7 | 02:98 "oikeus oppimisen ja opiskelun tukeen" | Yes | Fix before push (one line) | 16, 17 and 18 say "oikeus oppimisen tukeen". 02 adds a right the law is not shown to give. Change 02 to the same words. |

## Done-when

| Done-when line | Ruling |
|---|---|
| A counsellor can teach any topic in 45 minutes and reach its goal | **Met, with minors.** All 45-minute tables add to 45, drop the group phase and keep the goal task. Item 4's mismatches (13, 15, 18, 14) are about what the Tavoite names, not about whether the lesson works. |
| A student alone can do every task, also without a device | **Met, with a minor.** Every "Ilman laitetta" line works with paper and pen, and printouts are optional everywhere. Item 1 is wording in 13–18. |
| No task asks for anything that should not go into a shared HOPS | **Met.** All 18 topics say HOPS is shared with the school, and they keep health, family, support needs and money in the student's own notes. 05 is voluntary. 02's support note sits in the muistio. |
| Pedagogy, curriculum and facts checks have no must-fix left, or each is named here | **Met.** The seven final items are named above. The facts minors still open, not blocking: 05 links an OPH teacher resource for students, and the ILMO, Vipunen and Finlex pages were not re-read (script-rendered). |
| The judge accepts | **Accepted with minors.** |

## Remaining items (no third round; batch them into the next content brief)

1. Before push: fix 01 syventävät/soveltavat (item 6) and 02 "ja opiskelun" (item 7).
2. Add a "copy the case onto paper first" or invent-a-case line to the offline tasks in 13–18 (item 1).
3. Align Tavoite, rows and task steps in 13, 14, 15 and 18, and give 18's 45-minute HOPS row 9 minutes (item 4).
4. 05: add "yksi asia, jonka haluat oppia" to a task step (item 2). Add one task step each for 05 o3 and 18 o5,
   and fold 03 o2/o4, 04 o2 and 06 o4 into existing steps (item 3).
5. 07 and 10: add the äidinkieli exception and "poikkeuksista katso YTL" (item 5).
6. Cite asetus 810/2018 in `law` for 01 and 18 (S/H). Have a human check Finlex 714/2018 §§ 25, 28 once.
7. 05: mark the OPH "Miten valitsen oman alani?" link as a teacher resource, or drop it.
8. Brief 003: remove the syventävät/soveltavat line from the dg infographic in `data/images.yaml`.

## For the operator

- Accepted with small fixes: the lessons now fit 45 minutes, work on paper, and keep private things out of the HOPS.
- Two one-line errors must be fixed before the site goes public: one wrong curriculum term in topic 01 and one wrong law wording in topic 02.
- The other items are polish and can wait for the next content round.
- The build is clean apart from the missing pictures, which brief 003 owns. All 82 tests pass.
- Nothing has been committed or pushed.
