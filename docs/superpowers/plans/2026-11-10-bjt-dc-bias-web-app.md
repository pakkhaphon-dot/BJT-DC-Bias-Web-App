# BJT DC Bias Web App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Flask web app that computes the DC operating point of a voltage-divider-biased NPN common-emitter BJT from form input, with validation, region warnings, and automated tests.

**Architecture:** Server-rendered form POST. `dc_bias.py` holds all engineering math, validation, and region logic with no knowledge of HTTP/HTML. `app.py` routes `GET /` and `POST /calculate`, calls the engineering module, and renders `templates/index.html`. No JavaScript computation — every displayed number comes from Python.

**Tech Stack:** Python 3.15 (stdlib `unittest` for tests), Flask (only dependency), Jinja2 templates, one CSS file.

**Spec:** `docs/design-note.md` (approved 2026-11-10)

## Global Constraints

- Repo root: `C:\Users\b6828141\Documents\GitHub\BJT DC Bias Web App` (contains a space — always quote paths in shell commands)
- UI copy: English only (decision recorded in spec)
- Units: resistances entered in **kΩ**, converted to **Ω** before math; currents displayed in **mA**; voltages in **V**; every input label and result carries its unit
- No hardcoded DC results in templates or JavaScript — anti-goal in spec
- Forward-active model, fixed β and VBE; saturation threshold `VCE < 0.2 V`; cutoff check `VTH ≤ VBE`
- Test command (from repo root, stdlib only for Task 1): `python -m unittest discover -s tests -v`
- Flask dev server binds `127.0.0.1` only; never commit `.venv/`, `__pycache__/`, `.env`
- **Commits are made by the student via GitHub Desktop** (agent never runs `git commit`); each commit step below states the message to use
- Reference design case (spec): VCC=12 V, R1=100 kΩ, R2=22 kΩ, RC=2.2 kΩ, RE=1 kΩ, β=100, VBE=0.70 V

## Review Focus

Input classes the spec implies but task tests must pin down:

1. **Missing form field entirely** — `parse_inputs` must return a friendly error, not raise `KeyError`. Test in Task 1: empty dict → 7 errors, `params is None`.
2. **Empty or whitespace-only value** (`"  "`) — friendly error, not `ValueError` from `float()`. Test in Task 1.
3. **Non-finite numerics** (`"inf"`, `"nan"`, `"1e999"`) — `float()` accepts these; validation must reject via `math.isfinite`. Test in Task 1.
4. **Empty POST body** — `/calculate` with no fields renders the error page with HTTP 200, never a 500. Test in Task 2.
5. **Form keeps user input after POST** — repopulating fields proves values round-tripped through the server. Test in Task 2: response HTML contains `value="12"` for VCC.

---

### Task 1: Engineering core — `dc_bias.py` (math, validation, regions)

**Files:**
- Create: `dc_bias.py`
- Create: `tests/__init__.py` (empty)
- Test: `tests/test_dc_bias.py`

**Interfaces:**
- Consumes: nothing (stdlib only)
- Produces (Task 2 depends on these exact names):
  - `parse_inputs(form: Mapping[str, str]) -> tuple[dict[str, float] | None, list[str]]`
    - Expected keys: `vcc, r1, r2, rc, re, beta, vbe` (resistances in kΩ as strings)
    - Returns `(params, errors)`: on success `params` has keys `vcc_v, r1_ohms, r2_ohms, rc_ohms, re_ohms, beta, vbe_v`; on any error returns `(None, errors)` with English messages naming the field, e.g. `"R1: must be greater than zero."`
    - Validation: field present and non-blank after `strip()`; parses as `float`; finite (`math.isfinite`); `vcc, r1, r2, rc, re, beta` strictly `> 0`; `vbe` only numeric+finite (no sign rule — spec does not set one)
  - `solve_dc_bias(params: dict[str, float]) -> dict` with keys `vth_v, rth_ohms, ib_a, ic_a, ie_a, ve_v, vb_v, vc_v, vce_v, region, warnings`
    - `region`: `"Forward-Active"` / `"Cutoff"` / `"Saturation"`; `warnings`: `list[str]` (empty in Forward-Active)
    - Module constant `VCE_SAT_THRESHOLD_V = 0.2`
    - Equations (spec): `VTH = VCC·R2/(R1+R2)`, `RTH = R1·R2/(R1+R2)`, `IB = (VTH−VBE)/(RTH+(β+1)·RE)`, `IC = β·IB`, `IE = (β+1)·IB`, `VE = IE·RE`, `VB = VE+VBE`, `VC = VCC−IC·RC`, `VCE = VC−VE`
    - **Cutoff rule:** if `vth_v <= vbe_v` → report the off-state instead of negative currents: `ib=ic=ie=0`, `ve=0`, `vb=vth_v`, `vc=vcc_v`, `vce=vcc_v`, `region="Cutoff"`, warning that forward-active model does not apply
    - **Saturation rule:** otherwise compute all values; if `vce_v < VCE_SAT_THRESHOLD_V` → `region="Saturation"`, warning that the forward-active assumption fails and real VCE ≈ 0.2 V

