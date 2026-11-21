export const meta = {
  name: 'images',
  description: 'lukion-opinto-ohjaus: image tool and art direction in parallel, generation by script, separate image/browse/gate checks, redo rounds, judge',
  whenToUse: 'Run a committed images brief. args: {brief, root, now, judgement, max_dollars}',
  phases: [
    { title: 'Prepare', detail: 'tool builder and art director' },
    { title: 'Generate', detail: 'run the tool: diagrams first' },
    { title: 'Check', detail: 'image checker, browse, gates' },
    { title: 'Redo', detail: 'revise prompts, remake failed pictures; SVG fallback for diagrams' },
    { title: 'Judge' },
  ],
}

const ROOT = args && args.root
if (!ROOT) throw new Error('args.root (the project folder) is required')
const BRIEF = (args && args.brief) || 'prompts/003-images-and-diagrams.md'
const NOW = (args && args.now) || '2026-11-21'
const JUDGEMENT = (args && args.judgement) || 'docs/review/2026-11-21-brief-003-judgement.md'
const MAX = (args && args.max_dollars) || 10
const SHOTS = `${ROOT}\\tmp\\shots-images`

const RF = `Project root: ${ROOT}. First read ${ROOT}\\CLAUDE.md, ${ROOT}\\${BRIEF} (the brief) and ${ROOT}\\docs\\content-contract.md. game-engine (the folder named by GAME_ENGINE_DIR) is READ-ONLY: never write, commit or run git there; import its tools/pimage modules only through sys.path. Never print, log or commit an API key, and never read game-engine's .env yourself (pimage's read_token does that). Respect game-engine's GPU lock: local klein pictures go only through pimage's clients.make_api, which takes the lock and starts ComfyUI itself; never start ComfyUI another way. Spending cap for the whole brief: $${MAX}; stop and report before passing it. Today is ${NOW}. Do not commit, push or publish. Leave no server running.`
const REPORT = { type: 'object', properties: { files: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' }, dollars_spent: { type: 'number' }, open_issues: { type: 'array', items: { type: 'string' } } }, required: ['files', 'summary', 'open_issues'] }
const CHECK = { type: 'object', properties: { passed: { type: 'boolean' }, must_fix: { type: 'array', items: { type: 'object', properties: { image_id: { type: 'string' }, what: { type: 'string' }, owner: { type: 'string', enum: ['prompt', 'code'] } }, required: ['what', 'owner'] } }, minor: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' } }, required: ['passed', 'must_fix', 'summary'] }

phase('Prepare')
const prep = (await parallel([
  ['tool', 'sonnet', `You are the image tool builder. ${RF}
You own tools/images.py, tests/test_images.py and the image-placement part of pipeline/ and templates/ (the build must place each picture from data/images.yaml: the topic header illustration, diagrams at a named section, the front and module page images; with width, height, loading="lazy", and alt from the manifest; alt="" for decorative). Read game-engine's tools/pimage/models.py (ADAPTERS, CREATE), clients.py (make_api, Router.run_many), replicate_client.py (ReplicateClient, read_token) and budget.py, and use them: nano-banana through ReplicateClient, klein through make_api with game-engine's host file (hosts/<machine>.yaml, found by clients.host_file with repo=the GAME_ENGINE_DIR folder). tools/images.py reads data/images.yaml (schema in the brief), prints the planned calls and dollars first, stops before passing --max-dollars (default ${MAX}), supports --only and --redo (ids), --kind diagram|illustration, converts the output to WebP under 200 KB (Pillow), writes site-src/img/<id>.webp and appends to data/images.run.yaml (id, model id, prompt, seed, sha256, dollars, date; no key, no local path). A picture already made is kept unless --redo. Tests: fast, with fake clients, no network or GPU. Keep files under 500 lines; ruff clean. Wait until data/images.yaml exists before a real run; do not run a paid call yourself.`],
  ['art', undefined, `You are the art director. ${RF}
You own data/images.yaml. Read the topics in content/topics/ and docs/style-guide.md. Write: a top-level 'style' line for all illustrations (calm, friendly, flat editorial illustration, soft limited palette that suits a Finnish school site, no text, no logos, varied genders and backgrounds, no real people, no uniforms); then 'images', one entry per picture: id, kind (diagram|illustration), model (diagram -> nano-banana; illustration -> klein, per the operator), aspect (16:9 for headers, as needed for diagrams), page (topic id or front/op1/op2) and placement (header or the H2 section it follows), prompt, alt (Finnish; for diagrams a full description that carries all the information), and for diagrams expected_labels (the exact Finnish strings that must appear) and facts_from (the topic and section the facts come from). Illustrations: one per topic (18), the front page, op1 and op2. Diagrams: about 6-8 as in the brief, each prompt asking for a clean flat infographic with exactly the listed Finnish labels, high contrast, a white background, no extra text. Facts only from stable rules in the topics; no yearly figures. Validate the YAML.`],
].map(([k, m, p]) => () => agent(p, { label: `prepare:${k}`, phase: 'Prepare', schema: REPORT, ...(m ? { model: m } : {}) }).then(r => r && ({ key: k, ...r }))))).filter(Boolean)

phase('Generate')
const RUNNER = `You run the image tool; you make no artistic choices. ${RF}
Run python tools/images.py --kind diagram --max-dollars ${MAX}, then python tools/images.py --kind illustration --max-dollars ${MAX} (klein, local; it may wait for the GPU lock: let it wait up to 30 minutes, then report). Read the printed plan before the paid run and stop if it would pass the cap. Then run the site build. Report what was made, refused or failed, and the dollars spent (from data/images.run.yaml).`
const gen = await agent(RUNNER, { label: 'generate', phase: 'Generate', model: 'haiku', schema: REPORT })

const CHECKS = {
  images: ['sonnet', `You are the image checker; you made none of these. ${RF} For every entry in data/images.yaml, open site-src/img/<id>.webp with Read and look at it. Diagrams: compare every visible label with expected_labels letter by letter (Finnish ä/ö included), list missing, extra or misspelled text, and check the facts against the topic section named in facts_from. Illustrations: no text or pseudo-text, no logos, no distorted hands or faces, consistent style with the others, inclusive and non-stereotyped, suitable for a school site. Each failure is a must_fix with image_id; owner 'prompt' unless the fault is in placement or code.`],
  browse: ['sonnet', `You are the browse checker; you wrote nothing. ${RF} Build and serve _site on a free port; with headless Chrome (the local Chrome executable --headless=new --virtual-time-budget=6000 --screenshot --window-size=1366,900 and 500,900) capture the front page, /op1/, three topics with diagrams and their lesson views, and print one lesson to PDF. Save to ${SHOTS}\\ and LOOK. Must-fix: images missing, stretched or overflowing, missing alt on diagrams, pictures that dominate the text, print layout broken by images. Stop the server.`],
  gates: ['haiku', `You are the gate checker; you wrote nothing. ${RF} Run the build (exit 0), ruff, pytest -q, line counts (none over 500), check every site-src/img/*.webp is under 200 KB, and grep _site for external resources. Also confirm no API key pattern (r8_, sk-, token=) and no local path (a Windows user folder) in data/images.run.yaml or anywhere tracked. Each failure is a must_fix with owner 'code'.`],
}
const runChecks = keys => parallel(keys.map(k => () => agent(CHECKS[k][1], { label: `check:${k}`, phase: 'Check', model: CHECKS[k][0], schema: CHECK }).then(r => r && ({ check: k, ...r }))))

phase('Check')
let checks = (await runChecks(Object.keys(CHECKS))).filter(Boolean)
const history = [{ round: 0, prep, gen, checks }]
let failing = checks.filter(c => !c.passed || c.must_fix.length)

for (let round = 1; round <= 2 && failing.length; round++) {
  phase('Redo')
  const items = failing.flatMap(c => c.must_fix.map(f => ({ check: c.check, ...f })))
  const promptItems = items.filter(i => i.owner === 'prompt')
  const codeItems = items.filter(i => i.owner !== 'prompt')
  log(`round ${round}: ${promptItems.length} prompt and ${codeItems.length} code items`)
  const fixes = (await parallel([
    promptItems.length && (() => agent(`You are the art director, round ${round}. ${RF} You own data/images.yaml. Revise the prompts (and alt texts if needed) of the failed pictures below so the faults cannot recur. ${round === 2 ? 'This is the last round: for any diagram that failed in round 1 too, set fallback: svg on its entry instead of a new prompt.' : ''} Then run python tools/images.py --redo <the failed ids> --max-dollars ${MAX} (diagrams with fallback: svg are skipped). Report the ids remade and dollars.\nItems: ${JSON.stringify(promptItems)}`, { label: `redo:prompts-${round}`, phase: 'Redo', schema: REPORT })),
    (codeItems.length || round === 2) && (() => agent(`You are the code fixer, round ${round}. ${RF} You own tools/, pipeline/, templates/, site-src/ (except img/) and tests/. Fix these items at the root. ${round === 2 ? 'Also: for every diagram in data/images.yaml with fallback: svg (the art director sets it this round), draw it as an accessible inline SVG with exactly its expected_labels (Finnish), add it to site-src/img/<id>.svg and make the build use the SVG.' : ''} Rebuild and rerun ruff and pytest.\nItems: ${JSON.stringify(codeItems)}`, { label: `redo:code-${round}`, phase: 'Redo', model: 'sonnet', schema: REPORT })),
  ].filter(Boolean))).filter(Boolean)
  const re = (await runChecks(failing.map(c => c.check))).filter(Boolean)
  checks = checks.map(c => re.find(r => r.check === c.check) || c)
  history.push({ round, fixes, recheck: re })
  failing = checks.filter(c => !c.passed || c.must_fix.length)
}
if (failing.length) log(`still failing: ${failing.map(c => c.check).join(', ')}; the judge will rule`)

phase('Judge')
const judgement = await agent(`You are the judge; you wrote nothing in this project. Rule from files only: ${ROOT}\\${BRIEF}, CLAUDE.md, data/images.yaml, data/images.run.yaml, site-src/img/, the code and the screenshots in ${SHOTS}\\ (look with Read; open at least all diagrams and six illustrations yourself). Run the build and tests yourself. Sum the dollars in data/images.run.yaml and compare with the €10 cap. Context to verify, not trust: ${JSON.stringify(history).slice(0, 40000)}
Rule on each Done-when line of the brief. Write ${ROOT}\\${JUDGEMENT} (under 150 lines): verdict, a table, the spend, remaining items, and at most 5 plain lines for the operator. Do not commit.`,
  { label: 'judge', phase: 'Judge', schema: { type: 'object', properties: { verdict: { type: 'string', enum: ['accept', 'accept-with-minors', 'reject'] }, dollars_spent: { type: 'number' }, operator_summary: { type: 'string' }, remaining: { type: 'array', items: { type: 'string' } } }, required: ['verdict', 'operator_summary', 'remaining'] } })

return { prep, gen, checks, rounds: history.length - 1, judgement }
