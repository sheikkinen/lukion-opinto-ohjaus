# Lukion opinto-ohjaus

**Sivusto:** <https://sheikkinen.github.io/lukion-opinto-ohjaus/>

Avoin runko lukion opinto-ohjaukseen. Se seuraa lukion opetussuunnitelman perusteita 2019 (voimassa 1.8.2021
alkaen). Molemmat pakolliset moduulit, OP1 *Minä opiskelijana* ja OP2 *Jatko-opinnot, työelämä ja tulevaisuus*,
on jaettu yhdeksään aiheeseen. Jokaista aihetta voi käyttää kahdella tavalla:

- **itsenäisenä oppituntina:** opinto-ohjaajalle on tuntisuunnitelma 75, 60 ja 45 minuutin oppitunnille;
- **itseopiskelun askeleena:** opiskelija etenee polkua omaan tahtiinsa, ja merkinnät jäävät vain hänen omalle
  laitteelleen.

Jokainen aihe kertoo, mitä opetussuunnitelman tavoitteita ja sisältöjä se palvelee. Joka vuosi muuttuvat tiedot
(koepäivät, hakuajat, opintotuen määrät) ovat linkkejä viralliseen lähteeseen lukupäivän kera, ei kopioita.
Sivusto ei kerää tietoja: siinä ei ole tilejä, analytiikkaa eikä ulkoisia skriptejä.

**Lisenssi:** CC BY 4.0, katso [LICENSE](LICENSE). Opetussuunnitelman tekstit ovat Opetushallituksen
(ePerusteet), eivätkä ne kuulu CC BY -lisenssin piiriin.

**Tunnetut puutteet:** [docs/known-issues.md](docs/known-issues.md).

## Rakentaminen

```bash
python -m pip install -r requirements.txt
lukio-runko build
python -m http.server 8000 --directory _site
```

Aiheet ovat tiedostoissa `content/topics/` (Markdown, rakenne kuvattu tiedostossa
[docs/content-contract.md](docs/content-contract.md)). Opetussuunnitelman tekstit haetaan ePerusteista komennolla
`lukio-runko fetch-curriculum`. Build pysähtyy, jos jokin tavoite jää ilman aihetta, jos tuntisuunnitelman
minuutit eivät täsmää tai jos linkiltä puuttuu lukupäivä. GitHub Pages julkaisee sivuston jokaisesta `main`-haaran
pushista.

Sivuston rakentaa yhteinen moottori [lukio-runko](https://github.com/sheikkinen/lukio-runko), jonka versio on
lukittu tiedostossa `requirements.txt`. Tässä repositoriossa on vain sisältö, data, `subject.yaml` ja
dokumentaatio.

---

## How this was made: the flow

The operator's request: "Lukion opinto-ohjaus, following finnish curriculum. it should serve as stand-alone
backbone for lukion opinto-ohjaus content divided in topics that could be handled as stand-alone lessons - or as a
self learning path", on a GitHub-hosted site. The process is reused from two earlier projects (World Today and World
Literature): briefs written before the work, research by a fan-out plus a critic, a contract before building,
checkers who did not write what they check, and a judge outside the author. Every brief is in `prompts/`, every
decision in `decisions/INDEX.md`, every ruling in `docs/review/`, and a diary line per brief in `docs/diary/`.

