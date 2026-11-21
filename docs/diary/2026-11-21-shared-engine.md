# Brief 008: the shared engine, extracted and published

**Date:** 2026-11-21 **IDs:** brief 008, D-011

## What happened

A generalizer moved everything subject-specific into `subject.yaml` and proved it with a byte-for-byte golden
comparison (80 files, 0 differences). An extractor moved the engine into `lukio-runko` as an installable package with
a `lukio-runko build` command; the golden comparison held again. The judge accepted with minors: the engine's own
licence header, and one opinto-ohjaus field (HOPS) still hard-coded, which a fixer moved into `subject.yaml`. The
producer published `sheikkinen/lukio-runko` at tag v0.1.0 before pushing this site's switch, so the pinned install
resolves.

## Traps

- **Extraction deletes more than code.** The extractor removed this repository's brief and diary templates along with
  the engine's templates. They were restored.

## Heuristic

Prove a refactor of a published site with a byte-for-byte comparison against a copy built before the change.

**Seed:** Should the engine's CI build both subject sites and compare them with their published copies on every
engine change?
