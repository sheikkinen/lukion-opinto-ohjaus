export const meta = {
  name: 'fix-content',
  description: 'lukion-opinto-ohjaus: content fixers per topic group apply open items, separate checkers recheck, one more fix round, judge rules on the final recheck',
  whenToUse: 'A content follow-up brief with an open-items file. args: {brief, root, now, items_file, judgement}',
  phases: [
    { title: 'Fix', detail: 'four fixers, one per topic group' },
    { title: 'Check', detail: 'pedagogy, curriculum, facts' },
    { title: 'Refix', detail: 'one round on the recheck' },
    { title: 'Judge', detail: 'rules on the final recheck' },
  ],
}

const ROOT = args && args.root
if (!ROOT) throw new Error('args.root (the project folder) is required')
const BRIEF = args && args.brief
const ITEMS = args && args.items_file
const NOW = (args && args.now) || '2026-11-21'
const JUDGEMENT = args && args.judgement
if (!BRIEF || !ITEMS || !JUDGEMENT) throw new Error('args.brief, args.items_file and args.judgement are required')

const GROUPS = [
  ['01-06', 'content/topics/01-* to 06-*'],
  ['07-12', 'content/topics/07-* to 12-*'],
  ['13-15', 'content/topics/13-* to 15-*'],
  ['16-18', 'content/topics/16-* to 18-*, content/pages/ and data/yearly-facts.yaml'],
]
const RF = `Project root: ${ROOT}. Read ${ROOT}\\CLAUDE.md, ${ROOT}\\${BRIEF} (your brief), docs/content-contract.md, docs/style-guide.md and the open items in ${ROOT}\\${ITEMS}. Today is ${NOW}. Do not commit or push. Leave no server running. Never touch data/images.yaml, tools/, pipeline/, templates/ or site-src/ (another workflow owns them right now). Web reads: at most two tries per page. Write in the voice of topic 07 and the style guide.`
const REPORT = { type: 'object', properties: { files: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' }, not_done: { type: 'array', items: { type: 'string' } } }, required: ['files', 'summary', 'not_done'] }
const CHECK = { type: 'object', properties: { passed: { type: 'boolean' }, must_fix: { type: 'array', items: { type: 'object', properties: { what: { type: 'string' }, where: { type: 'string' } }, required: ['what', 'where'] } }, minor: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' } }, required: ['passed', 'must_fix', 'summary'] }

const fixers = (round, extra) => parallel(GROUPS.map(([k, files]) => () => agent(`You are the content fixer for ${files}, round ${round}. ${RF}
You own only ${files}. Apply every open item that touches your files, and the cross-cutting rules of the brief in all of them. ${extra || ''}
Then run python -m pipeline.build and fix any check failure in your files (if a failure is in someone else's file, leave it and say so).`,
  { label: `fix:${k}-r${round}`, phase: round === 1 ? 'Fix' : 'Refix', model: 'sonnet', schema: REPORT }).then(r => r && ({ group: k, ...r }))))

const CHECKS = {
  pedagogy: `You are the pedagogy and language checker; you wrote nothing. ${RF} Read all 18 topics. Check: every lesson table adds up and is realistic for 75, 60 and 45 minutes, and the goal task stays in each; task times fit the work; every offline alternative works for a student alone with paper and pen; HOPS prompts separate what belongs in the shared HOPS from one's own notes; open-question banks need no disclosure; the gender-aware assumption check is there; outcomes are practised by tasks; year placement reads as an example; plain, consistent Finnish. Do not edit.`,
  curriculum: `You are the curriculum-fidelity checker; you wrote nothing. ${RF} Compare every topic's cited codes with data/curriculum.yaml and with what it teaches; check the curriculum's own terms (e.g. 'valtakunnalliset valinnaiset opinnot'), law references, and that timing is an example. Do not edit.`,
  facts: `You are the facts and links checker; you wrote nothing. ${RF} Open every official link that changed since the last commit (git diff HEAD -- content data) and spot-check 10 others; check stable rules stated in changed text and that no yearly figure is typed outside a link. Do not edit.`,
}
const runChecks = keys => parallel(keys.map(k => () => agent(CHECKS[k], { label: `check:${k}`, phase: 'Check', model: 'sonnet', schema: CHECK }).then(r => r && ({ check: k, ...r }))))

phase('Fix')
const round1 = (await fixers(1)).filter(Boolean)
phase('Check')
let checks = (await runChecks(Object.keys(CHECKS))).filter(Boolean)
const history = [{ round: 1, fixes: round1, checks }]
let failing = checks.filter(c => !c.passed || c.must_fix.length)
if (failing.length) {
  phase('Refix')
  const items = failing.flatMap(c => c.must_fix.map(f => ({ check: c.check, ...f })))
  const round2 = (await fixers(2, `These are the recheck's must-fix items; apply those in your files: ${JSON.stringify(items)}`)).filter(Boolean)
  const re = (await runChecks(failing.map(c => c.check))).filter(Boolean)
  checks = checks.map(c => re.find(r => r.check === c.check) || c)
  history.push({ round: 2, fixes: round2, recheck: re })
  failing = checks.filter(c => !c.passed || c.must_fix.length)
}
const finalOpen = failing.flatMap(c => c.must_fix.map(f => ({ check: c.check, ...f })))

phase('Judge')
const judgement = await agent(`You are the judge; you wrote nothing in this project. Rule from files only: ${ROOT}\\${BRIEF}, CLAUDE.md, the open-items file ${ITEMS}, the topics and data. Run python -m pipeline.build and pytest yourself. Read at least five topics in full (one per group plus 07), including their 45-minute plans and offline alternatives.
Rule first on the FINAL recheck's open items, which are: ${JSON.stringify(finalOpen)}. For each, say whether it is real and whether it blocks publishing. Then rule on each Done-when line. Context to verify, not trust: ${JSON.stringify(history).slice(0, 40000)}
Write ${ROOT}\\${JUDGEMENT} (under 150 lines): verdict (accept / accept-with-minors / reject), a table, remaining items, at most 5 plain lines for the operator. Do not commit.`,
  { label: 'judge', phase: 'Judge', schema: { type: 'object', properties: { verdict: { type: 'string', enum: ['accept', 'accept-with-minors', 'reject'] }, operator_summary: { type: 'string' }, remaining: { type: 'array', items: { type: 'string' } } }, required: ['verdict', 'operator_summary', 'remaining'] } })

return { history_rounds: history.length, final_open: finalOpen, checks, judgement }
