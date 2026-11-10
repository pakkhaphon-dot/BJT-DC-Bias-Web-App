# BJT DC Bias Web App

ENG29 2121 · Lab 02 — First DC Bias Web App (2/2569)

A Flask web application that computes the **DC operating point** of a voltage-divider-biased NPN common-emitter BJT. Enter component values in the browser; the Python backend calculates VB, VE, VC, VCE, IC, IB and IE, with input validation and forward-active-region warnings.

## What it does

- Accepts `VCC, R1, R2, RC, RE, β, VBE` from an HTML form (resistances entered in **kΩ**)
- Computes the DC operating point entirely in Python (`dc_bias.py` — no numbers are hardcoded in HTML or JavaScript)
- Displays results with units and flags two model limitations:
  - **Cutoff** when `VTH ≤ VBE`
  - **Saturation** when `VCE < 0.2 V`
- Validates missing, blank, non-numeric, non-finite and non-positive inputs with clear English messages

## Circuit model

Voltage-divider bias, forward-active approximation (constant β, constant VBE):

```
VTH = VCC · R2 / (R1 + R2)       RTH = R1 · R2 / (R1 + R2)
IB  = (VTH − VBE) / (RTH + (β+1) · RE)
IC  = β · IB                     IE = (β+1) · IB
VE  = IE · RE                    VB = VE + VBE
VC  = VCC − IC · RC              VCE = VC − VE
```

Reference case from the lab handout: `VCC=12 V, R1=100 kΩ, R2=22 kΩ, RC=2.2 kΩ, RE=1 kΩ, β=100, VBE=0.70 V` → `VB≈1.942 V, VE≈1.242 V, VC≈9.294 V, VCE≈8.052 V, IC≈1.230 mA`, region **Forward-Active**.

## Repository layout

```
app.py                  # Flask routes: GET /, POST /calculate
dc_bias.py              # engineering math, validation, region checks (stdlib only)
templates/index.html    # input form + results (Jinja2, English UI)
static/style.css        # page styling
tests/
  test_dc_bias.py       # unit tests for engineering math
  test_web.py           # Flask test-client tests for routes
requirements.txt        # flask
.gitignore              # .venv, __pycache__, .env, etc.
README.md               # this file
AGENTS.md               # AI coding conventions for this repo
docs/
  design-note.md        # approved design specification
  validation.md         # independent hand calculation of the reference case
  reflection.md         # answers to the lab's four review questions
```

## Setup and run

```powershell
# 1. Create and activate a virtual environment (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Install dependencies
python -m pip install -r requirements.txt

# 3. Run the development server
python -m flask --app app run --debug

# 4. Open http://127.0.0.1:5000/ in your browser

# 5. Run the test suite
python -m unittest discover -s tests -v
```

The Flask debug server is for local development only (`127.0.0.1`); never expose it on a public network and never commit `.venv/`, `.env`, or API keys.

## Model limitations

This is a hand-calculation approximation, not a SPICE solver. Results outside the forward-active region are flagged with warnings rather than presented as trustworthy values. AC analysis, Bode plots, transient simulation and other bias topologies are intentionally out of scope for this lab (added in later weeks).