- [ ] **Step 1: Write failing tests in `tests/test_dc_bias.py`** — `unittest.TestCase` with:

```python
# reference case (spec data) — expected values precomputed independently
def test_reference_design_case_forward_active(self):
    params, errors = parse_inputs({"vcc": "12", "r1": "100", "r2": "22",
                                    "rc": "2.2", "re": "1", "beta": "100", "vbe": "0.7"})
    self.assertIsNone(errors)
    r = solve_dc_bias(params)
    self.assertAlmostEqual(r["vth_v"], 2.163934, places=5)
    self.assertAlmostEqual(r["rth_ohms"], 18032.786885, delta=0.001)
    self.assertAlmostEqual(r["ic_a"], 1.229858e-3, delta=1e-8)
    self.assertAlmostEqual(r["ie_a"], 1.242157e-3, delta=1e-8)
    self.assertAlmostEqual(r["ve_v"], 1.242157, places=4)
    self.assertAlmostEqual(r["vb_v"], 1.942157, places=4)
    self.assertAlmostEqual(r["vc_v"], 9.294311, places=4)
    self.assertAlmostEqual(r["vce_v"], 8.052154, places=4)
    self.assertEqual(r["region"], "Forward-Active")
    self.assertEqual(r["warnings"], [])
```

  Plus these tests (same file, names + assertions):
  - `test_kohm_conversion`: `r1="100"` → `params["r1_ohms"] == 100000.0` (kΩ→Ω is the contract)
  - `test_cutoff_reports_off_state`: VCC=1, same resistors → `vth 0.180328 ≤ vbe 0.7` → region `"Cutoff"`, `ic_a == 0`, `vce_v == 1.0`, warnings non-empty
  - `test_saturation_warning`: RC=10 kΩ, rest reference values → `vce < 0.2` → region `"Saturation"`, warnings non-empty
  - `test_negative_resistor_rejected`: `r1="-5"` → `params is None`, some error mentions `"R1"`
  - `test_missing_field_rejected`: `{}` → `params is None`, `len(errors) == 7`
  - `test_blank_value_rejected`: `"  "` for vcc → `params is None`, error mentions `"VCC"`
  - `test_non_numeric_rejected`: `beta="hundred"` → `params is None`, error mentions `"beta"`
  - `test_non_finite_rejected`: `vbe="inf"` and separately `vcc="nan"` → `params is None`

- [ ] **Step 2: Run tests, verify they fail**

  Run: `python -m unittest discover -s tests -v` (repo root)
  Expected: `ModuleNotFoundError: No module named 'dc_bias'`

- [ ] **Step 3: Implement `dc_bias.py`** — `parse_inputs` and `solve_dc_bias` per the Interfaces block; a small `REQUIRED = (("vcc", "VCC", "vcc_v", 1.0, True), ...)`-style table keeps the seven rules in one loop (field name, label, output key, kΩ multiplier, must-be-positive flag)

- [ ] **Step 4: Run tests, verify all pass**

  Run: `python -m unittest discover -s tests -v`
  Expected: `OK` — all 9+ tests pass

- [ ] **Step 5: User commits via GitHub Desktop**

  Message: `Add dc_bias engineering module with validation, regions and unit tests`
  Files: `dc_bias.py`, `tests/__init__.py`, `tests/test_dc_bias.py`

---

### Task 2: Flask app — routes, template, CSS

**Files:**
- Create: `app.py`
- Create: `templates/index.html`
- Create: `static/style.css`
- Create: `tests/test_web.py`
- Create: `requirements.txt` (contents: `flask`)
- Create: `.gitignore` (`.venv/`, `__pycache__/`, `*.pyc`, `.env`)

**Interfaces:**
- Consumes: `dc_bias.parse_inputs(form) -> (params|None, errors)` and `dc_bias.solve_dc_bias(params) -> results dict` (exact keys from Task 1)
- Produces: running app at `http://127.0.0.1:5000/` with routes `GET /` and `POST /calculate`; template context: `defaults` (dict of submitted raw strings per field), `errors` (list[str]), `results` (dict or None), `warnings` (list[str])

- [ ] **Step 1: Set up venv and install Flask**

  Run: `python -m venv .venv` then `.venv\Scripts\python -m pip install flask`
  Expected: installs without error (`.venv` is git-ignored)

- [ ] **Step 2: Write failing web tests in `tests/test_web.py`** — `unittest.TestCase` using `app.app.test_client()`:

