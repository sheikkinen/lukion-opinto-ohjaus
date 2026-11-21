# Brief 007 judgement: clear the eleven open minors

**Judge:** Opus, outside the authors. **Date:** 2026-11-21. **Brief:** `prompts/007-clear-minors.md`.
**Verdict: reject (one small content round needed).** Ten of the eleven items are fixed. Item 2 has two defects
left in topics 06 and 18: a step that marks a table no step creates, and an outcome left without a task step. Both
are a few lines in `content/`. Everything else, including the image budget, passes.

## Gates I ran myself

- `python -m pipeline.build` (LOO_TODAY=2026-11-21): 0 errors, 0 warnings.
- `ruff check .`: all checks passed.
- `pytest -q`: all tests pass (98).
- File length: largest code file is `pipeline/checks.py` at 402 lines; none over 500.
- Nothing committed for this brief (HEAD is `0fcc3da`, brief 008 written-before; brief 007 work is uncommitted).

## The eleven items

| # | Item | Ruling | Evidence |
|---|------|--------|----------|
| 1 | Topic 09 "Varusmiespalvelus" -> "Asepalvelus" | Fixed | `09-jatko-opintopolut.md:103` "Asepalvelus tai siviilipalvelus", same as topic 14 line 95 and the diagram |
| 2 | One action per step, at most five steps (03-06, 18) | **Not fixed** | Steps are split and none has over five, but two defects remain (see below) |
| 3 | Topic 18 45 min "kotiin" vs HOPS row; topic 13 names the task | Fixed | 18: cut column "Tehtävän 2 vaiheet 3 ja 4 kotiin" (line 267), goal line 236 agrees, HOPS row keeps step 5. 13: "Tehtävän 1 vaiheet 4–5 ja Tehtävän 2 vaiheet 4–5 kotiin" (line 225), goal line 196 agrees |
| 4 | Print one lesson length; whole view prints without JS | Fixed | `id="tunti-75/60/45"` blocks, plain "Tulosta 75/60/45 min / kaikki pituudet" anchors, `print.css:35` `:has(.plan-length:target)` rule. PDFs in `tmp/shots-007/`: one length 7 pages, all 11 pages |
| 5 | Headings "Tuntisuunnitelma (N min)", check adjusted | Fixed | Built topic 18 lesson view has exactly one of each; `pipeline/plan.py` accepts the new and old forms; tests in `tests/test_plan_print.py` |
| 6 | View links in the same place, current view marked | Fixed | Switch after the picture in both views, `aria-current="page"` plus bordered bold style; screenshots `t18_student_*`, `t18_tunti_*` |
| 7 | `/polku/` without JS: no dead buttons | Fixed | `data-js-only hidden` wrapper plus `site.css:165` guard; `polku_nojs_500.png` shows no counter or buttons |
| 8 | Dates d.m.yyyy everywhere | Fixed | `/opetussuunnitelma/` reads 21.11.2026 and 22.5.2026; ISO dates only in `datetime=` attributes |
| 9 | `il-op2-17`: no stray lamp, top half filled, one scene | Fixed | Opened the image: one room, window and curtains fill the top, nothing floats, no lamp |
| 10 | `il-op2`: no pleated skirts or uniform look | Fixed | Opened the image: four students from behind, all in trousers or jeans, varied colours, five paths |
| 11 | Routes diagram: caption off the bottom edge, same labels | Fixed | Opened the image: all ten labels correct, caption clear of the edge (about 24 px of 896; tight but not touching) |

## Rulings on the open items

1. **Topic 06 Task 1 (item 2): upheld, must fix.** Step 2 (line 125) says "Merkitse paperille tehtyyn taulukkoon",
   but no numbered step makes the table; only the "Ilman laitetta" line does. Fix: make step 2 "Tee paperille
   taulukko seuraaville kahdelle jaksolle" and step 3 the marking of compulsory courses; move "Lisää valinnaisia"
   into the closing "Voit ..." paragraph or merge with step 4's slot so the task stays at five steps.
