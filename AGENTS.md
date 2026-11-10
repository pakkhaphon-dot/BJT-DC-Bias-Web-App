# AI coding conventions — BJT DC Bias Web App

Repo: `BJT DC Bias Web App` (ENG29 2121 Lab 02)

## General

- UI copy: **English only** (decision recorded in `docs/design-note.md`)
- Units: resistances are entered in **kΩ** and converted to **Ω** before calculation; currents displayed in **mA**, voltages in **V**; every label and result carries its unit
- No hardcoded DC results in templates, CSS or JavaScript — every number comes from `dc_bias.py`
- All engineering logic lives in `dc_bias.py`, which knows nothing about Flask, HTTP or HTML
- `app.py` handles only routing, form parsing and template rendering

## Development workflow

- Tests first (TDD): write the failing test, watch it fail, write minimal code, run until green
- Full suite: `.venv\Scripts\python -m unittest discover -s tests -v` from the repo root
- Dev server: `python -m flask --app app run --debug` → `http://127.0.0.1:5000/`
- Commit style: short imperative summary, e.g. `Add dc_bias engineering module with validation`
- Commits are made by the student via **GitHub Desktop** — review the diff in the Changes tab before every commit

## Files never to commit

`.venv/`, `__pycache__/`, `*.pyc`, `.env`, `*.egg-info/`, `.DS_Store` (covered by `.gitignore`)

## Submission

Submit the GitHub repository URL and the latest commit SHA via Moodle, together with a screenshot of the running web app and the test log.