```python
def test_get_index_shows_form(self):
    rv = self.client.get("/")
    self.assertEqual(rv.status_code, 200)
    html = rv.get_data(as_text=True)
    self.assertIn("Calculate DC Bias", html)
    self.assertIn("VCC", html) and self.assertIn("kΩ", html)

def test_post_reference_case_shows_results(self):
    rv = self.client.post("/calculate", data={...reference values...})
    self.assertEqual(rv.status_code, 200)
    html = rv.get_data(as_text=True)
    self.assertIn("8.052", html)          # VCE [V], 3 dp
    self.assertIn("1.230", html)          # IC [mA], 3 dp
    self.assertIn("Forward-Active", html)
```

  Plus:
  - `test_post_invalid_shows_error_keeps_form`: `r1="-5"` → 200, error mentions `"R1"`, and `value="12"` still present (VCC kept) — page must not 500
  - `test_post_empty_body_shows_errors`: `data={}` → 200, at least one field error present
  - `test_post_cutoff_shows_warning`: VCC=1 case → 200, `"Cutoff"` in html and a warning string present
  - `test_results_are_not_hardcoded`: GET `/` contains no `"8.052"` (empty state has no result numbers)

- [ ] **Step 3: Run tests, verify they fail**

  Run: `.venv\Scripts\python -m unittest discover -s tests -v`
  Expected: `ModuleNotFoundError: No module named 'app'` (Task 1 tests still pass)

- [ ] **Step 4: Implement `app.py`** — `app = Flask(__name__)`; `GET /` renders the empty form; `POST /calculate` calls `parse_inputs(request.form)`, on `(None, errors)` re-renders with `defaults=request.form.to_dict()` and errors, else renders with `results = solve_dc_bias(params)` and `warnings=results["warnings"]` — both return HTTP 200

- [ ] **Step 5: Implement `templates/index.html` + `static/style.css`** — one page: intro line, form (7 labeled inputs with units, `method="POST" action="/calculate"`, `value="{{ defaults.get('<field>', '') }}"` to repopulate), error box (`{% for e in errors %}`), on results: table of VB/VE/VC/VCE in V and IC/IB/IE in mA formatted `%.3f` via Jinja, region badge, warning box; CSS keeps it clean and responsive — no pixel-perfect match to the lab mockup required

- [ ] **Step 6: Run all tests, verify pass**

  Run: `.venv\Scripts\python -m unittest discover -s tests -v`
  Expected: `OK` — Task 1 + Task 2 tests all pass

- [ ] **Step 7: Manual demo (student screenshots for Moodle)**

  Run: `.venv\Scripts\python -m flask --app app run --debug` → open `http://127.0.0.1:5000/`, try: reference values (success), `r1=-5` (error), VCC=1 (cutoff warning), RC=10 (saturation warning)

- [ ] **Step 8: User commits via GitHub Desktop**

  Message: `Add Flask app with routes, template, CSS and web tests`
  Files: `app.py`, `templates/index.html`, `static/style.css`, `tests/test_web.py`, `requirements.txt`, `.gitignore`

---

### Task 3: Documentation — README, AGENTS, validation, reflection

**Files:**
- Create: `README.md`
- Create: `AGENTS.md`
- Create: `docs/validation.md`
- Create: `docs/reflection.md`

**Interfaces:**
- Consumes: final behavior of Tasks 1–2 (commands, equations, reference values)
- Produces: docs required for Moodle submission (repo URL + SHA handed in separately by student)

- [ ] **Step 1: Write `README.md`** — project description, circuit and model assumptions (equations from spec), file structure, setup/run/test instructions exactly matching the commands used above (venv, `pip install -r requirements.txt`, `python -m flask --app app run --debug`, `http://127.0.0.1:5000/`, `python -m unittest discover -s tests -v`), input-unit note (kΩ), limitations of the forward-active model

- [ ] **Step 2: Write `AGENTS.md`** — conventions: English UI, all math in `dc_bias.py` only, no hardcoded results, TDD, student commits via GitHub Desktop

- [ ] **Step 3: Write `docs/validation.md`** — independent hand calculation for the reference case (the table of expected values from Task 1's test) alongside what the web page displays, satisfying acceptance criterion A3

- [ ] **Step 4: Draft `docs/reflection.md`** — answers to the lab's four questions (file:// vs running Flask; how the form reaches Python; whether changing `dc_bias.py` requires HTML changes; why out-of-region results need warnings) — student rewrites in their own words before submission

- [ ] **Step 5: Run full test suite one final time**

  Run: `.venv\Scripts\python -m unittest discover -s tests -v`
  Expected: `OK`

- [ ] **Step 6: User commits via GitHub Desktop**

  Message: `Add README, AGENTS conventions, validation and reflection docs`
  Files: `README.md`, `AGENTS.md`, `docs/validation.md`, `docs/reflection.md`