2. **Topic 18 Task 2 (item 2): upheld, must fix.** Step 5 (line 170) asks for one thing done better. The HOPS rows
   (e.g. line 268) still promise "kaksi asiaa ... ja yhden taidon, jota vahvistavat (Tehtävä 2, vaihe 5)", and the
   outcome at lines 80 and 207 ("nimetä yhden taidon, jota haluan vahvistaa") now has no step; the skill sits only
   in the optional "Jos ehdit" paragraph. Fix: step 5 asks for the skill to strengthen (with the "osaan paremmin"
   part folded in or moved to the note), and the HOPS rows say "yhden asian, jonka osaavat nyt paremmin, ja yhden
   taidon, jota vahvistavat". The three HOPS rows (lines 245, 257, 268), step 5 and the outcome must agree.
3. **Image budget: dismissed.** `data/images.run.yaml` had 37 entries at commit `75a2b3c`; the ledger is
   cumulative. Brief 007 added entries 38-42 only (see below), $0.0822, within the $0.50 cap. The $0.5532 figure is
   the all-briefs total.

## Image spend for brief 007

| Entry | Picture | Model | Dollars |
|---|---|---|---|
| 38 | dg-reitit-lukion-jalkeen | nano-banana-2.1 | 0.0336 |
| 39 | il-op2 | p-image | 0.0050 |
| 40 | il-op2-17-talous-ja-asuminen | p-image | 0.0050 |
| 41 | il-op2 | p-image | 0.0050 |
| 42 | il-op2 | nano-banana-2.1 | 0.0336 |
| | **Total** | | **0.0822** |

Five generations against "up to three remakes, about $0.10" in the brief: more tries than planned, cost within the
plan and the cap.

## Remaining (not blocking once item 2 is fixed)

- Print of one length is 7 pages for topic 18, not "about 4-5": pages 6-7 are sources and the curriculum box,
  which print with every length. Worth a later look (for example, sources only on "kaikki pituudet").
- Topic 18 line 105 says "varusmies- tai siviilipalvelus" in student text; outside item 1 but the same wording
  drift. The style-guide glossary still lists "varusmiespalvelus".
- Topic 03 Task 3 step 5 still names two things (one that helped, one to practise).
- Several actions moved into "Jos ehdit" paragraphs (03, 05, 06, 18); no other outcome found that depends only on
  them, but the self-study view does not number them.
- Topic 05 Task 2: privacy note now after the steps; "Ilman laitetta" names step 4 as needing a device, but only
  step 3 does.
- Routes diagram caption margin (24 px) is smaller than the caption height; acceptable.
- No real print-dialog test of the one-length print in a non-headless browser.
- `docs/known-issues.md` to be updated by the producer after acceptance and push.

## For the operator

1. Ten of the eleven fixes are done and look right on the built site, including the three new pictures.
2. One fix is half done: two task texts (topics 06 and 18) now point at things the student is never asked to do.
3. That is a few lines of Finnish text; one short content round, then a recheck, should close it.
4. The pictures cost about 8 cents in this brief, well under the 50-cent limit.
5. Printing one lesson length now gives 7 pages instead of 13; the last two are the source list.

## Re-judgement 2026-11-21

**Judge:** Opus, outside the authors. **Scope:** the content round after the reject above, and the remaining list.
**Verdict: accept with minors.** Both item 2 defects are fixed, and the five remaining content minors I listed are
cleared. One new mismatch in minute labels (topic 05) stays open as a minor. It does not block.

### Gates I ran myself

