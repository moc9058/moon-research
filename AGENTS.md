# Repository instructions for coding agents

Read `README.md` and `docs/new-paper-workflow.md` before adding or updating a
paper or study. Use `uv run new-study` for a new target only; preserve existing
projects and unrelated user changes.

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
