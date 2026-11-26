"""Evaluate configured sources, controls and numerical convergence."""

from math import cos, fsum, pi

from .components import SUSCEPTIBILITY
from .physics import (
    C, G0, MU0, ZERO, add, axial_loop_field, disk_axial_gravity,
    disk_axial_potential, dot, electric_field, loop_distance, loop_elements,
    loop_field, magnetic_energy_density, norm, point_gravity, scale, subtract,
    vector_sum,
)
from .schema import validate

AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
REGION_SIDE = 0.001  # Local cubic region centered on each measurement, in m.
TARGETS = {"0.01g": 0.01 * G0, "lunar": 1.62, "martian": 3.71, "earth": G0}


def coil_loops(source):
    radius = source["parameters"]["radius"]
    normal = source["normal"]
    centers = [add(source["position"], scale(side * radius / 2, normal))
               for side in (-1, 1)]
    return [
        (center, normal, radius, loop_elements(center, normal, radius, 32),
         loop_elements(center, normal, radius, 64))
        for center in centers
    ]


def field(loops, location, tolerance):
    contributions = []
    for center, normal, radius, coarse, fine, current in loops:
        if loop_distance(center, normal, radius, location) < radius / 4:
            raise ValueError("measurement stencil lies within a quarter radius of a filament")
        value = loop_field(fine, current, location)
        comparison = loop_field(coarse, current, location)
        limit = tolerance * abs(axial_loop_field(radius, 0, current))
        if norm(subtract(value, comparison)) > limit:
            raise ValueError("Biot–Savart quadrature did not converge within tolerance")
        contributions.append(value)
    return vector_sum(contributions)


def coil_gravity(pair, mass, location, tolerance):
    approximations = []
    for resolution in (3, 4):
        points = [position for loop in pair for position, _ in loop[resolution]]
        values = [point_gravity(mass / len(points), position, location) for position in points]
        approximations.append((vector_sum([value[0] for value in values]),
                               fsum(value[1] for value in values)))
    (coarse, low), (fine, high) = approximations
    scale_length = max(pair[0][2], norm(subtract(location, pair[0][0])))
    if (norm(subtract(coarse, fine)) > tolerance * abs(high) / scale_length
            or abs(low - high) > tolerance * abs(high)):
        raise ValueError("coil gravity quadrature did not converge within tolerance")
    return fine, high


def field_gradient(loops, location, step, tolerance):
    gradient = []
    for axis in AXES:
        delta = scale(step, axis)
        low = field(loops, subtract(location, delta), tolerance)
        high = field(loops, add(location, delta), tolerance)
        gradient.append((dot(high, high) - dot(low, low)) / (2 * step))
    return tuple(gradient)


def static_measurement(components, coil_geometry, location, tolerance):
    gravities, potentials, electric = [], [], []
    disk_targets = []
    for source in components:
        params = source["parameters"]
        center = source["position"]
        kind = source["type"]
        if kind == "point_charge":
            electric.append(electric_field(params["charge"], center, location))
            continue
        mass = params["mass"]
        if kind == "disk":
            normal = source["normal"]
            height = dot(subtract(location, center), normal)
            acceleration = disk_axial_gravity(mass, params["radius"], height)
            gravity = scale(acceleration, normal)
            potential = disk_axial_potential(mass, params["radius"], height)
            unit_acceleration = abs(acceleration) / mass
            disk_targets.append({
                "component": source["id"],
                "height_m": height,
                "radius_m": params["radius"],
                "required": {
                    name: {"acceleration_m_s2": target,
                           "mass_kg": target / unit_acceleration,
                           "rest_energy_j": target / unit_acceleration * C**2}
                    for name, target in TARGETS.items()
                },
            })
        elif kind == "coil_pair":
            gravity, potential = coil_gravity(coil_geometry[source["id"]], mass, location, tolerance)
        else:
            gravity, potential = point_gravity(mass, center, location)
        gravities.append(gravity)
        potentials.append(potential)
    return vector_sum(gravities), fsum(potentials), vector_sum(electric), disk_targets


def simulation(raw):
    spec = validate(raw)
    components = spec["components"]
    coil_geometry = {source["id"]: coil_loops(source)
                     for source in components if source["type"] == "coil_pair"}
    coils = [(source["parameters"], coil_geometry[source["id"]])
             for source in components if source["type"] == "coil_pair"]
    tolerance = spec["tolerance"]
    step = spec["half_step"]
    static = {name: static_measurement(components, coil_geometry, location, tolerance)
              for name, location in spec["measurements"].items()}
    observations = []
    for time in spec["times"]:
        loops = [
            (*loop, params["turns"] * params["current"] *
             cos(2 * pi * params["frequency"] * time + params["phase"]))
            for params, pair in coils for loop in pair
        ]
        for name, location in spec["measurements"].items():
            gravity, potential, electric, disk_targets = static[name]
            magnetic = field(loops, location, tolerance)
            gradient = field_gradient(loops, location, step, tolerance)
            check = field_gradient(loops, location, 2 * step, tolerance)
            # Mixed criterion accommodates cancellation at symmetry points.
            characteristic = sum(abs(axial_loop_field(loop[2], 0, loop[-1]))
                                 for loop in loops)
            gradient_floor = characteristic**2 / max(min(
                (loop[2] for loop in loops), default=1), step)
            if norm(subtract(gradient, check)) > tolerance * max(norm(gradient), gradient_floor):
                raise ValueError("magnetic gradient did not converge within tolerance")
            density = magnetic_energy_density(magnetic)
            energy = density * REGION_SIDE**3
            sample = spec["sample"]
            force = None if sample is None else scale(
                SUSCEPTIBILITY[sample[0]] * sample[1] / (2 * MU0), gradient
            )
            observations.append({
                "measurement": name, "position_m": location, "time_s": time,
                "gravity_m_s2": gravity, "potential_j_kg": potential,
                "electric_v_m": electric, "magnetic_t": magnetic,
                "magnetic_b_squared_gradient_t2_m": gradient,
                "magnetic_sample_force_n": force,
                "gravitational_sample_force_n": None if sample is None else scale(sample[2], gravity),
                "magnetic_energy_density_j_m3": density,
                "local_magnetic_energy_j": energy,
                "local_magnetic_energy_mass_equivalent_kg": energy / C**2,
                "disk_targets": disk_targets,
            })
    accelerations = []
    first_slice = observations[:len(spec["measurements"])]
    for index, left in enumerate(first_slice):
        for right in first_slice[index + 1:]:
            separation = norm(subtract(right["position_m"], left["position_m"]))
            if separation > 0:
                difference = subtract(right["gravity_m_s2"], left["gravity_m_s2"])
                accelerations.append(norm(difference) / separation)
    metrics = {
        "gravity_m_s2": max(norm(row["gravity_m_s2"]) for row in observations),
        "magnetic_force_n": max(norm(row["magnetic_sample_force_n"] or ZERO)
                                for row in observations),
        "magnetic_energy_j": max(row["local_magnetic_energy_j"] for row in observations),
        "gravity_gradient_s2": max(accelerations, default=0),
    }
    return {
        "observations": observations,
        "control": {"name": "sources_off", "gravity_m_s2": ZERO,
                    "magnetic_t": ZERO, "electric_v_m": ZERO},
        "region_side_m": REGION_SIDE,
        "metrics": metrics,
        "validation": {"status": "passed", "relative_tolerance": tolerance},
    }
