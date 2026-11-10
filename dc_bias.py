"""Engineering calculations for a voltage-divider-biased NPN common-emitter BJT.

ENG29 2121 Lab 02 — DC operating point under the forward-active
approximation (constant beta, constant VBE).

This module knows nothing about HTTP, Flask, or HTML: it takes plain
numbers and returns plain numbers so it can be unit-tested alone.
"""

import math

# (field, label, output key, multiplier, must_be_positive)
# Resistances arrive from the web form in kOhm and are stored in Ohm.
REQUIRED_FIELDS = (
    ("vcc", "VCC", "vcc_v", 1.0, True),
    ("r1", "R1", "r1_ohms", 1000.0, True),
    ("r2", "R2", "r2_ohms", 1000.0, True),
    ("rc", "RC", "rc_ohms", 1000.0, True),
    ("re", "RE", "re_ohms", 1000.0, True),
    ("beta", "beta", "beta", 1.0, True),
    ("vbe", "VBE", "vbe_v", 1.0, False),
)

# Below this collector-emitter voltage a silicon BJT is considered saturated.
VCE_SAT_THRESHOLD_V = 0.2


def parse_inputs(form):
    """Validate the raw web form and convert it to SI units.

    ``form`` maps field names (vcc, r1, r2, rc, re, beta, vbe) to raw
    strings; resistances are in kOhm.

    Returns ``(params, None)`` on success, where ``params`` maps output
    keys (vcc_v, r1_ohms, ..., beta, vbe_v) to floats in SI units, or
    ``(None, errors)`` where ``errors`` is a list of English messages,
    each naming the offending field.
    """
    params = {}
    errors = []
    for field, label, key, multiplier, must_be_positive in REQUIRED_FIELDS:
        raw = form.get(field)
        if raw is None or not str(raw).strip():
            errors.append(f"{label}: value is required.")
            continue
        try:
            value = float(str(raw).strip())
        except ValueError:
            errors.append(f"{label}: must be a number.")
            continue
        if not math.isfinite(value):
            errors.append(f"{label}: must be a finite number.")
            continue
        if must_be_positive and value <= 0.0:
            errors.append(f"{label}: must be greater than zero.")
            continue
        params[key] = value * multiplier
    if errors:
        return None, errors
    return params, None


def solve_dc_bias(params):
    """Compute the DC operating point from SI-unit parameters.

    ``params`` is the dict returned by :func:`parse_inputs`. Returns a
    dict with the Thevenin equivalents, branch currents, node voltages,
    the operating region ("Forward-Active", "Cutoff" or "Saturation") and
    a list of model-limitation warnings.

    Forward-active equations (constant beta, constant VBE):

        VTH = VCC * R2 / (R1 + R2)
        RTH = R1 * R2 / (R1 + R2)
        IB  = (VTH - VBE) / (RTH + (beta + 1) * RE)
        IC  = beta * IB          IE = (beta + 1) * IB
        VE  = IE * RE             VB = VE + VBE
        VC  = VCC - IC * RC       VCE = VC - VE

    When VTH <= VBE the transistor is cut off: instead of reporting the
    negative currents the model would produce, the off-state is reported
    (no currents, VE = 0 V, VC = VCC) with a warning.
    """
    vcc = params["vcc_v"]
    r1 = params["r1_ohms"]
    r2 = params["r2_ohms"]
    rc = params["rc_ohms"]
    re = params["re_ohms"]
    beta = params["beta"]
    vbe = params["vbe_v"]

    vth = vcc * r2 / (r1 + r2)
    rth = r1 * r2 / (r1 + r2)

    warnings = []

    if vth <= vbe:
        return {
            "vth_v": vth,
            "rth_ohms": rth,
            "ib_a": 0.0,
            "ic_a": 0.0,
            "ie_a": 0.0,
            "ve_v": 0.0,
            "vb_v": vth,
            "vc_v": vcc,
            "vce_v": vcc,
            "region": "Cutoff",
            "warnings": [
                "VTH <= VBE: the base-emitter junction is not forward-biased, "
                "the transistor is cut off and the forward-active model does "
                "not apply to this circuit."
            ],
        }

    ib = (vth - vbe) / (rth + (beta + 1.0) * re)
    ic = beta * ib
    ie = (beta + 1.0) * ib
    ve = ie * re
    vb = ve + vbe
    vc = vcc - ic * rc
    vce = vc - ve

    if vce < VCE_SAT_THRESHOLD_V:
        region = "Saturation"
        warnings.append(
            f"VCE = {vce:.3f} V is below {VCE_SAT_THRESHOLD_V:.1f} V: the "
            "transistor is saturated, the forward-active assumption fails "
            "and the real VCE is approximately 0.2 V."
        )
    else:
        region = "Forward-Active"

    return {
        "vth_v": vth,
        "rth_ohms": rth,
        "ib_a": ib,
        "ic_a": ic,
        "ie_a": ie,
        "ve_v": ve,
        "vb_v": vb,
        "vc_v": vc,
        "vce_v": vce,
        "region": region,
        "warnings": warnings,
    }
