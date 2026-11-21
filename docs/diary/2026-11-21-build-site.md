# Brief 002: the site built, accepted with minors

**Date:** 2026-11-21 **IDs:** brief 002

## What happened

`build-site.js` ran 25 agents: a pipeline builder, a lead writer who set the voice with topic 07 and the style guide,
a facts curator, four topic writers, an integrator, five checkers, two fix rounds split by file owner, and a judge.
The build passes with every curriculum code covered. The judge accepted with minors, while the pedagogy checker still
listed ten must-fix items after round 2: 45-minute plans that do not fit their time, offline alternatives that need a
printer, and HOPS prompts that could disclose a support need.

## Traps

- **The same fixed task times everywhere.** The writers copied the sample's 15/10/10 minutes into every topic.
- **The judge ruled on round 0, the checker on round 2.** The judge verified that the round-0 items were fixed and
  accepted, while the last recheck still had new items open.

## Heuristic

Give the judge the final recheck's open items as the list it must rule on, not the first round's.

**Seed:** Should the sample topic carry three different task lengths, so writers copy the reasoning and not the numbers?
