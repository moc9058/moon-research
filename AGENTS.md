# Repository instructions for coding agents

Read `README.md` and `docs/new-paper-workflow.md` before adding a paper.
Use `uv run new-study` to create the canonical layout. Default paper compute
to `shared`; use `dedicated` only for a documented technical reason.

Creating or editing infrastructure files does not authorize AWS deployment.
Never commit credentials, private keys, account IDs, instance IDs, generated
state, datasets, checkpoints, or secrets. Preserve unrelated user changes and
run the documented checks before committing.
