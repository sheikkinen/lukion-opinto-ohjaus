# 004: Make every lesson realistic, safe and stand-alone: the open teaching and curriculum items

**Written before the work.** Producer's brief, 2026-11-21. Run by `.claude/workflows/fix-content.js`, in parallel
with brief 003, on separate files.

## Why

Brief 002 was accepted with minors. The final recheck left 12 must-fix items (10 on teaching, 2 on the curriculum),
and the judge listed 10 more, all in `docs/review/2026-11-21-brief-002-open-items.json` [A]. The operator asked for
"stand-alone lessons - or as a self learning path" [O]. Plans that do not fit 45 minutes, offline tasks that need a
counsellor's printer, and HOPS prompts that could disclose a support need break that promise.

**Serves:** G-1. **Goal type:** technical (the checkers decide) and look (the voice stays as topic 07 set it).
**Chain:** brief 4 on G-1. **Models:** four content fixers on Sonnet (one per topic group, as the writers were split),
checkers on Sonnet, judge on Opus.

## Expected result, written before the work [M]

- The 45-minute plans drop the group phase and keep the task that delivers the lesson's goal. The 60-minute plans
  trim; task times vary with the task, not a fixed 15/10/10.
- Every offline alternative works for a student alone with paper and pen.
- HOPS prompts say what belongs in the HOPS (shared with the school) and what stays in one's own notes.
- Year placement reads as an example everywhere.
- Some new findings appear in the recheck. They are named in the judgement rather than chasing a third round.

## The work

1. Four fixers, each owning its topic files (01–06; 07–09 and 10–12; 13–15; 16–18), plus `content/pages/` and
   `data/yearly-facts.yaml` for the fourth. Each applies every open item that touches its files, and the
   cross-cutting rules everywhere in its files:
   - lesson tables realistic for 75, 60 and 45 minutes;
   - the goal task kept in every variant;
   - task times fitted to the work;
   - an offline alternative a student can do alone;
   - the HOPS privacy line;
   - year placement as an example;
   - the gender-aware assumption check;
   - open-question banks phrased so no one must disclose;
   - a fallback for students without last year's plan;
   - outcomes practised by tasks.

   The front page's licence text says CC BY 4.0 (D-008).
2. Rebuild. Checks by agents that wrote nothing: pedagogy and language, curriculum fidelity, facts and links.
3. One fix round on what the recheck finds, then the judge rules on the **final recheck's** open items (diary
   heuristic, brief 002).

## Limits

€0. Files: `content/` and `data/yearly-facts.yaml` only. Brief 003 owns `data/images.yaml`, `tools/`, `pipeline/`,
`templates/` and `site-src/`. Code minors (the S/H source, the table wrap and word break, the no-JS tick buttons) wait
for a later step.

## Done when

A counsellor can teach any topic in 45 minutes and reach its goal. A student alone can do every task, also without a
device. No task asks for anything that should not go into a shared HOPS. Internally: the pedagogy, curriculum and
facts checks have no must-fix item left, or each one left is named in the judgement, and the judge accepts.
