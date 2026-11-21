# Known issues: checklist for manual inspection

State after brief 007 (2026-11-21). Sources: the judgements in `docs/review/` and the live check of the deployed
site. Tick an item when you have looked at it on the site.

## Fixed in brief 005 (check that the fix reads well)

- [ ] Topic 01: the national optional studies are no longer split into "syventävät ja soveltavat"; the diagram
  `dg-opintojen-rakenne` was remade with the curriculum's own categories.
- [ ] Topic 02: "oikeus oppimisen tukeen" (Lukiolaki § 28).
- [ ] Topics 07 and 10: the äidinkieli exception and "poikkeuksista katso YTL" (worded generally; see facts below).
- [ ] Offline alternatives in all topics work with paper only (copy the case first, or invent one).
- [ ] Topics 13, 14, 15, 18: the goal, the plan rows and the task steps agree; topic 18's 45-minute HOPS row is
  9 minutes.
- [ ] Topics 03–06 and 18: every outcome has a task step.
- [ ] Topic 14 uses "Asepalvelus tai siviilipalvelus", as the routes diagram does.
- [ ] Working-life picture (`/op2/12-tyoelama-ja-ennakointi/`): one makerspace scene.
- [ ] The CC BY 4.0 credit is on the front page and in the footer of every page, with the note that curriculum text
  belongs to Opetushallitus.
- [ ] The "Avaa kuva suurempana" line no longer prints on paper.

## Fixed in brief 007 (check that the fix reads well)

- [ ] Print one lesson length: "Tulosta 75 min / 60 min / 45 min / kaikki pituudet" above each lesson plan.
- [ ] Headings "Tuntisuunnitelma (75 min)", "(60 min)", "(45 min)".
- [ ] The view links sit in the same place in both views and mark the current view.
- [ ] `/polku/` shows no dead buttons without JavaScript.
- [ ] Dates read d.m.yyyy everywhere.
- [ ] Topics 09 and 18 say "asepalvelus tai siviilipalvelus"; task steps in 03–06 and 18 hold one action each; topics
  13 and 18 say which task's steps go home.
- [ ] Pictures remade: money and housing (one full room), the OP2 page (casual clothes), the routes diagram (space
  under the caption).

## Still open

- [ ] **Topic 05, Task 2:** the 60- and 45-minute plan rows label steps 1, 2, 4 and 5 as 8 and 7 minutes, while the task
  says about 10. **Topic 18, 45 min:** "vaiheet 1 ja 2 (9 min)" for two 3-minute steps.
- [ ] **One-length print** of topic 18 is 7 pages; the last two are sources and the curriculum box.
- [ ] **Routes diagram:** the gap under the caption is smaller than the caption itself.
- [ ] **OP2 page picture:** two students wear plain skirts (not uniforms). Your call.
- [ ] **Topic 13:** a few task steps still bundle two actions.
- [ ] **Outcomes resting on optional text:** in topics 04, 06 and 18 an outcome is practised only in a "Jos ehdit"
  note.

## Not yet seen by a person

- [ ] A printed lesson plan on paper. The agents checked the PDFs as text and print-emulated screenshots, not as
  paper.
- [ ] The Finnish as a whole: read two topics as a student and two lesson plans as a counsellor.
- [ ] The self-study path: tick, write a note, reload, clear.
- [ ] All 21 illustrations and 7 diagrams together.

## Facts a person should confirm once

- [ ] Finlex: Lukiolaki 714/2018 §§ 25, 26, 28; asetus 810/2018 (S/H); Laki ylioppilastutkinnosta 502/2019 §§ 10,
  11, behind the äidinkieli exception in topics 07 and 10.
- [ ] Siviilipalvelus is backed only by intti.fi.
- [ ] The external links (51): the agents' sandbox could not reach outside hosts in the live check. Vipunen,
  Ammattinetti, Euroguidance and Studyinfo were unreachable earlier too.
- [ ] aoe.fi could not be searched, so "no open lesson set exists" is likely, not proven.

## Publishing

- [ ] The site is public, without `noindex`, and has a sitemap, so search engines may list it.
- [ ] The repository describes how game-engine's image modules (pimage) were used, in brief 003, the image workflow
  and `tools/images.py`. There are no secrets or local paths. Your call whether to trim it.
- [ ] Old commits still hold the local paths that brief 005 removed from the current files. No secrets were found in
  any commit. Rewriting the public history is your call.
