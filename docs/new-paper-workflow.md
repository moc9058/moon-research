# Paper and study setup workflow

This is the canonical procedure for Codex and humans working in `papers/` and
`studies/`. The filename is retained for existing links. By default, Codex
prepares the environment and documentation; the user writes research code.

## Inputs and defaults

| Input | Example | If omitted |
| --- | --- | --- |
| Kind/source | Paper PDF or URL; study topic or tutorial | Infer kind from the task; a study needs no paper |
| Slug | `2017-attention-is-all-you-need`, `seq2seq-attention` | Infer; avoid overwriting an existing target |
| Goal | Upstream reproduction, own implementation, modification | Environment setup for user implementation |
| Languages | `python`, `cpp` | Python |
| Runtime | WSL/Linux, Python version, CPU or GPU | Inspect available environment; do not assume it matches the user's PC |
| Upstream code | Repository URL plus commit/tag | Look for an official repository when relevant; label alternatives |
| Data | Dataset URL, version/split, existing local path | Record references; leave data undownloaded |
| Reproduction target | Table/figure/metric and acceptable difference | TODO; do not invent a scientific success criterion |
| Resource limit | Download limit, smoke-run time, GPU availability | Small setup checks only; no bulk downloads or long runs |

Use known information and resolve routine choices without repeated questions.
Ask only when a missing detail materially changes the setup. Missing metadata,
inaccessible sources, and unverified commands must be labeled explicitly.

## Scope and ownership

Codex may create directories, manifests, lockfiles, config files, setup scripts,
empty source folders, TODO placeholders, and small import/build checks. It may
inspect existing code to identify dependencies and explain where to begin.

The user owns model/algorithm code, training and evaluation logic, research
preprocessing, and modifications used to test a hypothesis. Do not fill these in,
refactor existing research code, or design a solution in advance unless asked.
When asked to review a change, provide findings first; edit only within the
requested scope. A request for code or a specific fix overrides setup-only
behavior for that task.

## Create or update

Run from the repository root:

```bash
uv sync --locked --group dev

# A single paper
uv run new-study <year-short-title> --kind paper --languages python

# A topic or exercise
uv run new-study <topic-slug> --kind study --languages python
```

For an existing target, inspect it and update only missing setup/documentation;
do not rerun the generator over it. Keep user code under
`implementations/<language>/`. Populate the generated README and supporting
files using this workflow; the generator supplies only a minimal skeleton.
Its placeholder tests and TODO programs are not evidence of research correctness.

## Dependencies and runtime

- Inspect upstream manifests and documented runtime requirements before choosing
  versions. Pin a compatible language version and framework stack, including
  CPU/GPU variants when relevant. Do not install GPU drivers as routine setup.
- Keep each paper/study language environment independent. No root-wide research
  dependencies or shared virtual environment for all projects.
- Python: in `implementations/python/`, update `pyproject.toml` and
  `.python-version`, run `uv lock`, then `uv sync --locked --group dev`.
- TypeScript: in `implementations/typescript/`, run
  `npm install --package-lock-only`, then `npm ci`.
- C/C++: in its implementation directory, validate CMake presets, configure,
  build, and run CTest if tools are available.
- Record native libraries and hardware requirements in the implementation README.
  Avoid speculative dependencies. If dependency installation or GPU validation
  is unavailable, provide exact commands and mark those steps unverified.

## Upstream source and baseline

For reproduction, first distinguish running the authors' code from independently
implementing their method. Record in the project README:

- Paper/tutorial and upstream code URLs; whether the code is official.
- Exact upstream commit (preferred) or release tag, license, and environment.
- Original entry point, configuration, checkpoint reference, and dataset split.
- Target result and any known deviations in hardware, data, budget, or version.

By default link to upstream code. If a checkout is needed, use a separate path
outside this repository, such as a sibling `moon-research-upstream/` directory,
and document the resolved commit and working directory. Keep its dependencies
separate when they conflict with the user's implementation. Do not copy upstream
code into the user's source tree or add a nested Git repository by accident.
Vendoring or adding a submodule requires a specific request and license review.

Record the unmodified baseline in `docs/experiments.md` before comparing a user's
change. If no baseline has run, write **not run**, not a fabricated score.
An environment smoke check, a small-scale reproduction, and a full-paper
reproduction must be labeled separately.

## Data and large artifacts

A link-only `data/README.md` is valid and is the default for large data. Record:

