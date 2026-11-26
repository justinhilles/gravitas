"""Packaged reference experiments and independent analytical checks."""

from importlib.resources import files
from json import loads
from math import cos, isclose, pi, sin, sqrt

from ..physics import G, MU0, norm, subtract
from ..simulation import simulation

BENCHMARKS = ("GRV-0001", "GRV-0002")


def definition(identifier):
    return loads(files(__package__).joinpath(f"{identifier.lower()}.json").read_text(
        encoding="utf-8"
    ))


def benchmark(identifier):
    raw = definition(identifier)
    result = simulation(raw)
    tolerance = raw["validation"]["relative_tolerance"]
    checks = []
    rows = result["observations"]

    def check(name, actual, expected):
        checks.append({
            "name": name, "actual": actual, "expected": expected,
            "passed": isclose(actual, expected, rel_tol=tolerance, abs_tol=1e-15),
        })

    if identifier == "GRV-0001":
        params = raw["components"][0]["parameters"]
        radius = params["radius"]["value"]
        amplitude = (4 / 5)**1.5 * MU0 * params["turns"]["value"] * (
            params["current"]["value"] / radius
        )
        omega = 2 * pi * params["frequency"]["value"]
        for row in rows:
            if row["measurement"] == "center":
                time = row["time_s"]
                expected = (amplitude * cos(omega * time), amplitude * sin(omega * time), 0)
                check(f"center field vector error at {time:g} s",
                      norm(subtract(row["magnetic_t"], expected)), 0)
                check(f"center field magnitude at {time:g} s", norm(row["magnetic_t"]),
                      amplitude)
                check(f"center gravity symmetry at {time:g} s", norm(row["gravity_m_s2"]), 0)
    else:
        params = raw["components"][0]["parameters"]
        mass = params["mass"]["value"]
        radius = params["radius"]["value"]
        surface_density = mass / (pi * radius**2)
        for row in rows:
            height = row["position_m"][2]
            expected = -2 * pi * G * surface_density * (1 - height / sqrt(radius**2 + height**2))
            check(f"vertical acceleration at {height:g} m", row["gravity_m_s2"][2], expected)
            target = row["disk_targets"][0]["required"]["earth"]
            check(f"rescaled acceleration at {height:g} m",
                  -expected * target["mass_kg"] / mass, target["acceleration_m_s2"])
    result["analytical_checks"] = checks
    return raw, result, all(item["passed"] for item in checks)
