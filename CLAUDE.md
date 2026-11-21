# CLAUDE.md — lukion-opinto-ohjaus

A free, public website that works as a stand-alone backbone for upper secondary school guidance counselling (lukion
opinto-ohjaus) in Finland. It follows the national core curriculum for general upper secondary education (Lukion
opetussuunnitelman perusteet 2019, in force since 1 August 2021). The content is divided into topics. Each topic works
in two ways:
- as a **stand-alone lesson** a guidance counsellor (opinto-ohjaaja) can teach;
- as a step in a **self-study path** a student can follow alone.

The site is in Finnish and hosted on GitHub Pages. The process is reused from world-today and world-literature: briefs
written before the work, research by a fan-out plus a critic, a content contract before building, separate checkers,
and a judge outside the author.

## The one law

Normalize at the boundary. Every topic is written to the content contract (`docs/content-contract.md`), and its
curriculum references point to the exact objective and content area in the national core curriculum. Pages, the
lesson view, the self-study path and the checks read only that structure.

## Roles

- **Operator** (the human) decides scope, look, cost (over €5) and publishing. The operator is spoken to in plain
  words. Questions are asked only where no safe default exists, and the defaults are written into the brief.
- **Producer** (the long session) writes the briefs, runs the workflows and reports.
- **Builders, checkers, judge:** workflow agents. Builders own separate files. Checkers and the judge wrote nothing
  they check.

## Rules in force

1. **Written-before.** Every brief is committed before its work, with its goal type and done-when in the operator's
   terms. A research brief writes its expected answer first. A brief is never edited afterwards; changes go in an
   addendum.
2. **Decision grades:** `O` the operator's words, `A` a committed file or a page read, `M` model-only.
3. **Curriculum fidelity:** every topic names the curriculum objectives and content it serves, citing the core
   curriculum (ePerusteet) by module and section. Nothing is presented as required by the curriculum unless it is.
   School-specific practice (course trays, the school's own schedules, Wilma conventions) is marked as an example
   for the school to adapt.
4. **Facts with a source and a date:** admission rules, the matriculation examination, application dates, statistics
   and services link to their official source (Opetushallitus, Ylioppilastutkintolautakunta, Opintopolku, Vipunen,
   Työmarkkinatori and others) with the date they were read. Anything that changes yearly says so and links instead
   of copying figures.
5. **Judge outside the author.** Look questions end on the operator's answer.
6. **Diary after every brief,** with a `**Seed:**`.
7. **Code limits:** no file over 500 lines, ruff clean, fast unit tests with no network.

## Content rules

- **Students' privacy:** no accounts, no analytics, no forms that send data anywhere. Self-study progress and a
  student's own notes stay in the browser (localStorage) and can be cleared. Reflection tasks never ask the student
  to share personal information with the site.
- **Inclusive and neutral:** no stereotyping by gender, background or field. Every route counts equally: the
  university of applied sciences, the university, vocational education, a gap year, work and studying abroad.
  Support for students with learning difficulties, Finnish as a second language and wellbeing is shown with links to
  help.
- **Accessible:** WCAG 2.1 AA, readable on a phone, printable lesson plans, plain Finnish (selkeä yleiskieli).
- **Original text only.** Nothing is copied from textbooks or other publishers' materials. Official texts are
  linked and quoted briefly with their source.

## Standing limits for every agent

- **Money:** €0 metered.
- **Publishing:** the operator asked for a GitHub-hosted site (D-001). Pushing to the public repository and turning
  on Pages happens only after the judge's acceptance and the publishing check, and is reported.
- **Public hygiene:** never commit a key, a local path, a personal e-mail or personal names of private individuals.
  Commits use the GitHub noreply e-mail.
- **Models:** a script for building and fetching; Haiku for rule-based checks; Sonnet for research, writing and
  judgement checks; Opus for design and the judge.

## Conventions

Conventional Commits, commit by explicit path, messages through `tmp/msg.txt`. Content is Markdown with front
matter. A small Python build writes static HTML; no JavaScript is needed to read a lesson.
