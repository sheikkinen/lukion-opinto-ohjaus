# Judgement: brief 002 (build the site)

**Judge:** Opus, outside the author. Files only. Date 2026-11-21. Nothing was edited except this file. Nothing was committed.

## Verdict: accept-with-minors

Every line of the brief's "Done when" is met. All five checkers' round-0 must-fix items were fixed, and I checked each fix
in the files. What is left is minor wording, plus one look question for the operator. The tables are clipped on a
narrow laptop and you have to scroll them sideways.

## What I ran and read

- `python -m pipeline.build`: `build: 0 errors, 0 warnings`. `ruff check pipeline tests`: all checks passed.
  `pytest -q`: 61 tests passed, no network. Largest code file is `pipeline/checks.py` (401 lines, the limit is 500).
- Read in full: `prompts/002-build-site.md`, `CLAUDE.md` and `docs/content-contract.md` with its addendum.
- Read the whole of these topics, one per writer group plus the sample:
  - 07 (sample)
  - 04 (OP1 01–06)
  - 10 (OP1 08–09 / OP2 10–12)
  - 13 (OP2 13–15)
  - 17 (OP2 16–18)
- Spot-read 01, 08, 11, 14, 15, 16 and 18 for the round-1 fixes.
- `_site/`: the module folders, lesson pages, print pages, path page, sources page and `site-src/js/polku.js`.
- Screenshots in `tmp/shots/`, the newest `v_*` set:
  - front page, 1366 px
  - path page, 500 px
  - curriculum page, full length at 1366 px
  - lesson 07, full length at 1366 and 500 px
  - print index for OP1, 1366 px

## Done when, line by line

| # | Done-when line (operator's terms) | Result | Evidence |
|---|---|---|---|
| 1 | The operator opens the built site locally and finds both modules with nine topics each. | pass | `_site/op1/` has 01–09 and `_site/op2/` has 10–18. The front page shows both module buttons (`v_front_1366.png`). |
| 2 | Every topic opens as a student page and as a lesson plan for 75, 60 or 45 minutes. | pass | All 18 topics have a `tunti/index.html` (9 + 9). Each lesson page has `Tuntisuunnitelma (75 min)`, `### 60 min` and `### 45 min`; topic 07 also has 90 min. The build checks that the minutes add up. In 04, 07 and 10 I added them by hand: 75, 60 and 45 each. |
| 3 | A student can walk the self-study path and tick steps, which stay only on their own device. | pass | `_site/polku/` has 18 `data-step-toggle` buttons. The controls are `hidden` until the script runs, so without JavaScript the page is a plain list. `polku.js` writes to localStorage (key `loo:v1`) only from click handlers: step toggle, note save, clear. It reads on load and never sends data. The shared-computer warning and "Tyhjennä tietoni" are visible (`v_polku_500.png`). |
| 4 | Lesson plans print cleanly. | pass, with a note | `/tulosta/op1/` and `/tulosta/op2/` each hold 9 `print-topic` blocks. `print.css` starts each lesson on a new page, undoes the stacked phone layout, repeats table headers and hides the navigation. The PDF (`tmp/shots/v_print_op1.pdf`) was checked by text only, so a person should still flip through one printout. |
| 5 | Every curriculum objective and content area shows which topic covers it. | pass | `/opetussuunnitelma/` lists each code with the official wording and its "Aiheet:" links (`v_opstall_1366.png`). Each module page has a coverage table (`Kattavuustaulukko`). The build fails if a code is not covered. The curriculum checker compared all 46 codes with ePerusteet word for word. |
| 6 | Every changing fact is a dated link. | pass | Every `official_links` entry has `read: 2026-11-21`. The help links show "(luettu 21.11.2026)". `/lahteet/` carries the read dates and the yearly-facts table. The build check for yearly figures passes, and the facts checker's scan found no yearly figure in any topic text. The 4 redirecting links are updated in `data/yearly-facts.yaml` and in the topics. |
| 7 | Internally, the build checks pass. | pass | 0 errors, 0 warnings, ruff clean, pytest green, no file over 500 lines, no external script, font, image or iframe (gates check, and I saw none in the templates). |
| 8 | Internally, the checkers' must-fix lists are empty or named in the judgement. | pass | See the next section. The round-0 must-fix items are all fixed. None is still open. |
| 9 | Internally, the judge accepts. | pass | Accept-with-minors. |

## Checkers' round-0 must-fix items, as checked in the files

- **Guidance after lukio (curriculum, facts):** The conditions from Lukiolaki § 25 are now stated, with a Finlex link:
  no study place, the year after completion, and the issuing school is responsible. The places are
  `content/pages/opetussuunnitelma.md:26`, `01-lukio-alkaa.md:105` and `18-urasuunnitelma.md:123`. The true/false
  claim in the lesson tables of 01 and 18 is now marked "tarua", with the condition.
- **Topic 08, yt9 and yt11 (curriculum):** There are new outcomes (lines 80–81), a self-assessment of information
  seeking (line 126), a section on online discussions, Tehtävä 3 on a fictional discussion, and a matching lesson row.
- **Opintopolku neuvonta (facts):** The page is now described as a contact directory, and higher-education applicants are
  pointed to the hakijapalvelut (`18:129`, 15, `guidance_services`).
- **Ensikertalainen (facts):** The rule is softened to "yleensä", with exceptions pointed to the hakijapalvelu
  (`15:112`).
