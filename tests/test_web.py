"""Flask route tests for the BJT DC Bias web app (ENG29 2121 Lab 02).

All tests run through Flask's built-in test client — no network, no
debug server required.
"""

import unittest

from app import app


class WebAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_index_shows_form(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
        html = rv.get_data(as_text=True)
        self.assertIn("Calculate DC Bias", html)
        self.assertIn("VCC", html)
        self.assertIn("kΩ", html)

    def test_post_reference_case_shows_results(self):
        rv = self.client.post(
            "/calculate",
            data={
                "vcc": "12",
                "r1": "100",
                "r2": "22",
                "rc": "2.2",
                "re": "1",
                "beta": "100",
                "vbe": "0.7",
            },
        )
        self.assertEqual(rv.status_code, 200)
        html = rv.get_data(as_text=True)
        self.assertIn("8.052", html)  # VCE [V], 3 dp
        self.assertIn("1.230", html)  # IC [mA], 3 dp
        self.assertIn("Forward-Active", html)

    def test_post_invalid_shows_error_keeps_form(self):
        rv = self.client.post(
            "/calculate",
            data={
                "vcc": "12",
                "r1": "-5",
                "r2": "22",
                "rc": "2.2",
                "re": "1",
                "beta": "100",
                "vbe": "0.7",
            },
        )
        self.assertEqual(rv.status_code, 200)
        html = rv.get_data(as_text=True)
        self.assertIn("R1", html)
        self.assertIn('value="12"', html)

    def test_post_empty_body_shows_errors(self):
        rv = self.client.post("/calculate", data={})
        self.assertEqual(rv.status_code, 200)
        html = rv.get_data(as_text=True)
        self.assertIn("value is required", html.lower())

    def test_post_cutoff_shows_warning(self):
        # VCC=1 V -> VTH ~0.18 V <= VBE 0.7 V -> Cutoff
        rv = self.client.post(
            "/calculate",
            data={
                "vcc": "1",
                "r1": "100",
                "r2": "22",
                "rc": "2.2",
                "re": "1",
                "beta": "100",
                "vbe": "0.7",
            },
        )
        self.assertEqual(rv.status_code, 200)
        html = rv.get_data(as_text=True)
        self.assertIn("Cutoff", html)

    def test_results_are_not_hardcoded(self):
        rv = self.client.get("/")
        html = rv.get_data(as_text=True)
        self.assertNotIn("8.052", html)


if __name__ == "__main__":
    unittest.main()
