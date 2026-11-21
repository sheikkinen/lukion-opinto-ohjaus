# Known issues: checklist for manual inspection

State after brief 005 (2026-11-21). Sources: the judgements in `docs/review/` and the live check of the deployed
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

## Still open

- [ ] **Topic 09** still says "Varusmiespalvelus"; topic 14 and the diagram say "Asepalvelus".
- [ ] **New task steps** in topics 03–06 and 18 bundle several actions into one step; the style guide asks for one.
- [ ] **Topic 18 at 45 min:** "Tehtävä 2 kotiin" conflicts with the HOPS row, which keeps step 5 of Task 2.
  **Topic 13:** "Vaiheet 4–5 kotiin" does not say which task.
- [ ] **Money and housing** picture (`/op2/17-talous-ja-asuminen/`): a stray lamp shape and an empty top half.
- [ ] **OP2 page** picture: pleated skirts that could read as school uniforms. Your call.
- [ ] **Routes diagram:** its caption sits close to the bottom edge.
- [ ] **Print:** a lesson plan prints all three lengths (75, 60, 45) one after another, about 13 pages. One length
  per print would suit a counsellor better.
- [ ] **Headings:** "Tuntisuunnitelma (75 min)" is followed by bare "60 min" and "45 min".
- [ ] **Lesson view:** the "Opiskelijan näkymä" and "Tuntisuunnitelma" links do not mark the current view, and they
  sit in a different place in each view.
- [ ] **Without JavaScript,** `/polku/` still shows its counter and its print and clear buttons, which do nothing.
- [ ] **Dates:** `/opetussuunnitelma/` mixes "21.11.2026" and "2026-05-22".

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
