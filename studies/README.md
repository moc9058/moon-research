# Studies

Run from repository root:

```bash
uv run new-study <name>
uv run new-study <name>/experiment-1 --generate --languages python
```

Default: README/docs only. Use --generate for isolated language configuration;
install dependencies inside implementations/<language>. Every nested node has
its own documentation. See [repository README](../README.md) and
[setup workflow](../docs/new-paper-workflow.md).
