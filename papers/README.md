# Papers

Each directory represents one paper and contains its reading notes, derivations,
experiment log, data provenance, results, and language-specific implementations.

```bash
uv run new-study 2017-attention-is-all-you-need \
  --kind paper \
  --languages python cpp typescript
```

Only request languages you will use. Add `.devcontainer/` when compiler, CUDA,
OS, or system libraries require stronger isolation.

For Codex setup, follow [the paper/study workflow](../docs/new-paper-workflow.md).
The user writes research code; prepare environments and source/data references only
unless implementation is explicitly requested. Large datasets may remain external links.
