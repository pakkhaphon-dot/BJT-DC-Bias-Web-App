"""Flask application for the BJT DC Bias web app (ENG29 2121 Lab 02).

Routes:
    GET  /       show the input form
    POST /calculate  compute the DC operating point and render results

All engineering math lives in dc_bias.py; this module knows only HTTP,
templates, and how to glue them together.
"""

from flask import Flask, render_template, request

from dc_bias import parse_inputs, solve_dc_bias

app = Flask(__name__)

FIELDS = ("vcc", "r1", "r2", "rc", "re", "beta", "vbe")


@app.route("/")
def index():
    return render_template("index.html", defaults={}, errors=[], results=None, warnings=[])


@app.route("/calculate", methods=["POST"])
def calculate():
    params, errors = parse_inputs(request.form)
    if errors:
        return (
            render_template(
                "index.html",
                defaults=request.form.to_dict(),
                errors=errors,
                results=None,
                warnings=[],
            ),
            200,
        )

    results = solve_dc_bias(params)
    return (
        render_template(
            "index.html",
            defaults=request.form.to_dict(),
            errors=[],
            results=results,
            warnings=results["warnings"],
        ),
        200,
    )
