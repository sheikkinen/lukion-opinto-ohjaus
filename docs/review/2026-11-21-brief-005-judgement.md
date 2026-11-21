# Judgement: brief 005, polish and pre-publish scan

Judge on Opus, outside the authors. Ruled from files only: `prompts/005-polish-and-publish.md` (with the addendum),
`CLAUDE.md`, `decisions/INDEX.md`, `docs/known-issues.md`, the changed content and data, the two remade pictures
(opened), `templates/base.html`, the scanned files and `tmp/shots-polish/` (20 PNGs). 2026-11-21.

## Verdicts

- **Polish: accept with minors.** Every brief 004 item and the brief 003 addendum items are done in the files. The
  one missing polish item is the footer licence line (step 1 of the work), which is a one-line template fix.
- **Publishing readiness: reject for now.** Two things block the next push: the footer licence line, and the
  local paths still in the working tree. Both are small. History rewrite is **not** required; see below.

## What I checked myself

- Build into a scratch directory: `build: 0 errors, 0 warnings`, exit 0. The built front page has "CC BY" twice in
  the body; the built `footer.site-footer` has no licence text (matches `templates/base.html` lines 26-33).
- `python -m pytest -q`: 87 passed. `ruff check .`: all checks passed. Largest Python file 401 lines (< 500).
- `data/images.run.yaml` sum of `dollars`: **$0.471** (brief said $0.37 before; the two remakes added $0.067 and
  the run log adds up). Far under the €10 of D-007.
- `dg-opintojen-rakenne.webp`: the 11 labels read exactly as `expected_labels`; no "syventävät ja soveltavat";
  the three cards match topic 01 lines 89-90 ("Valtakunnalliset valinnaiset opinnot", "Koulukohtaiset opinnot").
- `il-op2-12-tyoelama-ja-ennakointi.webp`: one continuous makerspace, three people (bicycle on a stand, seedlings
  under a grow lamp, chair sketch beside a small wooden chair), no laptop, no screen, no text. Matches the addendum.
- `front-500.png`: renders, no sideways scroll, licence is lower on the page (not in the viewport).
- `git grep -F 'C:\'`: confirms the paths the scanners list (four workflow `ROOT` defaults, `images.js` 21/40,
  `build-site.js` 42/66, `tools/images.py:34`, `scouting.json:729,740`, `prompts/003:46`).
- **Git state:** `origin/main` = `HEAD` (52e6176). D-010 [O] says the operator chose to "Publish now" the committed
  version for inspection. So the repository is **already public**, and the brief's "nothing has been pushed yet"
  no longer holds. This decides the history question.
- **Not in any report:** `pipeline/build.py` (sitemap call) is modified and `pipeline/sitemap.py` and
  `tests/test_sitemap.py` are untracked. They build and test clean. Whoever wrote them should say so in the diary,
  and they must be added by explicit path or they will be left out of the commit.

## Ruling on the open items

