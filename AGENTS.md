# AGENTS.md — Asset Label Generator

This file describes how AI agents (Claude Code) should work in this repository.

---

## Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable, working code only. Never commit directly except for initial scaffold and docs. |
| `phase-1/core-mvp` | Phase 1 implementation: reader, barcode gen, docx builder, CLI |
| `phase-2/polish` | Phase 2: input validation, dry-run, optional fields |
| `phase-3/enhancements` | Phase 3: QR codes, PDF output, GUI |

Each phase branch is created from `main`, developed, then merged back to `main` via a pull request (or direct merge once reviewed).

```
main
 └── phase-1/core-mvp   ← current active branch for Phase 1
      └── (merge to main when Phase 1 is complete)
 └── phase-2/polish     ← created from main after Phase 1 merges
```

---

## Starting a New Phase

```bash
git checkout main
git pull
git checkout -b phase-N/description
```

---

## Agent Boundaries — What Agents Must Never Do

Agents (Claude Code) must **never** run the following without an explicit instruction from the user:

- `git commit`, `git push`, `git merge`, `git rebase`, or any git command that changes history or remote state
- `git checkout`, `git switch`, or `git branch` to create or change branches
- Any shell command that installs packages, starts processes, or modifies files outside the project (e.g. `uv add`, `uv run`, `pip install`)
- Any destructive operation (deletes, resets, force-pushes)

The user runs all commands. Agents write code and files only. When a command is needed, state it in the reply so the user can run it themselves.

---

## Commit Style

- Short imperative subject line: `add barcode_gen module`, `fix column spacing for Avery 61523`
- Reference phase in the first commit: `phase 1: scaffold core modules`
- Commits must include the Co-Authored-By attribution line when made by Claude Code

---

## What Agents Should Know

- **Spec lives at** `docs/spec.md` — read it before starting any implementation work
- **Template target**: Avery 61523 (3/4" × 1-1/2", 40 labels/sheet, 4 col × 10 row)
- **Barcode type**: Code 39 (the `*serial*` asterisk format seen on the sample label photo)
- **Output format**: `.docx` via `python-docx`, not PDF (Phase 1)
- **Input**: CSV first, JSON second; both handled by `reader.py`
- **Dependencies**: managed with `uv`; add packages via `uv add <package>`
- **Venv**: `.venv` is already created; `uv run` activates it automatically
- **Output folder** `output/` is gitignored — never commit generated `.docx` files
- **Test print**: always note in PR description whether a test print was done on plain paper

---

## Phase Status

| Phase | Branch | Status |
|---|---|---|
| 1 — Core MVP | `phase-1/core-mvp` | Not started |
| 2 — Polish & Validation | `phase-2/polish` | Not started |
| 3 — Enhancements | `phase-3/enhancements` | Not started |