- `python -m pipeline.build` (LOO_TODAY=2026-11-21): 0 errors, 0 warnings.
- `ruff check .`: all checks passed.
- `pytest -q`: all tests pass (98).
- The default Python 3.13 on this machine is missing the `Markdown` package, so the build and 4 test modules fail
  to import with it as is. I ran the gates with Markdown 3.6 added through `PYTHONPATH` (this meets the
  project's `Markdown>=3.5`). This is an environment gap, not a project defect. The producer should reinstall the
  project dependencies before the push.
- Nothing is committed for this brief. HEAD is still `0fcc3da`.

### The eleven items

| # | Item | Ruling | Evidence |
|---|------|--------|----------|
| 1 | Topic 09 "Asepalvelus" | Fixed | Unchanged since the first ruling. The only "varusmies" left in content is the gloss in topic 14 (lines 95, 113) |
| 2 | One action per step, at most five steps (03-06, 18) | **Fixed** | 06 T1: step 2 makes the table, step 3 marks it, five steps. 18 T2 step 5 asks for one skill. The goal line, the HOPS rows of the 75, 60 and 45 plans (lines 245, 257, 268) and the outcome (lines 80, 207) agree. 03 T3 step 5 names one thing. 05 T2: one action per step |
| 3 | 18 at 45 min vs the HOPS row; 13 names the task | Fixed | The 18 cut column says steps 3 and 4 of Task 2 go home. Step 5 stays in the HOPS row, and the goal line agrees. The topic 13 line is unchanged |
| 4 | Print one length | Fixed | Carried from the first ruling. The code is unchanged and the print tests pass |
| 5 | Headings "Tuntisuunnitelma (N min)" | Fixed | Carried. Tests pass |
| 6 | View links, current view marked | Fixed | Carried. Tests pass |
| 7 | `/polku/` without JS | Fixed | Carried. Tests pass |
| 8 | Dates d.m.yyyy | Fixed | Carried. Tests pass |
| 9 | `il-op2-17` | Fixed | Carried from the first ruling. Not re-opened |
| 10 | `il-op2` | Fixed | Carried. Not re-opened |
| 11 | Routes diagram caption | Fixed | Carried. Not re-opened |

### The first remaining list

- **Topic 18 line 105 and the glossary:** cleared. The student text and the Alex case use "asepalvelus tai
  siviilipalvelus". The style-guide glossary row and section 7 use the same form, and the row names
  varusmiespalvelus only as a gloss.
- **Topic 03 Task 3 step 5:** cleared. It asks for one thing to practise. "Joka auttoi" moved to the note.
- **Topic 05 Task 2:** cleared. The privacy note sits in step 3, next to the Työmarkkinatori page. The section
  opening ("Muistio on sinun omasi") still stands. "Ilman laitetta" names only step 3 as needing a device.
- **One-length print is 7 pages, not 4-5:** still open (sources and the curriculum box print with every length).
- **"Jos ehdit" paragraphs are not numbered:** still open. Three outcomes now lean partly on optional text, and
  the section prose covers each: 04 "kuvata mitä hyvinvointi tarkoittaa", 06 "miten HOPSia päivitetään", and 18
  "millä ehdoilla oikeus ohjaukseen jatkuu".
- **Routes diagram margin; no real print-dialog test:** still open, as before.

### The checker's must-fix: ruled a minor

The checker found that topic 05 Task 2 now reads "vaiheet 1, 2, 4 ja 5 noin 10 min, vaihe 3 noin 5 min". The
60-minute and 45-minute Työskentely rows still label those steps as 8 and 7 minutes, so the 60-minute row adds to 23
of its 25. **Upheld as a fact.** I rule it a minor and not a reject, for three reasons. The rows add up, and the build
checks them. The text a student sees is consistent. A shorter lesson that compresses a step is a normal counsellor
choice, and topic 18 at 45 minutes has the same pattern (9 min for 3 + 3), which was already non-blocking. Fix it in
the next content touch. One way: set the 60-minute label to "(10 min)" so the row reads 15 + 10 = 25, and give the
45-minute label "(7 min, tiiviisti)".

### Remaining minors

1. Topic 05 Task 2: the minute labels in the 60 and 45 min rows (8 and 7) do not match the header (10).
2. Topic 18 at 45 min: "vaiheet 1 ja 2 ... (9 min)" for two 3-minute steps (from HEAD, not new).
3. Topic 13: Task 1 step 1 and Task 2 steps 4-5 still bundle actions. They are outside the item 2 scope.
4. Topic 06 Task 2: the "Jos ehdit" paragraph chains three optional actions in one sentence.
5. One-length print is 7 pages: sources and the curriculum box print with every length.
6. Several outcomes lean partly on unnumbered "Jos ehdit" text (04, 06, 18).
7. Routes diagram caption margin; no real print-dialog test.
8. The local Python is missing `Markdown`. Reinstall the dependencies before the push.
9. `docs/known-issues.md` is updated by the producer after acceptance and push.

### For the operator

1. All eleven fixes are now done. The two task texts that pointed at missing steps are corrected.
2. One small mismatch in minute labels is left in one lesson plan. It does not affect students and can wait.
3. The build, the style check and the tests pass. The work is ready for the producer to commit and publish.
