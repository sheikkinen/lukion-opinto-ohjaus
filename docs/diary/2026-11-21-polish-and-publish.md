# Brief 005: polish accepted; published before the last scan, by the operator's choice

**Date:** 2026-11-21 **IDs:** brief 005, D-010

## What happened

The operator asked to publish for inspection while brief 005 ran, so the repository went public with a known-issues
checklist after the producer's own scan of every commit (no secrets). Brief 005's polish was then accepted, but the
judge blocked the next push on the footer licence and local paths in workflow scripts and the image tool. The
producer fixed both, hid the "open larger" link in print (found by the live check), and added a sitemap on the
operator's request.

## Traps

- **Local paths in prompts are still local paths.** Workflow scripts carry prompts, and prompts carried folder names.

## Heuristic

Make workflow scripts take the project folder as a required argument, never as a default.

**Seed:** Should a pre-push hook grep for a drive letter and a user folder before every push?
