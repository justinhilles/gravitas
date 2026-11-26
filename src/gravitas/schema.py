"""Strict parser for version 1 SI experiment definitions."""

import json
from math import isclose
from pathlib import Path

from .components import REGISTRY, SUSCEPTIBILITY, Parameter
from .physics import C, add, dot, loop_distance, norm, scale, subtract

METRICS = {
    "gravity_m_s2": "maximize",
    "magnetic_force_n": "minimize",
    "magnetic_energy_j": "minimize",
    "gravity_gradient_s2": "minimize",
}
DISTANCE = Parameter("m", -10000, 10000)


def keys(value, required, optional=()):
    if not isinstance(value, dict):
        raise ValueError("expected object")
    missing = set(required) - value.keys()
    extra = value.keys() - set(required) - set(optional)
    if missing or extra:
        raise ValueError(f"missing keys {sorted(missing)}, unknown keys {sorted(extra)}")


def number(value, parameter):
    if (type(value) not in (int, float)
            or (parameter.integer and type(value) is not int)
            or not parameter.minimum <= value <= parameter.maximum):
        raise ValueError(f"expected {parameter.unit} in [{parameter.minimum}, "
                         f"{parameter.maximum}], got {value!r}")
    return value


def quantity(value, parameter):
    keys(value, ("value", "unit"))
    if value["unit"] != parameter.unit:
        raise ValueError(f"expected SI unit {parameter.unit}, got {value['unit']!r}")
    return number(value["value"], parameter)


def vector(value, parameter):
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError("expected a three-element vector")
    return tuple(number(element, parameter) for element in value)


def position(value):
    keys(value, ("value", "unit"))
    if value["unit"] != "m":
        raise ValueError("position requires unit m")
    return vector(value["value"], DISTANCE)


