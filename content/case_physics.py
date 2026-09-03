"""Mock physics for the E255 Task 1 test case.

Stands in for the FE (finite-element) thermal solver that the course's lab
environment will eventually provide. Case: liquid-cooled cold plate under a
battery module. Every constant here is [MOCK] — plausibly realistic, but
invented for feasibility testing. None of these numbers are course spec.

This file is "instructor-side": students would never see it. It plays the
role of the reference simulation ([T1v2] Req A "reference simulation values")
and generates the dataset ground truth.
"""
import numpy as np

CP_COOLANT = 4186.0        # J/(kg K), water coolant [MOCK]
BATTERY_TEMP_LIMIT_C = 60.0  # max safe cell temperature, deg C [MOCK]

# Input ranges [MOCK]. The five dimensions [T1v2] Req I names:
# heat load, coolant flow, inlet temperature, geometry, conductivity.
RANGES = {
    "Q_W":      (50.0, 500.0),   # heat load into the plate
    "mdot_kgs": (0.01, 0.10),    # coolant mass flow rate
    "Tin_C":    (15.0, 40.0),    # coolant inlet temperature
    "w_mm":     (1.0, 3.0),      # cooling-channel width (geometry dimension)
    "k_WmK":    (100.0, 400.0),  # plate thermal conductivity (material dimension)
}
INPUT_COLS = list(RANGES)
OUTPUT_COLS = ["Tout_C", "Tmax_C"]

# Thermal-resistance constants [MOCK]:
#   conduction resistance  R_cond = _C_COND / k
#   convection resistance  R_conv = _C_CONV * w^0.2 / mdot^0.8
_C_COND = 4.0
_C_CONV = 0.004

# Observation noise, mimicking solver/measurement variability [MOCK]
NOISE_SD = {"Tout_C": 0.15, "Tmax_C": 0.40}


def truth(Q, mdot, Tin, w, k):
    """Noise-free 'reference simulation'. Returns (Tout_C, Tmax_C).

    Physics content (this is what the PINN's constraints encode):
      * Energy balance (first law): Tout = Tin + Q / (mdot * cp)
      * Tmax = mean coolant temperature + Q * (R_cond + R_conv)
      * Monotone consequences: Tout >= Tin for Q > 0; Tmax > Tout here.
    """
    Q, mdot, Tin, w, k = map(np.asarray, (Q, mdot, Tin, w, k))
    Tout = Tin + Q / (mdot * CP_COOLANT)
    Tavg = 0.5 * (Tin + Tout)
    R = _C_COND / k + _C_CONV * w**0.2 / mdot**0.8
    Tmax = Tavg + Q * R
    return Tout, Tmax


def energy_balance_Tout(Q, mdot, Tin):
    """The first-law outlet temperature — the PINN's energy-balance target."""
    return np.asarray(Tin) + np.asarray(Q) / (np.asarray(mdot) * CP_COOLANT)


# Per-dimension densely sampled training regions [MOCK] - the content of the
# provided dataset datasheet ([T1v2] Req I needs a canonical dense/sparse
# boundary per dimension or I1a-e are not consistently gradable).
# Q/mdot/Tin tails align with the Req H sparse-region definitions below.
DENSE_REGIONS = {
    "Q_W":      (50.0, 432.5),     # sparse: top 15% (-> sparse_high_heat)
    "mdot_kgs": (0.0235, 0.0865),  # sparse: both 15% tails (-> low_flow_boundary / sparse_high_flow)
    "Tin_C":    (15.0, 36.25),     # sparse: top 15%
    "w_mm":     (1.7, 2.3),        # sparse: outside central band
    "k_WmK":    (205.0, 295.0),    # sparse: outside central band
}


def region_label(Q, mdot):
    """[T1v2] Req H1a-e taxonomy, VERBATIM from the 8/24 draft:
    central interpolation / sparse high-flow / sparse high-heat /
    low-flow boundary / combined thermal-extreme.

    The draft's regions overlap as written (flagged defect); this mock makes
    them disjoint via an explicit priority rule (first match wins):
    combined > low-flow boundary > sparse high-flow > sparse high-heat >
    central. Band fractions are [MOCK]."""
    Q, mdot = np.asarray(Q), np.asarray(mdot)
    qa, qb = RANGES["Q_W"]; ma, mb = RANGES["mdot_kgs"]
    qs, ms = qb - qa, mb - ma
    conds = [
        (Q >= qb - 0.30 * qs) & (mdot <= ma + 0.30 * ms),  # H1e
        mdot <= ma + 0.15 * ms,                            # H1d
        mdot >= mb - 0.15 * ms,                            # H1b
        Q >= qb - 0.15 * qs,                               # H1c
    ]
    names = ["combined_thermal_extreme", "low_flow_boundary",
             "sparse_high_flow", "sparse_high_heat"]
    return np.select(conds, names, default="central_interpolation")


REGION_ORDER = ["central_interpolation", "sparse_high_flow", "sparse_high_heat",
                "low_flow_boundary", "combined_thermal_extreme"]

# The four named edge conditions of [T1v2] Req C (center-of-range elsewhere) [MOCK]
EDGE_CONDITIONS = {
    "min_flow":               dict(Q_W=275.0, mdot_kgs=0.010, Tin_C=27.5, w_mm=2.0, k_WmK=250.0),
    "max_heat":               dict(Q_W=500.0, mdot_kgs=0.055, Tin_C=27.5, w_mm=2.0, k_WmK=250.0),
    "max_inlet_temp":         dict(Q_W=275.0, mdot_kgs=0.055, Tin_C=40.0, w_mm=2.0, k_WmK=250.0),
    "combined_highQ_lowflow": dict(Q_W=500.0, mdot_kgs=0.010, Tin_C=27.5, w_mm=2.0, k_WmK=250.0),
}

EXPECTED_BEHAVIOR = {
    "min_flow": ("Largest coolant temperature rise (Tout - Tin) since dT = Q/(mdot*cp); "
                 "convective resistance also grows at low flow, lifting Tmax."),
    "max_heat": ("Both Tout - Tin and the plate-to-coolant temperature drop scale with Q, "
                 "so Tmax rises roughly linearly with heat load."),
    "max_inlet_temp": ("Whole temperature field shifts up nearly one-for-one with Tin; "
                       "gradients (Tout - Tin, Tmax - Tin) barely change."),
    "combined_highQ_lowflow": ("Worst case: large Q meets large convective resistance; "
                               "Tmax should approach or exceed the battery limit."),
}

# FE-solver cost figures for [T1v2] Req G — PROVIDED to students because they
# cannot run the solver (audit finding; G1 fix). All [MOCK].
FE_COST = {
    "exec_time_per_run_s": 2400.0,   # 40 min per FE run [MOCK]
    "peak_memory_GB": 8.2,           # [MOCK]
    "runs_in_dataset": 1200,         # dataset generation campaign size [MOCK]
}
