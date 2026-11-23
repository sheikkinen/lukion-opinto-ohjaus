# Content contract

**Written before the work.** Producer, 2026-11-21, for brief 002, from the critic's proposal in
`docs/research/2026-11-21-scouting.json`. A builder who needs a change adds a dated addendum at the end and says so.

## Data files

- `data/curriculum.yaml`: fetched from the ePerusteet API (peruste 6828810, OPH-2263-2019; oppiaine 6835370; OP1
  6835293; OP2 6835294) by `pipeline/fetch_curriculum.py`. It holds the exact Finnish wording, keyed by code:
  `OP1.t1`–`t9` and `OP1.s1`–`s8` (objectives and content of OP1, in ePerusteet order), `OP2.t1`–`t10` and
  `OP2.s1`–`s8`, `OP.yt1`–`yt11` (the subject's general aims), plus the module names, credits, assessment, the
  publication date and the date checked. Topic files never type curriculum text; the build resolves codes.
- `data/yearly-facts.yaml`: one entry per fact that changes yearly: `key`, `rule` (plain Finnish), `url`,
  `publisher`, `read` (YYYY-MM-DD). Keys include `ytl_exam_dates`, `ytl_enrolment_deadline`, `ytl_fees`,
  `joint_application_windows`, `admission_results_dates`, `places_and_quota`, `todistusvalinta_tables`,
  `cut_off_points`, `entrance_exam_dates`, `study_right_rule`, `kela_student_aid`, `intti_callups`, `civil_service`,
  `employment_services`, `learning_support_rules`, `guidance_services`, `curriculum_version`, `international`.

## A topic file

`content/topics/NN-slug.md`, Markdown with YAML front matter, written in Finnish.

Front matter (all required unless marked optional):
- `id`: `op1-07-ylioppilastutkinto`; `module`: `OP1` | `OP2`; `order`: 1–18, unique; `title`; `summary` (one
  sentence in plain Finnish).
- `curriculum`: a list of codes (e.g. `[OP1.t6, OP1.t7, OP1.s1, OP1.s8]`). Unknown codes fail the build.
- `law` (optional): e.g. `["Lukiolaki 714/2018 § 26"]`.
- `suggested_timing`: `{year: 1, term: kevät}`; the page always adds "esimerkki, koulu päättää".
- `role`: `core` | `extension`; `duration_options`: `[45, 60, 75]` (90 optional); `self_study_minutes`: e.g. 20.
- `prerequisites`: topic ids (may be empty); `hops_part` (optional): `opiskelusuunnitelma` |
  `ylioppilastutkintosuunnitelma` | `jatko-opinto- ja urasuunnitelma`.
- `official_links`: `[{title, url, publisher, read: YYYY-MM-DD}]`. Every link has a read date.
- `yearly_facts`: keys from `data/yearly-facts.yaml` the topic refers to.
- `school_adapts`: things the school sets itself (shown as "esimerkki").
- `materials`, `accessibility`, `last_reviewed`.

Body: fixed H2 headings, in this order, checked by the build:
1. `## Opiskelijalle`: 300–600 words of plain Finnish. It opens with "Osaan…" outcomes that mirror the cited
   objectives. Stable rules may be stated; every changing figure is a link.
2. `## Tehtävät`: 1–3 tasks, each with a title, time, materials, up to 5 numbered steps and an offline
   alternative. At least one uses a real official tool by a stable link. No model answers (OP is S/H).
3. `## Pohdinta`: 2–3 open prompts that never ask for personal data to be shared with the site, plus a short
   self-assessment against the "Osaan" outcomes.
4. `## Itseopiskelun askel`: the goal, a time estimate, read → do one task → reflect → next step, what to write into
   which HOPS part. The "Merkitse tehdyksi" tick is drawn by the site.
5. `## Tuntisuunnitelma (75 min)`: a table of phases (minutes, activity, counsellor's role, alternative, cut if short)
   that adds up to 75. Template: Virittäytyminen 5 / Aiemman tiedon aktivointi 10 / Lyhyt alustus ≤10 / Työskentely
   25 / Pari- tai pienryhmäpohdinta 10 / HOPS-askel ja exit 10 / Puskuri 5. Then `### 60 min` and `### 45 min`
   variants (and `### 90 min`, optional). Then preparation (up to 5 lines), an open-question bank, and ground rules:
   no forced disclosure, and an assumption check (gender-aware, non-segregating guidance).
6. `## Eriyttäminen`: an easier and a deeper path; S2 and plain-language support; reading, attention and anxiety
   adjustments; a no-device version; a link to learning support, not a restatement.
7. `## Milloin opinto-ohjaajalle`: concrete triggers, and help links with read dates.
8. `## Lähteet`: generated from the front matter (curriculum codes with exact wording, law, official links with read
   dates). Not written by hand.

## Build checks (fail the build)

- Unknown curriculum code; an objective or content area of OP1, OP2 or OP.yt not served by any topic.
- A missing or out-of-order section; a lesson table whose minutes do not add up to the stated length.
- A link without a read date, or a read date older than 12 months.
- A figure (a date, a euro amount or a percentage) next to a yearly fact, unless it is inside the link text.
- Any external resource in the output that is not a plain link (scripts, fonts, images, iframes from other hosts).

## Site structure

`/` front page (two doors: Opinto-ohjaajalle and Opiskelijalle, the module cards, "opetussuunnitelma tarkistettu
<date>", the licence); `/op1/`, `/op2/` module pages (official names, credits, S/H, the exact objectives and content
with a coverage matrix, and the topic list); `/op1/07-ylioppilastutkinto/` the student view and `…/tunti/` the
lesson view; `/polku/` the self-study path (progress and notes under one localStorage key `loo:v1`, written only on a
click, a "Tyhjennä tietoni" button, a warning about shared computers, a plain list without JavaScript);
`/tulosta/op1/` and `/tulosta/op2/` all lesson plans of a module for printing; `/opetussuunnitelma/`;
`/lahteet/` (all links with read dates, and the yearly-facts table); `/tietosuoja/`; `/saavutettavuus/`.

No external requests, self-hosted fonts or system fonts, reflow at 320 px, AA contrast in light and dark themes,
correct heading order, and every page readable without JavaScript.

## Addendum 2026-11-21 (pipeline and site builder)

Added by the builder of brief 002; nothing above was changed.

- `curriculum` in a topic may be a list of codes or a list of `{code, kind, eperusteet_id}` mappings. The build reads the code only.
- A topic's file name is `NN-slug.md`, its `id` must be `<module in lower case>-NN-slug` and its pages are written to `/<module>/NN-slug/` and `/<module>/NN-slug/tunti/`.
- `## Lähteet` is generated. A topic file may leave it out (preferred) or end with it; its text is ignored. The `Tuntisuunnitelma` heading must state the length, `## Tuntisuunnitelma (75 min)`; variants are `### 60 min`, `### 45 min`, `### 90 min`. Each plan is a table with a `Min` column; a row whose cells contain "Yhteensä" is not counted; a range such as `5-10` fails. Every length in `duration_options` needs a plan.
- Yearly figures: a date (`1.12.`, `5.6.2027`, `1. joulukuuta`), a year from 2025 on, a euro amount or a percentage outside a link in a topic's body fails the build when the topic lists `yearly_facts`, and is a warning when it does not. Link text, link addresses, code spans and the generated Lähteet are not scanned. An entry in `data/yearly-facts.yaml` may carry an optional `stable_figures: ["1.12.", "5.6."]` list of figures that are exempt for topics that cite that fact.
- An external Markdown link in a topic or page body must also appear in that file's `official_links` (which carries the read date), or in the `url` of a cited yearly fact.
- Static pages in `content/pages/*.md` take the same `official_links` front matter, which is shown on `/lahteet/`. Block tokens alone on a line (`{{doors}}`, `{{path_list}}` and others) are replaced by generated HTML; inline tokens are `{{curriculum_checked}}`, `{{curriculum_published}}` and `{{topic_count}}`.
- Warnings, not failures: `Opiskelijalle` outside 300-600 words, `Tehtävät` without 1-3 `###` tasks, a plan length not listed in `duration_options`.
- `python -m pipeline.build --partial` (development only) turns uncovered codes, missing `data/yearly-facts.yaml` and unknown prerequisites into warnings. CI runs the build without it. `LOO_TODAY=YYYY-MM-DD` sets the date used for the 12-month link age check.

## Addendum 2026-11-21 (brief 008, subject config)

Added by the generalizer of brief 008; nothing above was changed.

- Everything subject-specific now lives in `subject.yaml` at the repository root: the site name, short name (the
  prefix of `LOO_TODAY` and `LOO_SITE_URL`), base address, localStorage key and licence line; the teacher's labels
  and the lesson plan's role column; the ePerusteet peruste, oppiaine and module ids, the module codes and routes and
  the expected code counts; the highest `order`; the assessment type; and the H2 sections above, in order, with the
  view (student or lesson) that shows each. The pipeline and the templates read these only from there.
- `assessment: sh` (this site) keeps the sections above. `assessment: numeric` (a subject graded 4–10) adds
  `## Koetehtävät` and `## Mallivastaukset` after `## Tehtävät`, both on the student view. The build checks that
  every `###` exam task states its points (`### 1. Otsikko (6 p)`) and that `## Mallivastaukset` has one non-empty
  `###` answer per task, with the same heading and in the same order. In an `sh` subject those headings are unknown
  sections and fail the build.
- New warning: a lesson plan table without the `Ohjaajan rooli` column (`teacher.role_column`).
- `site-src` files may carry `@SITE_NAME@` and `@STORAGE_KEY@`; the build fills them in when it copies the assets.

## Addendum 2026-11-21 (brief 008, the engine moves out)

Added by the extractor of brief 008; nothing above was changed.

- The pipeline, the page template, the engine's scripts and stylesheets and the image tool are now the `lukio-runko`
  package, pinned in `requirements.txt`. Read `python -m pipeline.build` above as `lukio-runko build`,
  `python -m pipeline.fetch_curriculum` and `pipeline/fetch_curriculum.py` as `lukio-runko fetch-curriculum`, and
  `tools/images.py` as `lukio-runko images`. Each takes `--root` (default: the current folder).
- The engine's assets are copied to `_site/assets/` first and this repository's `site-src/` (the pictures, and any
  file that replaces an engine asset of the same path) over them. A `templates/base.html` here would replace the
  engine's template; there is none.

## Addendum 2026-11-22: the shared content guideline (lukio-runko v0.4.0)

This contract now extends the shared guideline in the engine, `docs/content-guideline.md` in sheikkinen/lukio-runko
(v0.4.0, pinned in requirements.txt). In short: every teaching claim, rule or model-answer criterion names its basis
(a curriculum code from the topic's list, a matriculation exam requirement, a cited source or an operator decision) or
is labelled as the site's own framing (*sivuston oma jäsennys*); value questions are written as weighing and model
answers accept any well-argued view; checkers and judges verify claims against their basis, not against this site's
style guide or earlier drafts; and the guideline's watch list of English habits applies. Where this contract and the
guideline differ, the guideline applies until this contract is amended.

## Addendum 2026-11-23: no help blocks or emergency lines

Added in round 2 of the basis audit; nothing above was changed.

- Operator rule, 2026-11-22: "remove the unrelated safety block - it is US cultural thing"; the shared guideline §4
  (US-style safety apparatus) and norm ledger rows 3 and 4 in lukio-runko. Decision: D-015.
- No topic carries a help or crisis block, a 112 line, an emergency-number sentence (*soita hätänumeroon*,
  *Hätätilanteessa…*), a crisis line or youth helpline as a help pointer, or a content note. The one help block
  allowed across the sites is in the terveystieto mental-health chapter, not here.
- `## Milloin opinto-ohjaajalle` stays: it is subject content (OP guidance). Read item 7 under "A topic file" as
  concrete triggers plus dated links to services that match them; "help links" there does not mean crisis lines.
- A source link that supports subject content stays in `official_links`; only its use as a help pointer goes.

## Addendum 2026-11-23: repeated notes are said once (lukio-runko v0.5.1)

Added in the repeat clean-up; nothing above was changed.

- Operator decision, 2026-11-23, answering "Decide on the repeated per-page notes now?": "Remove repeats". Norm
  ledger row 5 in lukio-runko: a site-wide fact is stated once on a site page; topic pages do not repeat it. The
  engine pin is v0.5.1, which no longer stamps the yearly-facts note or the self-study storage note on each topic.
- Said once, not on each topic: that cases and people are fictional, how the open questions are used, and that the
  tasks work on paper (front page); that reflections need not be shown to anyone, what to keep out of HOPS, the
  visual-novel note, opiskeluhuolto and Ohjaamo (`/polku/`); the right to learning support with the OPH links
  (`/opetussuunnitelma/`). Where the self-study mark is stored was already said on `/polku/` and the front page.
- Read item 6 under "A topic file" as: a support link only where the topic has a support point of its own; the
  generic learning-support link is on `/opetussuunnitelma/`. Read item 7 as: help links to services specific to the
  topic's triggers; the label is left out when none remains.
- `data/yearly-facts.yaml` no longer has `learning_support_rules`; read the key list in "Data files" without it.
  `guidance_services` is cited only by the topics whose subject it is (08, 15).
- Kept on purpose, as lesson design: the ground rules (*Pelisäännöt*), the lesson goals and the table steps that
  remind the group to talk about cases, not their own situations. The review is in
  `docs/review/2026-11-23-repeat-cleanup.md`.
