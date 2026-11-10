# Reflection — Lab 02 BJT DC Bias Web App

ENG29 2121 · 2/2569

Draft answers to the four questions in the lab handout (section 10). Rewrite in your own words before submitting via Moodle.

## 1. Why is opening `templates/index.html` directly not the same as running Flask?

Opening `index.html` with `file://` only shows the static page — the form cannot send data anywhere, and no Python code runs. Flask runs a local HTTP server (`http://127.0.0.1:5000/`): when you submit the form, the browser sends an HTTP POST to `/calculate`, Flask calls `dc_bias.py` to compute VB, VE, VC, VCE and IC from your inputs, then renders the result back into the HTML. Without the server there is no backend calculation at all.

## 2. How does the form send data to Python?

The form uses `<form method="POST" action="/calculate">`. On submit the browser sends an HTTP POST request to `/calculate` carrying each `<input name="...">` value as form data. Flask's `request.form` receives those values, `app.py` passes them to `parse_inputs()` in `dc_bias.py`, which validates and converts them to SI units, then `solve_dc_bias()` computes the operating point and the result is rendered back into `templates/index.html`.

## 3. If you change the equation in `dc_bias.py`, do you need to change `index.html`?

No — not unless you also want to change what is shown or how inputs are labeled. `dc_bias.py` knows nothing about HTML or HTTP, and `index.html` knows nothing about the equations; they only agree on the keys passed between them (`vcc_v`, `ic_a`, `region`, etc.). Changing the math is a change in `dc_bias.py` only; changing labels, units or layout is a change in the template and CSS only.

## 4. Why must results outside the valid region carry a warning instead of being reported as accurate?

The Forward-Active approximation assumes constant β and constant VBE and only holds when the transistor is actually forward-active (VTH > VBE and VCE well above ~0.2 V). In cutoff the base-emitter junction is not conducting, so the model's negative currents are physically meaningless; in saturation VCE collapses to about 0.2 V and the formula badly overestimates it. Reporting such numbers without a warning would pretend the approximation still applies. The app therefore reports the off-state values for cutoff and attaches a "Saturation" warning explaining that the real VCE is approximately 0.2 V.