- **Redirecting links (facts):** `kela.fi/opiskelu`, the YTL tietopalvelu, the saavutettavuusvaatimukset scope page and
  `yliopistovalinnat.fi/todistusvalinta` are in place. The old addresses are recorded in the notes.
- **Timing (pedagogy):** In every topic, Tehtävä 1 is 15 min and Tehtävä 2 and 3 are 10 min each. These match the
  75-min rows. The 60 and 45-min plans are full tables, and they keep the fictional-case row and the Puskuri.
  Self-study is 40 min with Tehtävä 1 and 2 required, which matches 8 + 15 + 10 + 5.
- **Other pedagogy items:**
  - The goals and HOPS lines match the tasks that are required.
  - Outcome counts are cut to 4–5.
  - "Ohjaaja tulostaa" is gone from the student tasks (0 hits).
  - "jos ei hae yliopistoon" is gone (0 hits), and the case names are rotated.
  - The triggers now have two-week thresholds or deadlines.
  - 04 has an acute 112/MIELI line, 13 has triggers for work rights plus Työsuojelu, and 16 has the
    Yhdenvertaisuusvaltuutettu.
  - Differentiation now has sentence starters and a bilingual glossary table.
  - 02 has a recall test.
  - 16 uses OPH Kansainvälistymispalvelut and "kansainvälinen opiskelija".
  - The CV task in 11 uses paper or a text file with placeholders.
  - 14 now says who is liable for service.
  - "pysyviä" is gone (0 hits).
- **Lesson table (browse):** The wrapper now has `role="region"`, `tabindex="0"` and a focus outline
  (`pipeline/markdown_render.py:47`, `site.css:162`). Keyboard users can now scroll it. On a narrow laptop the
  table is still wider than its box, but it scrolls. In `v_lessontall_1366.png` the table fits. At 500 px the
  stacked layout reads well.

## Brief's expected result compared with what happened

- **"18 topics, 2,000–3,500 words each, every code covered":** Met. Counted without front matter, the topics run from
  2,231 words (11) to 2,781 (18), and the build confirms coverage.
- **"Checks find fact and link problems first":** Partly. The facts checker found moved links and one law stated
  wrongly, but no yearly figures were typed into the text. The biggest finds were in pedagogy: timing that did not
  add up, and self-study goals that hung on optional tasks.
- **"Uneven voice between writers":** Not found. Copying the sample kept the voice even. The flip side was copied
  faults (07's timing) and repeated boilerplate, and round 1 fixed both.
- **"Vipunen, Ammattinetti, Studyinfo need a browser":** Confirmed. Vipunen opened only in Chrome and links to its
  front page only. Ammattinetti is not linked. Studyinfo is linked as the English Opintopolku.

## Remaining items (minor, none blocking)

1. Year and term still read as fact in some body text:
   - 07:118, "Ensimmäisen vuoden yo-suunnitelma"
   - 07:239 and 09:209, "Toisena opiskeluvuonna"
   - 10:97, 143 and 149, "viime vuonna" and "Ensimmäisen vuoden"

   The front matter correctly says "esimerkki, koulu päättää". Add "esimerkiksi", or write "edellinen suunnitelmasi".
2. The school deadline is said to be "aina ennen YTL:n viimeistä päivää" (07:84 and 155, 10:132). Write "yleensä".
3. The ILMO tool ("Tuleeko sinusta ylioppilas?") is not described as giving only an indicative result (07 Tehtävä 1, 10).
4. The "Tuki" link in 16, 17 and 18 still goes to a 2025 OPH news page. The other topics use the stable "Oppimisen tuen
   uudistus" page.
5. The "suoritusmerkintä (S tai H)" label is hard-coded in `pipeline/views_site.py` with no source. It comes from the
   general part of the curriculum (asetus 810/2018 § 17).
6. Wording:
   - 13:73, "tunnuksia"
   - 13:184, the lesson Tavoite sentence
   - 17:116, the yleinen asumistuki sentence could mislead students
   - 07:84, the school_adapts wording
7. Facts minors still open:
   - `study_right_rule` has no source page.
   - The intti.fi front page does not name siviilipalvelus.
   - The audience of the OPH "Miten valitsen oman alani?" page is unclear.
   - The yearly-fact notes on page reads are out of date.
8. Content repeats between pairs of topics: 07 and 10, 09 and 14, 05 and 11. Consider making the second pass go deeper.
9. Facts not checked again by anyone: the issuing school's responsibility under § 25, and "asevelvollisuus koskee Suomen
   miespuolisia kansalaisia" (14:95). The fixer took both from the checkers and did not re-open them.
10. Look: on a narrow laptop (about 830 px) the 75-min table scrolls sideways inside its box. A long word breaks
    mid-word in the meta grid ("ylioppilastutkintosuunnitelm/a"). Print was checked by text only.

## For the operator

- The site is ready to look at: two modules, nine topics each, every topic as a student page and a lesson plan.
- Before publishing, please print one lesson plan and look through the pages yourself. Nobody saw the printout as an
  image.
- On a small laptop the long lesson table scrolls sideways inside its box. Tell us if you would rather it wrapped.
- A few sentences still say "first year" or "second year" as if fixed. These are small wording fixes for next time.
- Publishing still waits for your choice of content licence.
