# 002: Build the site: 18 full topics over OP1 and OP2, a lesson view and a self-study path

**Written before the work.** Producer's brief, 2026-11-21. Built by `.claude/workflows/build-site.js`.

## Why

The operator [O] as in brief 001, plus "site target language: Finnish" (D-006). Full lessons (D-002); workflows
(D-003).

**Serves:** G-1. **Goal type:** look (the operator's eye on the finished site decides the look and voice) with
technical parts (the build checks decide those). **Chain:** brief 2 on G-1.
**Models:** pipeline and site builder Sonnet; the sample topic and its style guide Opus (the voice every writer
follows); four topic writers Sonnet; checkers Sonnet (curriculum, facts, pedagogy and language, browse) and Haiku
(gates); fixers Sonnet; judge Opus.

What stands [A]: `docs/research/2026-11-21-research.md`, `docs/content-contract.md`, `CLAUDE.md`.

## Expected result, written before the work [M]

- 18 topics, each 2,000–3,500 words of Finnish across its sections, every curriculum code covered.
- The checks find fact and link problems first: links that move, and yearly figures typed into the text. The
  pedagogy checker finds uneven voice between writers, which is why one sample topic sets the voice first.
- Some official sites (Vipunen, Ammattinetti, Studyinfo) need a browser check, or are left out with a note.

## The work

1. **Foundation, in parallel:**
   - *Pipeline and site* (Sonnet): `pipeline/` (curriculum fetch from the ePerusteet API into
     `data/curriculum.yaml`; the Markdown build into `_site/`; all build checks in the contract), `templates/`,
     `site-src/` (CSS, a small progress script, print styles, fonts), the static pages (front, modules, curriculum,
     sources, privacy, accessibility), `tests/`, and `.github/workflows/pages.yml` (build and deploy on push).
   - *Sample topic and style guide* (Opus): topic 07 written in full to the contract, and `docs/style-guide.md`
     (voice, terms, a glossary of guidance terms, how tasks and lesson tables are written).
   - *Yearly facts* (Sonnet): `data/yearly-facts.yaml` and checks of the official URLs, in a browser if a fetch fails.
2. **Topics, in parallel,** each writer following the sample and the style guide: OP1 01–06 except 07 is done; OP1
   08–09 and OP2 10–12; OP2 13–15; OP2 16–18. Each writer owns its topic files.
3. **Build and integrate:** run the build, fix contract and join problems.
4. **Check, by agents that wrote nothing:** curriculum fidelity; facts and links (opened, read dates, no copied
   yearly figures); pedagogy and language (plain Finnish, a consistent voice, lesson minutes add up, inclusive and
   non-segregating, no requests for personal data); browsing (screenshots at desktop and phone width, without
   JavaScript, print view, localStorage only on click); gates (build checks, ruff, tests, line limits, no external
   requests).
5. **Fix and recheck,** at most two rounds: a content fixer (owns `content/`, `data/yearly-facts.yaml`) and a code
   fixer (owns `pipeline/`, `templates/`, `site-src/`, `tests/`), each taking the findings in its files.
6. **Judge** (Opus, files only) writes `docs/review/2026-11-21-brief-002-judgement.md`.
7. The producer commits by explicit path and writes the diary line. Publishing follows only after the operator
   chooses the content licence.

## Limits

€0. Nothing pushed. No text copied from textbooks or publishers; official texts linked and quoted at most briefly.
No personal names of private individuals in examples (use made-up first names only in task cases, clearly fictional).

## Done when

The operator opens the built site locally and finds both modules with nine topics each. Every topic opens as a
student page and as a counsellor's lesson plan for 75, 60 or 45 minutes. A student can walk the self-study path and
tick steps, which stay only on their own device. Lesson plans print cleanly. Every curriculum objective and content
area shows which topic covers it. Every changing fact is a dated link. Internally: the build checks pass, the
checkers' must-fix lists are empty or named in the judgement, and the judge accepts.
