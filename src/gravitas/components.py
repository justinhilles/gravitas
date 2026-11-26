"""Versioned component types and SI parameter domains for schema v1."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Parameter:
    unit: str
    minimum: float
    maximum: float
    integer: bool = False


@dataclass(frozen=True)
class ComponentType:
    model: str
    geometry: str
    parameters: dict[str, Parameter]
    oriented: bool = False


MASS = Parameter("kg", 1e-12, 1e21)
RADIUS = Parameter("m", 0.001, 1000)
REGISTRY = {
    "point_mass": ComponentType("newtonian-v1", "point", {"mass": MASS}),
    "disk": ComponentType("newtonian-v1", "uniform thin disk", {
        "mass": MASS, "radius": RADIUS,
    }, oriented=True),
    "coil_pair": ComponentType("biot-savart-v1", "Helmholtz pair", {
        "mass": MASS,
        "radius": RADIUS,
        "current": Parameter("A", -100, 100),
        "turns": Parameter("1", 1, 1000, integer=True),
        "frequency": Parameter("Hz", 0, 1000),
        "phase": Parameter("rad", -100, 100),
    }, oriented=True),
    "point_charge": ComponentType("coulomb-v1", "point", {
        "charge": Parameter("C", -1, 1),
    }),
}

# Representative scalar room-temperature SI volume susceptibilities for
# sensitivity estimates. Graphite is intentionally excluded due to anisotropy.
SUSCEPTIBILITY = {"bismuth": -1.66e-4, "copper": -9.63e-6,
                  "aluminum": 2.2e-5, "silicon": -4.1e-6}
