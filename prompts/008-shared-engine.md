# 008: Make the site engine shared: a subject config, then its own repository, pinned by each subject site

**Written before the work.** Producer's brief, 2026-11-21. Runs after brief 007 is pushed.

## Why

The operator [O]: "planning for terveystieto - should this be a separate github pages? or are the tools etc pushing
for single site", then "Separate, shared engine" (D-011). Each subject gets its own GitHub Pages site; one engine
builds them all.

**Serves:** G-2 (and keeps G-1 running). **Goal type:** technical; the opinto-ohjaus output staying identical decides.
**Chain:** first brief on the engine. **Models:** generalizer Opus (design of the config); extractor Sonnet; checkers
Sonnet and Haiku; judge Opus. Creating the repository, tagging and pushing are done by the producer.

What stands [A]:
- About 23 subject-specific spots in 8 files: `pipeline/fetch_curriculum.py`, `views_site.py`, `layout.py`,
  `models.py`, `checks.py`, `build.py`, `sitemap.py`, and `templates/base.html` (OP's ePerusteet ids, `OP1`/`OP2`,
  S/H assessment, the site name and address).
- Terveystieto will be graded 4–10 and is a matriculation exam subject, so its topics need exam-style tasks with
  model answers, sections opinto-ohjaus does not have (brief 006 report).

## Defaults (the operator may override any)

- Engine repository: `sheikkinen/lukio-runko`, public, licence CC BY 4.0 like D-008 (Creative Commons does not
  recommend CC for code; MIT is the usual alternative, the operator's call).
- Versions as git tags (`v0.1.0` first); each subject site installs a pinned tag in its Pages workflow.
- The terveystieto site: `sheikkinen/lukion-terveystieto`, sheikkinen.github.io/lukion-terveystieto, set up by its
  own brief in its own repository.

## The work

1. **Subject config.** `subject.yaml` in this repository names everything subject-specific: the site's name, short
   name and address; the ePerusteet peruste, oppiaine and module ids and their codes; the assessment type (`sh` or
   `numeric`); the content-contract sections per assessment type (`numeric` adds `## Koetehtävät` and
   `## Mallivastaukset`, checked by the build); the licence line; the module routes. The pipeline reads only that.
2. **Golden check.** Before the change, build `_site` and keep a copy. After it, the new build is byte-identical,
   except for differences the generalizer lists and the checker accepts.
3. **Extract.** The engine (the pipeline, templates, site assets, the image tool, the workflow scripts as templates,
   tests) moves to a local `lukio-runko` folder beside this one, as an installable Python package with a `lukio-runko
   build` command. This repository keeps only its content, data, `subject.yaml` and docs, and installs the engine.
   The golden check runs again.
4. **Checks** by agents that wrote nothing: identical output, tests in both folders, no local paths, line limits, and
   a dry build of a two-topic test subject with `assessment: numeric` to prove the new sections work.
5. **Judge,** then the producer creates the public repository, tags `v0.1.0`, pins it in this site's Pages workflow,
   pushes both, and checks that the live opinto-ohjaus site is unchanged.

## Limits

€0. The live opinto-ohjaus site must not change visibly. No content changes in this brief.

## Done when

The operator sees the opinto-ohjaus site exactly as before, and a new public `lukio-runko` repository that a second
subject can use. Internally: the golden check passes, both test suites pass, the numeric test subject builds, and the
judge accepts.
