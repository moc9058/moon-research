# Repository instructions for coding agents

Read `README.md` and `docs/new-paper-workflow.md` before adding or updating a
paper, study, or nested assignment/experiment. Preserve existing projects and
unrelated user changes.

## Creation contract

- Run commands from repository root (or explicitly select the root).
- `uv run new-study <relative-path>` targets studies; `uv run new-paper
  <relative-path>` targets papers. Never use the removed `--kind` flag.
- Default to documentation containers: README.md, docs/README.md, docs/notes.md.
  Do not create language manifests or environments at course/group levels.
- For an executable node use `--generate --languages <needed languages>`.
  Nested paths such as course/assignment-1 are supported at any depth.
  Generation writes configuration only. Install/build inside that node's
  implementations/<language>/, never from a documentation-only ancestor.
- A new language may be added to an existing node with --generate. Existing
  language directories must be edited in place; never overwrite user work.
- Each executable language owns its manifest, lockfile, and local environment.
  No uv/npm workspace or shared research dependencies at repository root.
- Keep README/docs at every logical hierarchy level and language project.
  Add relative child links to parent READMEs, preserving existing content.
  Record scope, status, sources, environment ownership, and next steps.
  Shared notes live at parents; child-specific notes live at children.
  Add derivations and experiment logs when relevant; do not invent results.
- Root src/moon_research and tests are generator tooling. Keep research code
  and its tests in the relevant implementation. Do not add vacuous tests.
- Templates: papers/_template and studies/_template mirror the generated
  documentation contract. Update templates when changing that contract.


Default to environment setup only. The user writes research code. Prepare
manifests, lockfiles, configuration, source/data references, and environment
checks, but do not implement or modify models, algorithms, research preprocessing,
training/evaluation loops, or experimental changes unless explicitly requested.
Generator placeholders are scaffolding, not a completed implementation or a
successful reproduction.

Keep upstream source and the user's implementation separate. Record source
URLs, exact revisions, licenses, dataset versions/splits, and working directories
for commands. Prefer external dataset/checkpoint links; do not bulk-download
artifacts or start long training unless requested. Respect authorization already
given in the current task.

Never commit credentials, private keys, account IDs, instance IDs, generated
state, datasets, checkpoints, or secrets. Run the documented checks before
committing and report unavailable checks honestly.
