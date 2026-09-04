# Notion and GitHub Workflow

Notion hub: [AI Research Lab](https://app.notion.com/p/3d169428c8618198a261c0f821b25f98)

## Source of truth

| Information | Source of truth |
| --- | --- |
| Paper metadata, summary, criticism, questions | Notion Papers |
| Definitions, prerequisites, mastery | Notion Concepts |
| Paper-to-paper relationship and explanation | Notion Connections |
| Implementation status and next action | Notion Implementations |
| Source code, tests, commands, configuration | GitHub |
| Metrics and reproducibility evidence | GitHub |
| Large datasets and checkpoints | External artifact storage; link from both |

## One paper cycle

1. Duplicate `TEMPLATE — Paper Note (duplicate me)` in Notion.
2. Fill metadata and change Status from Inbox to Reading.
3. Create or link Concept records while reading.
4. Add a Connection row whenever a paper relationship needs an explanation.
5. If implementation adds value, duplicate the Implementation template.
6. Run `uv run new-study <slug>`, enter the new directory, and run
   `uv sync --group dev` to create its independent environment.
7. Paste the Notion URL into its README, then commit the hypothesis,
   configuration, code, lock file, and result.
8. Paste the GitHub directory or commit URL into Notion.
9. Mark the implementation reproducible only after a clean rerun.

## Review discipline

A paper is Read when you can state the problem, contribution, evidence, and one
limitation without reopening it. A concept is Applied only after using it in
an implementation or analysis. A failed experiment still counts as useful work
when its configuration and interpretation are recorded.
