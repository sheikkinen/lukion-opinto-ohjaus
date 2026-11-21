# 003: Enliven the site with diagrams and illustrations

**Written before the work.** Producer's brief, 2026-11-21. Runs after brief 002 is accepted. Built by
`.claude/workflows/images.js`.

## Why

The operator [O]: "check image related tools on game-engine; budget grant: €10. Operators recommendation:
nano-banana for graphs and images needing specifics. klein or pimage for generic images. option: enliven the site
with graphs and images." Recorded as D-007.

**Serves:** G-1. **Goal type:** look; the operator's eye on the finished pages decides. **Chain:** brief 3 on G-1.
**Models:** art director Opus (the image plan, prompts and alt texts); tool builder Sonnet; the generation run a
script (no model); image checker Sonnet (vision); browse checker Sonnet; gates Haiku; judge Opus.

What stands [A, read in game-engine, which is used read-only as a library]:
- `tools/pimage/models.py`: the adapters `nano-banana` (`google/nano-banana-2.1` on Replicate, $0.0336 a picture, no
  seed, 1K PNG), `p-image` ($0.005), `klein` (FLUX.2 klein 4B on the local ComfyUI, free, about 18 s a picture warm),
  `sdxl` (local, free). Each adapter builds the model's input from `(prompt, seed, aspect, image)`.
- `tools/pimage/clients.py`: `make_api(host_path, repo, replicate_factory)` gives a router with `run` and
  `run_many`. klein starts ComfyUI itself and takes game-engine's GPU lock (`gpu_lock.py`) before the first local
  picture, so it never runs beside another GPU job.
- `tools/pimage/replicate_client.py`: `read_token()` reads the Replicate key from the environment or game-engine's
  `.env`, and never prints it. `ReplicateClient.run_many` posts in parallel and handles 429s.
- `tools/pimage/budget.py` caps the dollars of a run. The `pimage.py` command itself is shaped for book characters
  and places, so this project calls the modules, not the command.

## The effect [M]

- **Diagrams with exact content on nano-banana** (operator's recommendation), about 6–8: the five tests of the
  ylioppilastutkinto and how they are chosen; the three parts of the HOPS; a three-year guidance timeline (marked as
  an example); the routes after lukio, all equal; the joint application step by step; the three-step self-study loop
  (read → do → reflect). Every label is in Finnish. The same information is always in the page text too, and the
  image has a full Finnish alt text. A diagram whose Finnish text is wrong after two tries is drawn as SVG by code
  instead.
- **Generic illustrations on klein** (free, local): one calm, consistent illustration per topic (18), the front page
  and the two module pages. No text in the picture, students of varied backgrounds and genders, no logos, no real
  people, no school uniforms. One style line for all of them.
- Images are WebP, under 200 KB each, self-hosted, with `loading="lazy"`, width and height set, and decorative ones
  marked `alt=""`. The site still makes no external requests.

## The work

1. **In parallel:**
   - *Tool* (Sonnet): `tools/images.py` reads `data/images.yaml` and makes each picture with game-engine's pimage
     modules (imported from `C:\src\game-engine\tools\pimage`, read-only), with the model named per picture. It
     writes `site-src/img/<id>.webp` and `data/images.run.yaml` (model, prompt, seed, sha256, dollars, date). It
     takes `--only <ids>`, `--redo <ids>` and `--max-dollars` (default 10). The planned calls and cost are printed
     first, and a run stops before it would pass the cap. It never prints the key. Tests have no network. The build
     places images and alt texts from the manifest.
   - *Art director* (Opus): `data/images.yaml` holds the style line, and per picture: id, kind (`diagram` |
     `illustration`), model (`nano-banana` | `klein`), aspect, prompt, the Finnish alt text, the exact expected
     labels (for diagrams) and the page it goes on. Diagram facts come from the topics' stable rules, never from
     yearly figures.
2. **Generate:** run the tool (a script), the diagrams first.
3. **Check, by agents that wrote nothing:** an image checker looks at every picture at page size. It compares
   diagram labels with the expected labels letter by letter and checks the facts against the topic text, the style
   and consistency, artefacts (hands, faces, garbled text in illustrations), inclusiveness, and that no illustration
   holds text. A browse checker looks at the pages, alt texts, sizes and print view. Gates run the build, tests,
   sizes and the no-external-requests check.
4. **Redo,** at most two rounds: the art director revises the prompts for failed pictures and the tool remakes only
   those. A diagram that fails twice becomes an SVG drawn by the code fixer.
5. **Judge,** then the producer commits.

## Limits

- **Money:** at most €10 (D-007). The tool's cap is $10 a run, and the whole brief stops at €10 spent. Expected
  spend: under $2 (about 8 diagrams × up to 3 tries × $0.0336, illustrations free).
- **game-engine:** read-only. Nothing is written or committed there. Its GPU lock is respected, and ComfyUI is
  started only by its own client.
- No API key, prompt log with a key, or local path is committed. `data/images.run.yaml` records models and prompts
  only.

## Done when

The operator sees a calm illustration at the top of every topic and on the front and module pages, and clear Finnish
diagrams where they help: the matriculation exam, the HOPS, the timeline, the routes, the application and the
self-study loop. Every label is spelled right and matches the text. Internally: the checks pass, the spend is
recorded and under €10, and the judge accepts.
