# Known issues: checklist for manual inspection

State of 2026-11-21, commit before brief 005. Sources: the judgements of briefs 002–004
(`docs/review/`) and the image re-judgement. Tick an item when you have looked at it on the site. "Fixing" means
brief 005 is changing it now; the live site gets it on the next push.

## Content: errors to fix before wider use (fixing)

- [ ] **Topic 01** (`/op1/01-lukio-alkaa/`): splits the national optional studies into "syventävät ja soveltavat".
  The 2019 curriculum does not make that split. The diagram `dg-opintojen-rakenne` repeats it. Both are being remade.
- [ ] **Topic 02** (`/op1/02-opiskelutaidot/`): "oikeus oppimisen ja opiskelun tukeen" should be "oikeus oppimisen
  tukeen" (Lukiolaki § 28).
- [ ] **Topics 07 and 10**: the matriculation exam rule lacks the äidinkieli exception (Laki ylioppilastutkinnosta
  § 11) and a "poikkeuksista katso YTL" line.

## Content: lesson quality (fixing)

- [ ] **Offline alternatives in topics 13–18** still say "read the cases on this page". A student with no device
  cannot do that.
- [ ] **Goals versus tasks:** in topics 13, 14, 15 and 18, the lesson goal, the plan rows and the task steps do not
  fully agree. Topic 18's 45-minute HOPS row is too short.
- [ ] **Outcomes no task practises:** topic 05 (outcome 3 and "one thing you want to learn"), 18 (outcome 5), and
  some in 03, 04 and 06.
- [ ] **Topic 05:** an OPH page aimed at counsellors is linked as if it were for students.
- [ ] **Topic 14** says "Varusmiespalvelus" where the routes diagram says "Asepalvelus".

## Pictures

- [ ] **Working life** (`/op2/12-tyoelama-ja-ennakointi/`): shows six scenes instead of four, two of them similar.
  Being remade as one scene (fixing).
- [ ] **OP1 page:** the alt text says "hall", but the picture shows a classroom (fixing).
- [ ] **Routes diagram** (`/op2/14-koulutusvaylat/`): its caption sits close to the bottom edge.
- [ ] **OP2 page:** two students wear pleated skirts that could read as school uniforms. Your call.
- [ ] **Money and housing** (`/op2/17-talous-ja-asuminen/`): a stray lamp shape, and the top half is empty.
- [ ] Look at all 21 illustrations and 7 diagrams together: do they suit the site and each other?

## Look and use (not yet seen by a person)

- [ ] **Print a lesson plan** (any topic → "Tuntisuunnitelma" view → print, or `/tulosta/op1/`). It was checked by
  text only, never as paper.
- [ ] **Phone:** on a narrow screen the long lesson table scrolls sideways inside its box. Do you want it wrapped?
- [ ] **Self-study path** (`/polku/`): tick a step, write a note, reload, then press "Tyhjennä tietoni". Without
  JavaScript, the "Merkitse tehdyksi" buttons show but do nothing.
- [ ] **Voice:** read two topics as a student and two lesson plans as a counsellor. Is the Finnish natural and
  consistent?

## Facts a person should confirm once

- [ ] Lukiolaki 714/2018 § 25 (guidance, also after graduation) and § 28 (learning support), as the topics cite them.
- [ ] Siviilipalvelus is backed only by intti.fi. siviilipalvelus.fi could not be opened by the agents.
- [ ] Vipunen, Ammattinetti, Euroguidance and Studyinfo links were partly unreachable to the agents. Check that
  they open.
- [ ] The national open-material library aoe.fi could not be searched, so "no open lesson set exists" is likely, not
  proven.

## Publishing

- [ ] The repository and site are public. The pages carry no `noindex`, so search engines may list them.
- [ ] The repository names game-engine's image modules (pimage) and how they were used. No secrets or internals
  beyond that. Your call whether that is fine.
- [ ] Curriculum text is quoted from Opetushallitus (ePerusteet); the licence page says it is not under CC BY.
