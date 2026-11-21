# Judgement: brief 003, images and diagrams

Judge: Opus, outside the authors. Date 2026-11-21. Ruled from the files only: `prompts/003-images-and-diagrams.md`,
`CLAUDE.md`, `data/images.yaml`, `data/images-illustrations.yaml`, `data/images.run.yaml`, `site-src/img/`, the
built `_site/`, the code, and the screenshots in `tmp/shots-images/`.

## Verdict: REJECT (not done yet)

The diagram half of the brief is done and good. The illustration half was never made: none of the 21 klein
illustrations exist, so the first sentence of the done-when ("a calm illustration at the top of every topic and on
the front and module pages") is not met, and the image checker has never seen an illustration. The cause is the
environment (drive E: full, where game-engine's klein writes its job files), not the code.

## What I ran and looked at myself

- `python -m pipeline.build`: exit 0, 0 errors, 21 warnings, every one `il-...: no picture file yet`.
- `ruff check .`: clean. `python -m pytest -q`: all pass.
- Opened all 7 diagrams in `site-src/img/`. Opened no illustrations, because there are none to open
  (`site-src/img/` holds only `dg-*.webp`; the manifest lists 21 `il-*` entries).
- Screenshots: `b-front-1366.png` (front page, no picture at all) and `t-yo-500.png` (topic 07 at phone width:
  diagram at the end of Opiskelijalle, with the "Avaa kaavio suurena" link).
- `_site/`: diagrams appear on op1/01, op1/06, op1/07, op2/14 and op2/15. No page shows an illustration.
- Longest data file 295 lines; all WebP files 38-68 KB.

## Done-when, line by line

| Done-when line | Ruling | Evidence |
|---|---|---|
| Calm illustration at the top of every topic (18) | FAIL | 0 of 18 files; build warns for each |
| Illustration on the front page | FAIL | `il-front` missing; `b-front-1366.png` shows text only |
| Illustration on the module pages (op1, op2) | FAIL | `il-op1`, `il-op2` missing |
| Diagram: matriculation exam | PASS | `dg-ylioppilastutkinto` on op1/07; labels exact; rule (5 tests, äidinkieli + 4 from 3 groups, one long syllabus, 3 sessions) correct |
| Diagram: HOPS | PASS | `dg-hops-kolme-osaa` on op1/06; three parts, labels exact |
| Diagram: timeline (marked as example) | PASS | `dg-ohjauksen-aikajana` on op1/01; "Esimerkki, koulu päättää" present; OP1/OP2 bands match suggested_timing |
| Diagram: routes, all equal | PASS | `dg-reitit-lukion-jalkeen` on op2/14; eight equal circles, equal-worth caption |
| Diagram: application step by step | PASS | `dg-haku-vaihe-vaiheelta` on op2/15; six steps, labels exact |
| Diagram: self-study loop | PASS | `dg-itseopiskelun-askel` on op1/01; Lue, Tee yksi tehtävä, Pohdi, Seuraava askel, clockwise |
| Every label spelled right and matches the text | PASS | I read all 7 myself; ä/ö correct, no extra text. The structure diagram now says "Valtakunnalliset valinnaiset opinnot" as op1-01 does |
| WebP, under 200 KB, lazy, width/height, alt | PASS | 38-68 KB; checked in `_site` and by the browse checker |
| No external requests | PASS | gates round 1 and 2 |
| Checks pass | FAIL | images recheck passed (diagrams only); browse recheck failed on the missing illustrations; gates pass |
| Spend recorded and under €10 | PASS | see below |
| Judge accepts | FAIL | this judgement |

## Spend

`data/images.run.yaml` holds 8 entries, all `google/nano-banana-2.1` at $0.0336:
7 first diagrams plus 1 remake of `dg-opintojen-rakenne`. **Total $0.2688**, well under the €10 cap (and under
the brief's expected $2). klein would be free. Note: one round-2 fixer report says $0.2352; that figure is stale,
the log total is $0.2688. No key, no local path in the log.

## Claims I checked and did not trust

- Build errors from round 0 are fixed: both moved diagrams are placed by topic op1-01. True.
- Manifest split under 500 lines: `images.yaml` 282, `images-illustrations.yaml` 295. True.
- The images checker's doubt about the matriculation rule: the diagram follows the current YTL structure
  (äidinkieli plus at least four tests from at least three groups, five in all). I find no fault.
- The round-2 images checker wrote "the manifest has no illustration entries". False: they are in
  `data/images-illustrations.yaml`; that checker only read `images.yaml`. It never checked illustrations either way.

## Remaining items

1. **Make the 21 illustrations** (owner: operator for disk space, then the script). Free space on E:, make sure no
   other job holds the GPU lock, then run `python tools/images.py --kind illustration`. Free; spends $0.
2. **Check the illustrations** with the image checker (no text, hands, faces, style, inclusiveness, school
   suitability), then a browse recheck of the front page, /op1/, /op2/ and the topic tops. Then judge again.
3. **Stray ComfyUI server** (pid 44964, port 8199) started by a round-2 run may still be running; the fixer's kill
   was denied. The operator or producer should stop it once nothing uses it.
4. Minor, code: `tools/images.py` with `--redo` and no `--only` also makes every missing picture; `--redo` should
   limit the run to the ids it names.
5. Minor, look: the timeline and loop diagrams were planned for the front page but sit on op1/01 (the build has no
   section placement on static pages). The loop diagram renders about 700 px wide on desktop; cap it (about 420 px).
   The routes caption touches the bottom edge of its image. Topic 14 says "Varusmiespalvelus" where the diagram
   says "Asepalvelus".
6. Do not commit until items 1-2 pass; the diagram work can be committed with the illustrations in one go.

## For the operator

- The seven Finnish diagrams are finished, correct and on the pages; they cost $0.27 of the €10.
- The pictures at the top of every page were never made: the E: drive is full, so the local image maker could not run.
- Please free some space on E: (a few hundred MB is enough) and say go; making them costs nothing.
- A leftover image server may still be running on port 8199; it can be stopped once the pictures are done.
- After the pictures are made and checked, I will judge again; nothing is committed until then.

## Re-judgement 2026-11-21

Judge: Opus, outside the authors. Ruled from the files only: the brief, `CLAUDE.md`, D-007 and D-009,
`data/images.yaml`, `data/images-illustrations.yaml`, `data/images.run.yaml`, `site-src/img/`, the built `_site/`,
the code, and `tmp/shots-images2/`.

### Verdict: ACCEPT WITH MINORS

All 21 illustrations now exist and sit on the front page, both module pages and all 18 topics. Three of the four
pictures the illustration checker failed are fixed. The fourth, `il-op2-12-tyoelama-ja-ennakointi`, no longer has
empty panels and now reads as a calm, finished picture of varied work. It still does not match its prompt or its alt,
but the page renders it with `alt=""` as decorative, so a reader never sees the mismatch. I rule that a minor fix,
not a blocker. The diagram fixes (width caps, lesson-view placement, link wording, `--redo`) are in place.

### What I ran and looked at myself

- `python -m pipeline.build`: 0 errors, 0 warnings. `ruff check .`: clean. `python -m pytest -q`: all pass. The two
  new tests `test_redo_alone_makes_only_the_named_ids` and `test_diagram_caps_and_lesson_placement` exist.
- Opened all 7 diagrams and 11 illustrations at full size: `il-front`, `il-op1`, `il-op2`, `il-op1-02`, `il-op1-03`,
  `il-op1-07`, `il-op2-11`, `il-op2-12`, `il-op2-14`, `il-op2-17`, `il-op2-18`.
- Built HTML: `picture-square` on `dg-itseopiskelun-askel` (CSS cap 520 px), `picture-compact` on
  `dg-ylioppilastutkinto` and `dg-reitit-lukion-jalkeen` (760 px). Lesson views (`/tunti/`) of op1/01, 06, 07 and
  op2/14, 15 carry their diagrams; `/tulosta/op1` and `/tulosta/op2` do too. "Avaa kuva suurempana" is on 12 pages;
  the old "Avaa kaavio" wording is gone from `_site/` and `pipeline/`.
- Every image's last run-log `sha256` matches the file in `site-src/img/`. All files 36-93 KB.
- The screenshots in `tmp/shots-images2/` were taken at 12:31-12:32; the remade pictures are from 12:35. So no
  screenshot shows the three remade pictures. The build proves they resolve; I judged them from the files.

### The four remade pictures

| Picture | Ruling | What I saw |
|---|---|---|
| `il-op1-03-ajankaytto` | PASS | Flat vector now, same style as the set. One student puts a note on a weekly wall grid, a second sits at a desk. No photoreal parts, no text. Alt was rewritten to match. |
| `il-op2-11-osaaminen` | PASS | One student with a sketchbook at a small table with a whistle, a wooden spoon, a heart badge and sneakers. No longer repeats `il-op1-02`. Robot kit missing, which does not matter. |
| `il-op2-14-koulutusvaylat` | PASS | School in the centre, five roads of equal width ending at a university, a workshop, a red folk high school, a hiker's trail and a harbour. No route dominates. This meets the equal-routes rule. |
| `il-op2-12-tyoelama-ja-ennakointi` | PASS, minor | No empty panels. Six scenes, not four: a cyclist riding (not repairing), a person on a video call, a pair at a laptop, two near-identical greenhouse scenes, a painter at an easel. Calm, no text, varied people. The alt still lists the four planned scenes; it should describe what is drawn. |

### Done-when, line by line

| Done-when line | Ruling | Evidence |
|---|---|---|
| Calm illustration at the top of every topic (18) | PASS | 18 of 18 files; build gives 0 warnings; style consistent after `il-op1-03` remake |
| Illustration on the front page | PASS | `il-front`: students on a birch-lined path, calm, no text |
| Illustration on the module pages (op1, op2) | PASS | `il-op1` (classroom, counsellor and students), `il-op2` (group looking out over a town) |
| Diagram: matriculation exam | PASS | `dg-ylioppilastutkinto` on op1/07, unchanged and correct; now capped at 760 px |
| Diagram: HOPS | PASS | `dg-hops-kolme-osaa` on op1/06, three parts, labels exact |
| Diagram: timeline (marked as example) | PASS | `dg-ohjauksen-aikajana`, "Esimerkki, koulu päättää" present |
| Diagram: routes, all equal | PASS | `dg-reitit-lukion-jalkeen` on op2/14; eight equal circles; caption still touches the bottom edge (minor) |
| Diagram: application step by step | PASS | `dg-haku-vaihe-vaiheelta` on op2/15, six steps |
| Diagram: self-study loop | PASS | `dg-itseopiskelun-askel`, clockwise, now capped at 520 px |
| Every label spelled right and matches the text | PASS, minor | All 7 diagrams read again; ä/ö correct. Open: topic 14 says "Varusmiespalvelus", the routes diagram says "Asepalvelus" |
| WebP, under 200 KB, lazy, width/height, alt | PASS | 36-93 KB; `loading="lazy"`, width and height set; diagrams carry Finnish alt, illustrations `alt=""` |
| No external requests | PASS | unchanged since the gates; no new external URL in the pages |
| Checks pass | PASS | build, ruff and pytest pass; the illustration checker's four must-fix items re-checked by me above; the browse check passed |
| Spend recorded and under €10 | PASS | see below |
| Judge accepts | PASS | this re-judgement, with minors |

### Spend

`data/images.run.yaml` has 35 entries: 8 × `google/nano-banana-2.1` at $0.0336 = $0.2688 (diagrams) and
27 × `prunaai/p-image` at $0.005 = $0.135 (21 illustrations plus 6 remakes). **Total $0.4038**, matching the fixer's
figure, and far under the €10 grant in D-007. The switch to p-image is recorded in D-009. No key or local path in
the log.

### Remaining

1. Minor, data: rewrite the alt of `il-op2-12-tyoelama-ja-ennakointi` to describe what is drawn (six work scenes:
   a cyclist, remote work, two people at a laptop, greenhouse work, painting). Free, edit in
   `data/images-illustrations.yaml`.
2. Minor, look (operator's call): `il-op2-12` has two near-identical greenhouse scenes and no repair scene. One more
   remake costs $0.005 if the operator wants it.
3. Minor, content: "Varusmiespalvelus" in topic 14 versus "Asepalvelus" in the routes diagram. Pick one word.
4. Minor, look: the routes diagram caption touches the bottom edge of the image; `il-op2-17` has a stray lamp-like
   shape and an empty top half; `il-op2` shows two pleated skirts that could read as uniform-like; topic 1 hall vs
   classroom alt wording. None blocks.
5. Minor, check: take fresh screenshots of op1/03, op2/11, op2/12 and op2/14; the current set predates the remakes.
6. Housekeeping: confirm nothing listens on port 8199 (pid 44964) before closing the brief.
7. Commit the diagram and illustration work together by explicit path, with the diary entry. Not done by me.

### For the operator

- Every page now has its calm picture, and the seven Finnish diagrams are correct and sized well.
- Three of the four weak pictures were redrawn and are good; the work-life picture is acceptable but not perfect.
- All images together cost about $0.40 of the €10 you allowed.
- A few small word and look fixes remain; none stops the site from going ahead.
- The work is ready to commit; it has not been committed yet.