| # | Check | Item | Real? | Blocks push? | History rewrite? |
|---|---|---|---|---|---|
| 1 | browse | Footer has no CC BY 4.0 line / credit | Yes, confirmed in `templates/base.html` and the build | **Yes** (brief step 1 and done-when) | n/a |
| 2 | secrets | `tools/images.py:34` default `C:\src\game-engine` + docstrings naming game-engine `.env`, pimage | Yes. Path: real breach of "never commit a local path". Docstrings: private detail, no secret | **Yes for the path** (make it env-only, no default). Docstrings: no | No |
| 3 | secrets | `ROOT = 'C:\\src\\lukion-opinto-ohjaus'` in four workflows; Chrome and game-engine paths in `images.js`, `build-site.js` | Yes | **Yes** (default to the script's own dir or require `args.root`; "Chrome on PATH" in prompts) | No |
| 4 | secrets | `scouting.json:729,740` local CLAUDE.md path | Yes; harmless content, still a local path | **Yes** (replace with `CLAUDE.md`); keep the JSON public, it holds no private names | No |
| 5 | secrets | `prompts/003` path `C:\src\game-engine\tools\pimage` and pimage internals; 005 and D-009 prose | Path real (line 46). Internals real but no secret | **Path: yes**, by addendum note, not by editing the brief (rule 1). Internals: no, operator's call | No |
| 6 | secrets | Machine details: drive E:, pid 44964, port 8199, `hosts/<machine>.yaml` | Real, trivial; no host name or user | No. Generalize when convenient | No |
| 7 | private | Brief 003 describes pimage module inventory, GPU lock, ComfyUI | Real | No. Briefs are never edited; an addendum can say "game-engine details superseded". Already disclosed in `known-issues.md` as "your call" | No |
| 8 | private | `images.js` lines 21, 28, 35 expose game-engine layout | Real; the path part is item 3 | Path: yes (item 3). Layout prose: no | No |
| 9 | private | `tools/images.py` path + pimage internals; `pipeline/images.py:30` klein comment | Same as item 2 | Path: yes (item 2). Comments: no | No |
| 10 | private | Workflow local paths | Duplicate of item 3 | (item 3) | No |
| 11 | private | Scouting JSON local path | Duplicate of item 4 | (item 4) | No |
| 12 | private | Review notes and diary: pid, port, E:, klein job files, D-009 | Real, trivial; same as item 6 | No | No |

## Items that block the push

1. Add a CC BY 4.0 line with the `LICENSE` credit to the footer in `templates/base.html`, e.g. "Sisältö: CC BY 4.0,
   Lukion opinto-ohjaus" linking to the licence. Rebuild, 0 errors.
2. Remove every local absolute path from the working tree: the four workflow `ROOT` defaults, the Chrome and
   game-engine paths in `images.js` and `build-site.js`, the `C:\src\game-engine` default in `tools/images.py`
   (env var `GAME_ENGINE_DIR` only, clear error when unset), the two `scouting.json` entries. For
   `prompts/003:46`, add an addendum to brief 003 stating the path is now a placeholder, or accept it as history
   (operator's call; the brief text itself is not edited).
3. Re-run `git grep -F 'C:\'` and get no hits outside brief 003; build 0/0; pytest; ruff.

Not blocking, do in the same commit if cheap: replace "pid 44964 / port 8199 / drive E:" with "a stray local image
server" and "the local disk was full" in the brief 003 judgement, the diary, `pipeline/images.py:29` and the
illustrations YAML header.

## History rewrite

**Not required.** Nothing secret was found in any of the 15 commits: no keys, tokens, `.env` content or personal
e-mail; authors use the GitHub noreply address. What history holds is local directory names and game-engine
prose, and that history is already public on GitHub since D-010. A rewrite would need a force-push and could not
recall clones, forks or caches, so it would remove little and break the commit links in the decisions and diary.
The brief expected a rewrite only on the premise "nothing has been pushed yet", which D-010 superseded. If the
operator still wants the old commits gone, that is the operator's decision (O), done as a separate step after this
push, with the force-push stated plainly. The brief's done-when "scan clean across the whole history" should be
read as "no secrets across the whole history, no local paths in the tree"; record that as an addendum.

## Minors carried forward (none block)

- Legal references were not read against Finlex (script-rendered): 714/2018 §§ 25, 26, 28; 810/2018 (no section
  number in `law`); 502/2019 §§ 10, 11 behind the hedged äidinkieli exception in 07 and 10. A person opens them once.
- Some new task steps hold two or three actions (03, 04, 05, 06, 18), against one action per step.
- 18 at 45 min: "Tehtävä 2 kotiin" against a HOPS row that keeps Tehtävä 2 step 5; 13 "Vaiheet 4–5 kotiin" does not
  name the task.
- 09 line 103 still says "Varusmiespalvelus…" while 14 and the diagram say "Asepalvelus"; 14 defines it.
- `il-op2-17` stray lamp and empty top half; `il-op2` pleated skirts (operator's look call); il-op2-12 is crisper
  than the p-image set but in palette.
- `images.run.yaml` keeps the old syventävät prompts; it is an append-only log, leave it.
- CLAUDE.md, the producer brief template and prompts/005 name world-today and world-literature; fine if those are
  public, otherwise reword.
- Stray files `tmp/shots-polish$n-*.png` and `tmp/shots-live$…`: gitignored, delete by hand.
- Unreported sitemap work (`pipeline/sitemap.py`, `tests/test_sitemap.py`, `pipeline/build.py`): passes; diary it
  and commit by path.

## For the operator

1. The fixes from the review are in and the site builds clean; the new diagram and the workshop picture are right.
2. Two small things must be fixed before the next push: the licence line in the footer, and some folder paths
   from this computer that are written into scripts and notes.
3. No passwords, keys or private e-mail are anywhere in the project or its history.
4. The repository is already public, so rewriting its history is not needed and would gain little; say if you
   still want it.
5. Images have cost $0.47 of the €10 budget; one person should check the four law references once on Finlex.
