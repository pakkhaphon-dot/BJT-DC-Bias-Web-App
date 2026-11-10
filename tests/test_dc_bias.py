"""Unit tests for the dc_bias engineering module (ENG29 2121 Lab 02).

Reference design case from the spec: VCC=12 V, R1=100 kOhm, R2=22 kOhm,
RC=2.2 kOhm, RE=1 kOhm, beta=100, VBE=0.70 V.
Expected DC values were precomputed independently by hand.
"""

import unittest

from dc_bias import parse_inputs, solve_dc_bias

REFERENCE_INPUTS = {
    "vcc": "12",
    "r1": "100",
    "r2": "22",
    "rc": "2.2",
    "re": "1",
    "beta": "100",
    "vbe": "0.7",
}


def reference_with(**overrides):
    data = dict(REFERENCE_INPUTS)
    data.update(overrides)
    return data


class ParseInputsTests(unittest.TestCase):
    def test_kohm_conversion(self):
        params, errors = parse_inputs(reference_with())
        self.assertIsNone(errors)
        self.assertEqual(params["r1_ohms"], 100000.0)
        self.assertEqual(params["rc_ohms"], 2200.0)

    def test_negative_resistor_rejected(self):
        params, errors = parse_inputs(reference_with(r1="-5"))
        self.assertIsNone(params)
        self.assertTrue(any("R1" in e for e in errors))

    def test_missing_field_rejected(self):
        params, errors = parse_inputs({})
        self.assertIsNone(params)
        self.assertEqual(len(errors), 7)

    def test_blank_value_rejected(self):
        params, errors = parse_inputs(reference_with(vcc="  "))
        self.assertIsNone(params)
        self.assertTrue(any("VCC" in e for e in errors))

    def test_non_numeric_rejected(self):
        params, errors = parse_inputs(reference_with(beta="hundred"))
        self.assertIsNone(params)
        self.assertTrue(any("beta" in e for e in errors))

    def test_non_finite_rejected(self):
        params, errors = parse_inputs(reference_with(vbe="inf"))
        self.assertIsNone(params)
        params, errors = parse_inputs(reference_with(vcc="nan"))
        self.assertIsNone(params)


class SolveDcBiasTests(unittest.TestCase):
    def test_reference_design_case_forward_active(self):
        params, errors = parse_inputs(reference_with())
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

    def test_cutoff_reports_off_state(self):
        params, _ = parse_inputs(reference_with(vcc="1"))
        r = solve_dc_bias(params)
        self.assertEqual(r["region"], "Cutoff")
        self.assertEqual(r["ic_a"], 0.0)
        self.assertEqual(r["vce_v"], 1.0)
        self.assertTrue(r["warnings"])

    def test_saturation_warning(self):
        params, _ = parse_inputs(reference_with(rc="10"))
        r = solve_dc_bias(params)
        self.assertLess(r["vce_v"], 0.2)
        self.assertEqual(r["region"], "Saturation")
        self.assertTrue(r["warnings"])


if __name__ == "__main__":
    unittest.main()