| Field | What to record |
| --- | --- |
| Identity | Dataset name, stable source URL/DOI, version or release |
| Access | License, registration or manual approval requirements |
| Scope | Subset, train/validation/test split, approximate size if known |
| Integrity | Published checksum or verification method if available |
| Local use | Expected local path, file layout, and config/environment variable |
| Preparation | Authors' preprocessing instructions and unresolved user tasks |
| Availability | External reference only, already present, or verified downloaded |

Prefer stable landing pages over expiring or signed URLs. Store secrets in local
ignored files, not in committed URLs or scripts. An external local path is fine;
record how the user's future code should consume it rather than implementing a
loader for them. Do not invent checksums or claim a download has been verified.

Do not download full datasets/checkpoints during setup unless requested. A tiny
synthetic fixture can check plumbing if needed, but cannot validate paper metrics.
Keep downloaded data and checkpoints out of Git. `data/README.md` and
`results/README.md` are tracked; other files in those directories are ignored by
default. Use `results/README.md` for artifact links and `docs/experiments.md` for
small textual results. Add an exact allowlist exception only when a small metrics
file should actually be versioned.

## Experiment record

Prepare this structure in `docs/experiments.md`; fill only observed results:

- Experiment ID/date and status (planned, smoke-tested, completed, failed).
- Question/hypothesis and reproduction target.
- Upstream commit, user-code commit, and whether local changes were present.
- Dataset version, split, preprocessing, and checkpoint reference.
- Working directory, exact command, config, seed, and dependency lockfile.
- Hardware, resource budget, and actual runtime when measured.
- Baseline versus modified condition; change one factor at a time when feasible.
- Metrics, uncertainty/repeated seeds when relevant, logs and artifact links.
- Deviations, failure notes, and interpretation; never infer success from exit 0.

For a modification experiment, keep the baseline configuration/result available.
Codex prepares the comparison plan and records; the user writes the modification.

## Verification and handoff

From the repository root, before committing:

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run pytest
git diff --check
```

Run relevant environment checks for initialized language projects. Do not start
long training or provision infrastructure as part of setup. Respect run/download
limits already provided by the user. Separate verified results from commands
that must be run on the user's machine or with unavailable data/hardware.

Report the target path, changed files, environment versions, source revision,
data status, checks and limitations, and exact next commands with working
directories. State which file the user should write first and what remains TODO.
If asked to commit/push, check the diff for artifacts/secrets and unrelated edits.

## Copyable requests (Korean)

### New paper: prepare reproduction

> moon-research의 README.md와 AGENTS.md에 따라 [논문 URL]을 papers에 추가해줘.
> 목표는 [표/그림/지표]의 재현 준비야. 공식 코드는 [URL 또는 찾아줘], 데이터는
> [URL 또는 찾아줘]이고, 실행 환경은 [WSL/Linux, CPU/GPU]야.
> 연구 코드는 내가 작성할 테니 환경·의존성·원본 코드 참조·데이터 경로·실험
> 기록 양식만 준비해줘. 대용량 데이터는 외부 링크로 기록하고 다운로드하지 마.
> 원본 코드로 실행할 절차와 내 구현으로 실험할 절차를 구분하고, 확인한 사항과
> 아직 실행하지 않은 사항, 내가 처음 작성할 파일을 알려줘. 변경을 커밋하고 push해줘.

### New study: prepare an implementation exercise

> moon-research의 저장소 지침에 따라 [주제]를 studies에 추가해줘.
> [언어]로 [학습 목표]를 직접 구현할 거야. 참고 자료는 [URL/없음]이고 실행
> 환경은 [환경]이야. 필요한 환경·문서·설정과 최소 환경 점검만 준비하고,
> 알고리즘이나 학습 코드는 작성하지 마. 변경을 커밋하고 push해줘.

### Existing project: prepare a modification experiment

> [papers/studies 경로]에서 [기준 실험]과 [변경 가설]을 비교하려고 해.
> 코드는 내가 수정할 테니 기존 코드 변경 없이 기준 설정·평가 지표·데이터
> split·seed·실험 기록 양식과 실행 명령을 정리해줘. 아직 실행하지 않은 결과는
> 미실행으로 표시하고, 지금은 학습을 실행하지 마.

### Review code I wrote

> [경로 또는 diff]에서 내가 작성한 코드를 [논문 식/원본 동작/가설]과 비교해줘.
> 먼저 논리 오류·텐서 차원·데이터 누수·재현성 문제와 검증 방법을 설명해줘.
> 코드는 직접 수정하지 말고, 내가 고칠 위치와 이유를 알려줘.
