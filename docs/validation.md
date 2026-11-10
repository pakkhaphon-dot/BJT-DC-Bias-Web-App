# Validation — reference DC bias calculation

ENG29 2121 Lab 02 — acceptance criterion A3: results agree with an independent engineering calculation.

## Reference case (from the lab handout)

| Input | Value |
|---|---|
| VCC | 12 V |
| R1 | 100 kΩ |
| R2 | 22 kΩ |
| RC | 2.2 kΩ |
| RE | 1 kΩ |
| β | 100 |
| VBE | 0.70 V |

## Independent hand calculation (Forward-Active approximation)

1. Thevenin equivalent at the base

   `VTH = VCC · R2 / (R1 + R2) = 12 · 22 / (100 + 22) = 2.163934 V`

   `RTH = R1 · R2 / (R1 + R2) = 100 · 22 / 122 = 18.0328 kΩ = 18032.787 Ω`

2. Check `VTH > VBE`: 2.163934 V > 0.70 V → transistor is ON, forward-active model applies.

3. Base current

   `IB = (VTH − VBE) / (RTH + (β+1) · RE)`

   `IB = (2.163934 − 0.70) / (18032.787 + 101 · 1000) = 1.463934 / 119032.787 = 1.229858 × 10⁻⁵ A`

4. Collector and emitter currents

   `IC = β · IB = 100 · 1.229858e-5 = 1.229858 × 10⁻³ A = 1.230 mA`

   `IE = (β+1) · IB = 101 · 1.229858e-5 = 1.242157 × 10⁻³ A = 1.242 mA`

5. Node voltages

   `VE = IE · RE = 1.242157e-3 · 1000 = 1.242157 V`

   `VB = VE + VBE = 1.242157 + 0.70 = 1.942157 V`

   `VC = VCC − IC · RC = 12 − 1.229858e-3 · 2200 = 12 − 2.705688 = 9.294312 V`

   `VCE = VC − VE = 9.294312 − 1.242157 = 8.052154 V`

6. Region check: VCE = 8.052 V ≫ 0.2 V → **Forward-Active**, no warnings.

## What the web app displays (verified by tests)

| Quantity | Hand calculation | Web app (test assertion) | Match |
|---|---|---|---|
| VTH | 2.163934 V | `assertAlmostEqual(2.163934, places=5)` | ✅ |
| RTH | 18032.787 Ω | `assertAlmostEqual(..., delta=0.001)` | ✅ |
| IC | 1.230 mA | `assertAlmostEqual(1.229858e-3 A, delta=1e-8)` | ✅ |
| IE | 1.242 mA | `assertAlmostEqual(1.242157e-3 A, delta=1e-8)` | ✅ |
| VE | 1.242157 V | `assertAlmostEqual(..., places=4)` | ✅ |
| VB | 1.942157 V | `assertAlmostEqual(..., places=4)` | ✅ |
| VC | 9.294311 V | `assertAlmostEqual(..., places=4)` | ✅ |
| VCE | 8.052154 V | `assertAlmostEqual(..., places=4)` | ✅ |
| Region | Forward-Active | `"Forward-Active"`, no warnings | ✅ |

The hand calculation and the web application agree; the forward-active model is valid for this operating point.
