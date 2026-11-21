# 007: Clear the eleven open minor items

**Written before the work.** Producer's brief, 2026-11-21. Run as a workflow: content, code and image fixers in
parallel, then checks and a judge.

## Why

The operator [O]: "Yes, clear them", in answer to "Shall I clear the 11 open minors in one more brief?". The items
are under "Still open" in `docs/known-issues.md` [A].

**Serves:** G-1. **Goal type:** technical, with two look items. **Chain:** brief 6 on G-1 (after 001–005).
**Models:** content fixer Sonnet; code fixer Sonnet; art director Opus (up to three picture remakes, about $0.10,
within D-007); checkers Sonnet and Haiku; judge Opus.

## The items and who owns them

**Content fixer** (`content/`):
1. Topic 09 says "Varusmiespalvelus" where topic 14 and the diagram say "Asepalvelus". Align it.
2. New task steps in topics 03–06 and 18 bundle several actions. Split them into one action per step, still at most
   five steps per task (style guide).
3. Topic 18 at 45 minutes: "Tehtävä 2 kotiin" conflicts with the HOPS row, which keeps step 5 of Task 2. Topic 13:
   "Vaiheet 4–5 kotiin" does not name the task.

**Code fixer** (`pipeline/`, `templates/`, `site-src/` except `img/`, `tests/`):
4. Printing: a counsellor can print **one** lesson length (75, 60 or 45 minutes), not all three. Printing the
   whole view still works, without JavaScript.
5. Headings: "Tuntisuunnitelma (75 min)", "Tuntisuunnitelma (60 min)", "Tuntisuunnitelma (45 min)". Adjust the
   build check that reads them.
6. The lesson view and the student view: the two view links sit in the same place in both and mark the current view
   (`aria-current="page"` and a visible style).
7. `/polku/` without JavaScript: the counter, the print-notes and clear buttons are hidden like the tick buttons.
8. Dates: one format, `d.m.yyyy`, everywhere on the site, including `/opetussuunnitelma/`.

**Art director** (`data/images*.yaml`, remakes):
9. `il-op2-17` (money and housing): remove the stray lamp shape and fill the empty top half. One scene.
10. `il-op2` (the OP2 page): no pleated skirts or anything that reads as a uniform.
11. `dg-reitit-lukion-jalkeen`: the caption must not touch the bottom edge. Remake with a margin, with the same
    labels.

## Limits

€0 apart from the image remakes (at most $0.50). Nothing outside the listed files. The build, ruff and the tests
must pass.

## Done when

The operator finds every "Still open" item fixed on the site. A lesson plan prints one length of about 4–5 pages, the
headings match, the current view is marked, the path without JavaScript shows no dead buttons, dates read d.m.yyyy,
and the three pictures look right. Internally: the checks pass and the judge accepts. Then the producer pushes,
checks the live site and updates `docs/known-issues.md`.
