# Papers

Each directory represents one paper and contains its reading notes, derivations,
experiment log, data provenance, results, and language-specific implementations.

```bash
uv run new-study 2017-attention-is-all-you-need \
  --kind paper \
  --languages python cpp typescript \
  --compute shared
```

Only request languages you will use. Add `.devcontainer/` when compiler, CUDA,
OS, or system libraries require stronger isolation.

Use the shared AWS VM by default. Select `--compute dedicated` when a paper
needs its own VM or network topology; this creates a paper-level infrastructure
contract without deploying anything.
