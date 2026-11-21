# Brief 008 judgement: shared engine (subject.yaml, then lukio-runko)

Judge (Opus), 2026-11-21. I wrote nothing that I judge. I ruled only on the internal Done-when of
`prompts/008-shared-engine.md`: the golden check passes, both test suites pass, the numeric test subject builds.
I ran each of them myself; nothing below is taken from the producer's or the checkers' reports alone.

## Verdict: accept with minors. Two small fixes before the engine repository is made public

The engine works and the opinto-ohjaus output is byte-identical. The fixes are in `lukio-runko` only and do not touch
the site output, apart from re-running the golden check after the first one.

## What I ran

| Done-when item | How I checked it | Result |
|---|---|---|
| Golden check | Built opinto-ohjaus with the installed engine (`python -m lukio_runko build`, `LOO_TODAY=2026-11-21`) into a scratch folder, then `lukio_runko compare tmp/golden <out>` and a separate `diff -rq` | Build 0 errors, 0 warnings. 80 files in golden, 0 differences. `diff -rq` printed nothing |
| Engine is the new folder | `import lukio_runko` resolves to `lukio-runko/src/lukio_runko` (editable install) | Pass |
| Engine tests | `pytest` in `lukio-runko` | 121 passed (about 40 s). `ruff check` clean, `ruff format --check` clean (41 files) |
| Subject tests | `pytest` in opinto-ohjaus | 2 passed. `ruff check` clean |
| Numeric test subject | Two topics with `assessment: numeric`, written with the engine's test helpers into a scratch root, built through the CLI (`python -m lukio_runko build --root ...`) | Complete subject: 0 errors, exit 0, page has `koetehtavat` and `mallivastaukset` sections. Without model answers: `error: missing section '## Mallivastaukset'`, exit 1 |
| Line limit | `wc -l` over the package | Longest file `checks.py`, 393 lines |
| Local paths, keys, e-mails | grep of both folders' changed and new files | None. Only the public GitHub and site addresses |
| Engine code left in the site | `git status` in opinto-ohjaus | `pipeline/`, `templates/`, `tools/`, `site-src/css`, `site-src/js` and the engine tests are deleted; `site-src/img` stays |
| Pages workflow | `pages.yml`, `requirements.txt` | Installs `lukio-runko @ git+https://github.com/sheikkinen/lukio-runko@v0.1.0`, runs `lukio-runko build` |
| Nothing committed | `git status`; `lukio-runko` has no git repository yet | Pass |

Two warnings on the numeric build are about the short `Opiskelijalle` text in the test fixture. They are expected.

## The engine checker's must-fix items, ruled

1. **`hops_part` in the engine (upheld, minor, fix before the tag).** `checks.py` lines 98-101 accept only the three
   opinto-ohjaus HOPS parts, and `views_topic.py` lines 160-161 print the row `HOPS-osa`. A topic without the field
   is not affected, so terveystieto can build. But it is an opinto-ohjaus idea inside a shared engine. Move the
   allowed values and the row label into `subject.yaml` (for example an optional `topic_fields` entry). With no entry
   the engine skips the check. Then run the golden check again: the `HOPS-osa` rows must stay byte-identical.
2. **LICENSE (upheld, blocks the public push).** `lukio-runko/LICENSE` is the opinto-ohjaus file. It has the title
   "Lukion opinto-ohjaus" and an attribution line pointing at the opinto-ohjaus site. `pyproject.toml` uses it as
   the package licence, so it goes into the wheel. A public engine repository must not present itself as the
   opinto-ohjaus site. It needs its own title and attribution. The brief's default is CC BY 4.0, and the brief
   names MIT as the operator's alternative for code. Until the operator answers, keep CC BY 4.0 and only correct
   the title and attribution.
3. **Workflow templates name opinto-ohjaus (not upheld as a fix).** The README says to copy and adapt them. Fine
   for 0.1.0.

## Producer's open question

"The role label for lesson tables" read as the column header `teacher.role_column: Ohjaajan rooli`, plus
`teacher.label`. **Accepted.** It is a reasonable reading, it is all configuration, and a missing column only gives a
warning. Terveystieto sets its own values.

## What blocks creating the public lukio-runko repository and pushing

1. Fix the LICENSE title and attribution (must-fix 2).
2. Fix `hops_part` (must-fix 1), then run the engine tests and the golden check again. Both must still show 121+
   passed and 80 files, 0 differences.
3. Order: create `sheikkinen/lukio-runko`, push, tag `v0.1.0`, and only then push opinto-ohjaus. If opinto-ohjaus
   is pushed first, its Pages build cannot install the pinned tag and fails. The live site then keeps the old build,
   but nothing new deploys.
4. Before pushing opinto-ohjaus, commit the deletions and new files by explicit path (`requirements.txt`,
   `subject.yaml`, `tests/test_site.py`). Keep `tmp/golden` out of the commit.
5. After the push, check that the Pages run is green and that the live front page and one lesson page match
   `tmp/golden`. This proves the brief's "the operator sees the site exactly as before".

No `.gitattributes` change: the golden check depends on the stored LF files.

## Remaining minors (not blocking)

1. `.claude/workflows/*.js` in opinto-ohjaus duplicate the engine's `workflows/` and still mention `pipeline/`. They
   are historical records; leave them, or note it in an addendum.
2. The `lukio-runko` console script is not on this machine's PATH. Use `python -m lukio_runko`. CI is unaffected.
3. Two committed files from earlier briefs (`docs/review/2026-11-21-brief-005-judgement.md`,
   `prompts/003-images-and-diagrams.md`) contain an old local path. They are unchanged here and covered by an
   earlier addendum.
4. Three `python -m http.server 8000` processes are listening on this machine. They were started on 15-16 November,
   before this brief, so they are not from brief 008. I did not stop them. The operator can close them.
5. The test fixture `subject.yaml` in the engine uses the opinto-ohjaus name and address. That is acceptable for a
   fixture.

## For the operator

1. The shared engine works: the opinto-ohjaus site builds exactly the same, file for file.
2. Two small fixes come first: the engine's licence file still carries the opinto-ohjaus name, and one opinto-ohjaus field has to move out of the engine.
3. Your call: keep the engine under CC BY 4.0 like the site, or use MIT, the usual licence for code.
4. After the fixes, the producer publishes the engine first, then the site, and checks that the live site has not changed.
