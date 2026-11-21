export const meta = {
  name: 'build-site',
  description: 'lukion-opinto-ohjaus: foundation (pipeline, sample topic and style guide, yearly facts), topic writers, integrate, five separate checks, fix and recheck by file owner, judge',
  whenToUse: 'Run a committed build brief. args: {brief, root, now, judgement}',
  phases: [
    { title: 'Foundation', detail: 'pipeline and site; sample topic 07 and style guide; yearly facts' },
    { title: 'Topics', detail: 'four writers following the sample' },
    { title: 'Integrate', detail: 'build and fix joins' },
    { title: 'Check', detail: 'curriculum, facts, pedagogy and language, browse, gates' },
    { title: 'Fix', detail: 'content fixer and code fixer, then recheck; at most two rounds' },
    { title: 'Judge', detail: 'rules on Done when from files only' },
  ],
}

const ROOT = args && args.root
if (!ROOT) throw new Error('args.root (the project folder) is required')
const BRIEF = (args && args.brief) || 'prompts/002-build-site.md'
const NOW = (args && args.now) || '2026-11-21'
const JUDGEMENT = (args && args.judgement) || 'docs/review/2026-11-21-brief-002-judgement.md'
const SHOTS = `${ROOT}\\tmp\\shots`

const RF = `Project root: ${ROOT}. First read ${ROOT}\\CLAUDE.md (rules), ${ROOT}\\${BRIEF} (the brief), ${ROOT}\\docs\\content-contract.md (the interface) and ${ROOT}\\docs\\research\\2026-11-21-research.md; the critic's full proposal (topic list with curriculum codes, contract, site structure, yearly facts) is the 'proposal' array in ${ROOT}\\docs\\research\\2026-11-21-scouting.json. Today is ${NOW}. Do not commit, push or publish. Never print secrets. Leave no server running. Write only the files you own; if the contract must change, append a dated addendum to docs/content-contract.md and say so. Web reads: at most two tries per page; list pages you could not read instead of retrying. The site language is Finnish.`
const REPORT = { type: 'object', properties: { files: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' }, open_issues: { type: 'array', items: { type: 'string' } } }, required: ['files', 'summary', 'open_issues'] }
const CHECK = { type: 'object', properties: { passed: { type: 'boolean' }, must_fix: { type: 'array', items: { type: 'object', properties: { what: { type: 'string' }, where: { type: 'string', description: 'file path (and line or topic id)' }, owner: { type: 'string', enum: ['content', 'code'] }, evidence: { type: 'string' } }, required: ['what', 'where', 'owner'] } }, minor: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' } }, required: ['passed', 'must_fix', 'summary'] }
const WRITE_RULES = `Write in plain, warm, respectful Finnish (selkeä yleiskieli) addressed to the student as 'sinä' in the student sections and to the counsellor in the lesson plan. Follow docs/style-guide.md and the sample content/topics/07-ylioppilastutkinto.md exactly in structure and voice. Every section of the contract, in order. Curriculum codes from the critic's topic list (proposal task 'a'); never type curriculum wording. Every official link has a read date (open the page with WebFetch; if it fails twice, use a stable parent page you could open, or leave it out and say so). No yearly figure typed in the text: link it. All routes count equally (university, AMK, vocational, kansanopisto, gap year, service, work, abroad); no gendered or stereotyped examples; task cases use clearly fictional first names. No reflection asks the student to share personal data with the site. Original text only.`

phase('Foundation')
const foundation = (await parallel([
  ['pipeline', 'sonnet', `You are the pipeline and site builder. ${RF}
You own pipeline/, templates/, site-src/, tests/, pyproject.toml, .github/workflows/pages.yml and the static pages' sources (put their Finnish text in content/pages/*.md: etusivu, opetussuunnitelma, tietosuoja, saavutettavuus, lahteet intro, polku intro). Build in Python 3.13 (Markdown and PyYAML; check with pip, install into the user site only if missing):
1. pipeline/fetch_curriculum.py: fetch https://eperusteet.opintopolku.fi/eperusteet-service/api/perusteet/6828810/kaikki, find oppiaine OP (id 6835370) and modules OP1 (6835293) and OP2 (6835294), and write data/curriculum.yaml with exact Finnish wording keyed OP1.t1..t9, OP1.s1..s8, OP2.t1..t10, OP2.s1..s8, OP.yt1..yt11 in ePerusteet order, plus module names, credits, assessment text, the record's last publication date and checked date. Normalize at the boundary (strip HTML). Run it.
2. pipeline/build.py: read content/topics/*.md and content/pages/*.md and write _site/ per the site structure in the contract: front page, /op1/ /op2/ with exact objectives and contents and a coverage matrix, each topic as a student view and a /tunti/ lesson view, /polku/, /tulosta/op1/ and /tulosta/op2/, /opetussuunnitelma/, /lahteet/ (links with read dates and the yearly-facts table), /tietosuoja/, /saavutettavuus/. Relative links only, so it works under /lukion-opinto-ohjaus/ on GitHub Pages and from a local server. No JavaScript needed to read. A small site-src/js/polku.js stores progress and notes under localStorage key 'loo:v1' only on a click, with a 'Tyhjennä tietoni' button; without JS the path is a list. CSS: system font stack (no external fonts), light and dark themes with AA contrast, reflow at 320 px, a print stylesheet for lesson plans.
3. pipeline/checks.py: every build check in the contract (unknown code, uncovered code, missing or out-of-order section, lesson minutes not adding up, link without read date or older than 12 months, a figure next to a yearly fact outside a link, any external non-link resource in _site). The build exits non-zero on a failure and prints each problem with file and line.
4. tests/: fast unit tests for the checks and the build helpers (no network).
5. .github/workflows/pages.yml: on push to main, set up Python, install deps, run the build (without refetching the curriculum; data/curriculum.yaml is committed), upload _site, deploy to Pages.
Other agents write content/topics/ and data/yearly-facts.yaml at the same time, so the build must cope with missing topics while you develop. Limits: no file over 500 lines, ruff clean, names that say what they are for. Run ruff and pytest before returning.`],
  ['sample', undefined, `You are the lead writer and set the voice. ${RF}
You own content/topics/07-ylioppilastutkinto.md and docs/style-guide.md.
1. Write docs/style-guide.md (under 200 lines, in English with Finnish examples): voice (sinä to the student; collegial to the counsellor), plain Finnish rules, a glossary of guidance terms with the exact official forms (HOPS, ylioppilastutkinto, yhteishaku, todistusvalinta, ensikertalainen, jatko-opintosuunnitelma ...), how 'Osaan' outcomes mirror objectives, how tasks are written (title, time, materials, up to 5 steps, offline alternative), how lesson tables are written, inclusive and non-segregating language, how to link yearly facts, what never to do.
2. Write topic 07 'Ylioppilastutkinto ja alustava yo-suunnitelma' in full to the contract, with its codes from the critic's list (OP1.t6, OP1.t7, OP1.s1, OP1.s8), official links to YTL pages opened with WebFetch (read dates), the stable five-test rule stated, every changing value linked. It must be the best example a writer can copy: complete, warm, concrete, usable tomorrow by a counsellor and by a student alone.
${WRITE_RULES}`],
  ['facts', 'sonnet', `You are the yearly-facts curator. ${RF}
You own data/yearly-facts.yaml only. For every key in the contract's list (and any the critic's task 'd' adds), write key, rule (one plain Finnish sentence that states only the stable rule), url (the most stable official landing page), publisher, read (${NOW}). Open each URL with WebFetch. For the ones the research could not open (Vipunen, Ammattinetti, Euroguidance, Studyinfo, siviilipalvelus.fi, the Opintopolku front page, aoe.fi), try once more; if a fetch fails, try headless Chrome: the local Chrome executable --headless=new --dump-dom <url>. Record what could not be verified in a 'note' field and prefer a verified parent page. Validate the YAML parses.`],
].map(([k, m, p]) => () => agent(p, { label: `foundation:${k}`, phase: 'Foundation', schema: REPORT, ...(m ? { model: m } : {}) }).then(r => r && ({ key: k, ...r }))))).filter(Boolean)
log(`foundation: ${foundation.map(f => f.key).join(', ')}`)

phase('Topics')
const GROUPS = [
  ['op1-a', 'topics 01, 02, 03, 04, 05 and 06 of OP1'],
  ['op1b-op2a', 'topics 08 and 09 of OP1 and topics 10, 11 and 12 of OP2'],
  ['op2-b', 'topics 13, 14 and 15 of OP2'],
  ['op2-c', 'topics 16, 17 and 18 of OP2'],
]
const writers = (await parallel(GROUPS.map(([k, which]) => () => agent(`You are a topic writer. ${RF}
Write ${which}, each as content/topics/NN-slug.md (NN two digits, slug from the Finnish title), with the titles, timing and curriculum codes of the critic's topic list (proposal task 'a'). You own only those files. Read docs/style-guide.md and the sample content/topics/07-ylioppilastutkinto.md first and match them. Use data/yearly-facts.yaml keys for changing facts. When done, run python -m pipeline.build (or the entry point in pipeline/) and fix any check failure in your own files.
${WRITE_RULES}`, { label: `topics:${k}`, phase: 'Topics', model: 'sonnet', schema: REPORT }).then(r => r && ({ key: k, ...r }))))).filter(Boolean)

phase('Integrate')
const integration = await agent(`You are the integrator. ${RF}
Builders reported: ${JSON.stringify([...foundation, ...writers]).slice(0, 30000)}
Run the build end to end. Make it pass: fix join problems at their root (pipeline/ for code, the topic file for content: a wrong code, a missing section, minutes not adding up, a link without a date). Do not invent facts. Confirm all 18 topics and every curriculum code are covered. Serve _site on a free port and load the front page, one topic in both views, /polku/ and /tulosta/op1/ in headless Chrome (--dump-dom) to confirm they render; stop the server. Run ruff and pytest. Return what you changed and the build's summary.`, { label: 'integrate', phase: 'Integrate', model: 'sonnet', schema: REPORT })

const CHECKS = {
  curriculum: ['sonnet', `You are the curriculum-fidelity checker; you wrote nothing. ${RF} Compare every topic's cited codes with data/curriculum.yaml and with what the topic actually teaches: does the content serve the cited objectives and content areas, is anything presented as required by the curriculum that is not, are module names, credits and S/H assessment right, are law references right (Lukiolaki 714/2018 § 25, § 26), is year and term shown as an example? Spot-check data/curriculum.yaml against the ePerusteet API for 5 codes. Do not edit.`],
  facts: ['sonnet', `You are the facts and links checker; you wrote nothing. ${RF} Open every official link in the topics and data/yearly-facts.yaml (WebFetch; on failure, headless Chrome --dump-dom once). Report broken or wrong links, links whose page does not support the sentence they back, read dates missing, stable rules stated wrongly (e.g. the five-test rule of the ylioppilastutkinto, YTL enrolment rules, first-time applicant rules, student aid rules), and any yearly figure typed into text. Do not edit.`],
  pedagogy: ['sonnet', `You are the pedagogy and language checker; you wrote nothing. ${RF} Read all 18 topics. Check: plain, correct Finnish and a consistent voice across writers (compare with topic 07 and docs/style-guide.md); every lesson table adds up to its length and the 60 and 45 variants are realistic; tasks are concrete and doable in the time; differentiation is real; nothing stereotypes by gender or background and every route is treated as equal; no reflection asks for personal data to be shared; 'when to see the counsellor' is concrete; examples use fictional names. List problems per topic with section. Do not edit.`],
  browse: ['sonnet', `You are the browsing checker at viewing size; you wrote nothing. ${RF} Serve ${ROOT}\\_site on a free port. With headless Chrome (the local Chrome executable --headless=new --screenshot=<file> --window-size=1366,900 and 500,900, plus --dump-dom for links and --disable-javascript for the no-JS check) capture the front page, /op1/, one topic in student and lesson view, /polku/, /tulosta/op1/ (also print to PDF with --print-to-pdf and look at it), /opetussuunnitelma/, /lahteet/, /tietosuoja/. Save to ${SHOTS}\\ and LOOK at each with Read. Must-fix: broken or empty pages, broken relative links, a page unreadable without JS, localStorage written on page load (inspect polku.js), overflow, unreadable print, missing privacy page content. Stop the server. Do not edit.`],
  gates: ['haiku', `You are the gate checker; you wrote nothing. ${RF} In ${ROOT} run the build (it must exit 0), ruff check pipeline tests, pytest -q (fast, no network), line counts of pipeline/ tests/ site-src/ templates/ (over 500 fails), and grep _site for external resources (src= or href= to http(s) hosts on script, link rel=stylesheet, img, iframe, font). Each failure is a must_fix with the file. Do not edit.`],
}
const runChecks = keys => parallel(keys.map(k => () =>
  agent(CHECKS[k][1], { label: `check:${k}`, phase: 'Check', model: CHECKS[k][0], schema: CHECK }).then(r => r && ({ check: k, ...r }))))

phase('Check')
let checks = (await runChecks(Object.keys(CHECKS))).filter(Boolean)
const history = [{ round: 0, checks }]
let failing = checks.filter(c => !c.passed || c.must_fix.length)

for (let round = 1; round <= 2 && failing.length; round++) {
  phase('Fix')
  const items = failing.flatMap(c => c.must_fix.map(f => ({ check: c.check, ...f })))
  log(`round ${round}: ${items.length} must-fix items from ${failing.map(c => c.check).join(', ')}`)
  const byOwner = o => items.filter(i => (i.owner || 'content') === o)
  const fixes = (await parallel([
    ['content', `content/ and data/yearly-facts.yaml`],
    ['code', `pipeline/, templates/, site-src/, tests/ and .github/`],
  ].filter(([o]) => byOwner(o).length).map(([o, files]) => () => agent(`You are the ${o} fixer for round ${round}. ${RF}
You own ${files}. Fix each item at its root; do not touch files you do not own (if an item needs the other owner, say so). Rebuild and rerun ruff and pytest at the end. Never invent facts.
${o === 'content' ? WRITE_RULES : ''}
Items: ${JSON.stringify(byOwner(o))}`, { label: `fix:${o}-${round}`, phase: 'Fix', model: 'sonnet', schema: REPORT }).then(r => r && ({ owner: o, ...r }))))).filter(Boolean)
  const re = (await runChecks(failing.map(c => c.check))).filter(Boolean)
  checks = checks.map(c => re.find(r => r.check === c.check) || c)
  history.push({ round, fixes, recheck: re })
  failing = checks.filter(c => !c.passed || c.must_fix.length)
}
if (failing.length) log(`still failing: ${failing.map(c => c.check).join(', ')}; the judge will rule`)

phase('Judge')
const judgement = await agent(`You are the judge; you wrote nothing in this project. Rule from files only: ${ROOT}\\${BRIEF}, CLAUDE.md, the content contract, the topics, data, code and _site, and the screenshots in ${SHOTS}\\ (look at them with Read). Run the build, ruff and pytest yourself. Context, which you verify rather than trust: ${JSON.stringify(history).slice(0, 50000)}
Rule on each line of the brief's 'Done when', in the operator's terms first, and compare with its expected result. Read at least four topics in full yourself (one per writer group, plus topic 07). Write ${ROOT}\\${JUDGEMENT} (under 200 lines): the verdict (accept / accept-with-minors / reject), a table of each Done-when line with pass or fail and file evidence, remaining items, and at most 5 plain-words lines for the operator. Do not commit.`,
  { label: 'judge', phase: 'Judge', schema: { type: 'object', properties: { verdict: { type: 'string', enum: ['accept', 'accept-with-minors', 'reject'] }, operator_summary: { type: 'string' }, remaining: { type: 'array', items: { type: 'string' } } }, required: ['verdict', 'operator_summary', 'remaining'] } })

return { foundation, writers, integration, checks, rounds: history.length - 1, judgement }
