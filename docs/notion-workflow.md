# Notion and GitHub Workflow

Notion hub: [moon-research](https://app.notion.com/p/3d169428c8618198a261c0f821b25f98)

## Source of truth

| Information | Source of truth |
| --- | --- |
| Citation metadata, summary, criticism, and questions | Notion Articles |
| Article-to-article relationship, rationale, and evidence | Notion Links |
| Source code, tests, commands, and configuration | GitHub |
| Metrics and reproducibility evidence | GitHub |
| Large datasets and checkpoints | External artifact storage; link from both |

## Graph model

An **Article** is a node. A **Link** is a directed edge:

```text
From Article --Relation--> To Article
```

Every Link must include a short **Why**. Add an **Evidence** locator such as a
section, figure, experiment, or quoted-claim location after verifying the edge.
Use Topics only for broad filtering; use Links for claims about relationships.

## One article cycle

1. Capture the title and Source URL in Articles with Status `Inbox`.
2. Duplicate `TEMPLATE — Article note (duplicate me)` and fill the citation
   properties.
3. Change Status to `Reading`; complete the summary, discussion, limitations,
   and questions inside the page.
4. Write a one-sentence Takeaway.
5. Add one Link row for every meaningful relationship to an existing Article.
6. If coding improves understanding, run `uv run new-study <slug>`, enter the
   new directory, and run `uv sync --group dev`.
7. Commit the hypothesis, configuration, code, lock file, result, and Notion URL.
8. Paste the GitHub directory or commit into the Article's `GitHub URL`.
9. Set Status to `Processed` only after a clean review.

## Link vocabulary

| Relation | Direction |
| --- | --- |
| Builds on | A directly depends on an idea introduced by B |
| Extends | A generalizes or adds capability to B |
| Supports | A provides evidence consistent with B |
| Contradicts | A provides evidence or claims against B |
| Alternative to | A addresses a similar problem using a different approach |
| Uses method from | A reuses a method from B |
| Same dataset | A and B evaluate on the same dataset; direction is arbitrary |

## Review discipline

An Article is Processed when you can explain its problem, method, evidence, and
conclusion without reopening it; identify at least one limitation or open
question; and represent its important relationships as explained Links. A
failed experiment still counts when its configuration and interpretation are
recorded reproducibly.