| Step | What happened | Agents |
|---|---|---|
| Scoping | Three questions with defaults: full lessons, multi-agent workflows, the name. The rest went into the brief as defaults the operator could override (Finnish, both modules, no tracking, €0). Later the operator confirmed Finnish (D-006) and chose CC BY (D-008). | — |
| Brief 001, research | `scout.js`: six researchers (curriculum and law, topics, pedagogy, self-study and privacy, official facts, existing material), then an Opus critic. The curriculum was read from the ePerusteet API, so the objectives are quoted exactly. The critic corrected the expected answers: the real module names, § 25 not § 24, and four topics the brief had missed. | 7 |
| Contract | The critic's proposal became `docs/content-contract.md`: curriculum codes instead of typed text, fixed sections, lesson tables that must add up, dated links, and build checks that enforce all of it. | — |
| Brief 002, build | `build-site.js`: a pipeline builder, a lead writer (topic 07 and the style guide, to set the voice), a facts curator, four topic writers, an integrator, five checkers, two fix rounds split by file owner, and a judge. Accepted with minors, with 12 checker items still open. | 25 |
| Brief 003, images | Budget €10 (D-007). `images.js`: a tool builder (game-engine's pimage modules, read-only) and an art director, generation by script, checks, redo rounds, a judge. The 7 Finnish diagrams on nano-banana were right first time. The illustrations failed on klein because the shared drive was full, so the producer switched them to p-image (D-009). Rejected, then followed up and accepted. Spend: $0.40. | 15 + 5 |
| Brief 004, lesson quality | `fix-content.js`, in parallel with brief 003 on separate files: four fixers per topic group, three checkers, one refix round, and a judge ruling on the final recheck. Plans now fit 45 minutes and keep the goal task; HOPS privacy and the gender-aware check are in every topic. | 15 |
| Publish for inspection | The operator asked for inspection before the final polish. The producer scanned every commit for secrets, local paths and e-mail (clean), wrote `docs/known-issues.md`, created the public repo, turned on Pages, and watched the deploy. | — |
| Brief 005, polish | The last content items, two picture remakes, two pre-publish scanners over the full history, a judge. Running at the time of writing; its fixes reach the site with the next push. | 9 |
| Live check | Two agents on the deployed site: pages at desktop and phone width, print to PDF, what a visitor can reach, the privacy page. | 2 |

About 78 subagents, about 10 million subagent tokens, and $0.40 of image spend.

## Reflections: the orchestrator's notes

**What worked.**
- *Reading the curriculum from its source.* The ePerusteet API gave the exact objective and content texts. Every
  topic cites codes, and the build resolves them and fails when one is left uncovered. The critic's spot-check
  caught that my expected module names were wrong before anything was written.
- *One sample before many writers.* Topic 07 and the style guide set the voice, and four writers followed them. The
  checkers found little drift in tone between writers.
- *File ownership made parallel work possible.* Briefs 003 and 004 ran at the same time on the same checkout
  without clashing, because each workflow owned separate files.
- *Lessons carried forward.* The World Today fix loop had not converged, so this time fixers were split by file
  owner, the judge ruled on the final recheck (the brief 002 diary's heuristic), and the defaults went into the
  brief instead of becoming questions. `scout.js` was reused with only the critic's tasks changed.
- *Checks a script can do.* The diagrams' Finnish labels were checked letter by letter against the expected labels,
  and none was wrong. Lesson minutes, dated links, curriculum coverage and external requests are build checks, not
  opinions.

**What did not work as well.**
- *The recheck always finds something new.* 12 open items became 7, and then a few more appeared. Each round of
  readers sees more. The workable answer was the one the operator asked for: publish with a checklist of known
  issues, and let the next round fix them.
- *Writers copy numbers, not reasons.* Every topic first had the sample's 15, 10 and 10 minute tasks, and several
  "offline" alternatives still needed the web page. Rules that only a reader can check keep slipping. Mechanical
  checks would help: an outcome named in a required task, and no "this page" in an offline line.
- *The environment is part of the toolchain.* A full shared drive stopped the free local image model, and the
  first image brief was rejected for it. A disk check before a local run would have saved a round.
- *Image models ignore counts.* p-image drew six scenes for a four-scene prompt three times. One scene per picture,
  with counts kept for diagrams, works better.
- *Size and cost.* The build alone ran 25 agents and 4.3 million tokens, far above a small team's guideline. Most
  of the value came from the critic, the sample topic and the checkers; the fix rounds cost the most for the least.
- *Published before the last scan, by choice.* The operator chose to inspect early. My own scan covered secrets,
  local paths and e-mail across every commit. The deeper scan for private-project detail runs in brief 005, after
  the push.

**What the evidence does and does not cover.** Agents read the curriculum, the law and the official pages, and
other agents checked their work. No counsellor has taught a lesson from it, no student has walked the path, and no
person has yet printed a lesson plan or read the Finnish as a whole. Two legal points (Lukiolaki § 25 and § 28) are
ruled from files and should be checked once on Finlex by a person. The checklist in `docs/known-issues.md` is the
honest state of the site.