def string(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("expected a nonempty string")
    return value


def array(value, minimum, maximum):
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        raise ValueError(f"expected an array with {minimum} to {maximum} entries")
    return value


def component(value):
    keys(value, ("id", "type", "position", "parameters"), ("normal",))
    kind = string(value["type"])
    if kind not in REGISTRY:
        raise ValueError(f"unsupported component type {kind}")
    definition = REGISTRY[kind]
    keys(value["parameters"], definition.parameters)
    parsed = {
        "id": string(value["id"]),
        "type": kind,
        "position": position(value["position"]),
        "parameters": {
            name: quantity(value["parameters"][name], spec)
            for name, spec in definition.parameters.items()
        },
    }
    if definition.oriented != ("normal" in value):
        raise ValueError(f"invalid orientation for {kind}")
    if definition.oriented:
        normal = vector(value["normal"], Parameter("1", -1, 1))
        length = norm(normal)
        if not isclose(length, 1, rel_tol=1e-9):
            raise ValueError("normal must be a unit vector")
        parsed["normal"] = scale(1 / length, normal)
    return parsed


def validate(raw):
    keys(raw, (
        "schema_version", "id", "name", "description", "hypothesis", "prediction",
        "evidence", "components", "measurements", "environment", "controls",
        "parameters", "objectives", "validation", "safety", "seed", "models",
    ), ("sample",))
    number(raw["schema_version"], Parameter("schema version", 1, 1, True))
    for name in ("id", "name", "description", "hypothesis", "prediction"):
        string(raw[name])
    if raw["evidence"] != "established":
        raise ValueError("only established models are enabled in schema v1")
    number(raw["seed"], Parameter("seed", 0, 2**64 - 1, True))
    components = [component(item) for item in array(raw["components"], 1, 16)]
    indexed = {item["id"]: item for item in components}
    if len(indexed) != len(components):
        raise ValueError("duplicate component ID")
    models = sorted({REGISTRY[item["type"]].model for item in components})
    if any(item["type"] == "coil_pair" for item in components) and "newtonian-v1" not in models:
        models = sorted([*models, "newtonian-v1"])
    if sorted(array(raw["models"], 1, 3), key=string) != models:
        raise ValueError(f"model versions must match components: {models}")

    environment = raw["environment"]
    keys(environment, ("medium", "times"))
    if environment["medium"] != "vacuum":
        raise ValueError("schema v1 supports vacuum")
    times = [quantity(item, Parameter("s", 0, 1000))
             for item in array(environment["times"], 1, 16)]
    measurements = {}
    for item in array(raw["measurements"], 1, 16):
        keys(item, ("id", "position"))
        name = string(item["id"])
        if name in measurements:
            raise ValueError("duplicate measurement ID")
        measurements[name] = position(item["position"])

    objectives = [string(item) for item in array(raw["objectives"], 1, len(METRICS))]
    if set(objectives) - METRICS.keys() or len(set(objectives)) != len(objectives):
        raise ValueError("objectives must be unique supported metrics")
    controls = [string(item) for item in array(raw["controls"], 1, 1)]
    if controls != ["sources_off"]:
        raise ValueError("supported control is sources_off")
    validation = raw["validation"]
    keys(validation, ("relative_tolerance",))
    tolerance = number(validation["relative_tolerance"], Parameter("1", 1e-12, 0.01))
    safety = raw["safety"]
    keys(safety, ("simulation_only", "max_current"))
    if safety["simulation_only"] is not True:
        raise ValueError("v1 requires simulation_only")
    max_current = quantity(safety["max_current"], Parameter("A", 0, 100))

    adjustable = []
    for item in array(raw["parameters"], 0, 16):
        keys(item, ("component", "parameter", "min", "max"))
        source = indexed.get(string(item["component"]))
        name = string(item["parameter"])
        if source is None or name not in source["parameters"]:
            raise ValueError("adjustable parameter must refer to an existing parameter")
        spec = REGISTRY[source["type"]].parameters[name]
        low, high = (quantity(item[key], spec) for key in ("min", "max"))
        if low > high or (name == "current" and max(abs(low), abs(high)) > max_current):
            raise ValueError("invalid adjustable parameter bounds")
        adjustable.append((source["id"], name, low, high, spec.integer))
    if len({item[:2] for item in adjustable}) != len(adjustable):
        raise ValueError("duplicate adjustable parameter")

    sample = None
    if "sample" in raw:
        value = raw["sample"]
        keys(value, ("material", "volume", "mass"))
        material = string(value["material"])
        if material not in SUSCEPTIBILITY:
            raise ValueError("unsupported isotropic sample material")
        sample = (material, quantity(value["volume"], Parameter("m^3", 1e-15, 1e-3)),
                  quantity(value["mass"], Parameter("kg", 1e-12, 100)))

    if "magnetic_force_n" in objectives and sample is None:
        raise ValueError("magnetic force scoring requires a sample")
    if "gravity_gradient_s2" in objectives and len(set(measurements.values())) < 2:
        raise ValueError("gravity gradient scoring requires two distinct positions")

    half_step = 1e-4
    for source in components:
        params = source["parameters"]
        for location in measurements.values():
            offset = subtract(location, source["position"])
            if source["type"] in {"point_mass", "point_charge"} and norm(offset) < 1e-9:
                raise ValueError("measurement is within 1 nm of a point source")
            if source["type"] == "disk":
                height = dot(offset, source["normal"])
                off_axis = subtract(offset, scale(height, source["normal"]))
                if abs(height) < 1e-9 or norm(off_axis) > 1e-10 * abs(height):
                    raise ValueError("disk measurements require nonzero axial height")
            if source["type"] == "coil_pair":
                radius = params["radius"]
                normal = source["normal"]
                if params["frequency"] * (norm(offset) + 1.5 * radius) / C > 0.01:
                    raise ValueError("coil geometry exceeds the quasistatic domain")
                for side in (-1, 1):
                    center = add(source["position"], scale(side * radius / 2, normal))
                    if loop_distance(center, normal, radius, location) < radius / 4 + 2 * half_step:
                        raise ValueError("measurement stencil is too close to a coil filament")
        if source["type"] == "coil_pair" and abs(params["current"]) > max_current:
            raise ValueError("coil current exceeds experiment limit")
    return {
        "components": components, "measurements": measurements, "times": times,
        "adjustable": adjustable, "seed": raw["seed"], "objectives": objectives,
        "sample": sample, "tolerance": tolerance, "half_step": half_step,
    }


def unique_object(pairs):
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("duplicate JSON object key")
    return result


def load(path):
    raw = json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    validate(raw)
    return raw
