# Papers

Run from repository root:

```bash
uv run new-paper <name>
uv run new-paper <name>/experiment-1 --generate --languages python
```

Default: README/docs only. Use --generate for isolated language configuration;
install dependencies inside implementations/<language>. Every nested node has
its own documentation. See [repository README](../README.md) and
[setup workflow](../docs/new-paper-workflow.md).
