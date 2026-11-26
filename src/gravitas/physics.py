"""SI calculations for Newtonian gravity and quasistatic electromagnetism."""

from math import cos, dist, fsum, pi, sin, sqrt

G = 6.67430e-11
C = 299_792_458
MU0 = 1.25663706127e-6
EPS0 = 1 / (MU0 * C**2)
G0 = 9.80665
ZERO = (0.0, 0.0, 0.0)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b, strict=True))


def scale(factor, vector):
    return tuple(factor * x for x in vector)


def subtract(a, b):
    return add(a, scale(-1, b))


def dot(a, b):
    return fsum(x * y for x, y in zip(a, b, strict=True))


def norm(vector):
    return dist(vector, ZERO)


def cross(a, b):
    x, y, z = a
    u, v, w = b
    return y * w - z * v, z * u - x * w, x * v - y * u


def vector_sum(vectors):
    return tuple(map(fsum, zip(*vectors))) if vectors else ZERO


def point_gravity(mass, source, location):
    """Return gravitational acceleration and potential per unit test mass."""
    displacement = subtract(source, location)
    radius = norm(displacement)
    if radius == 0:
        raise ValueError("measurement coincides with a point mass")
    return scale(G * mass / radius**3, displacement), -G * mass / radius


def ring_axial_gravity(mass, radius, height):
    return -G * mass * height / (radius**2 + height**2)**1.5


def disk_axial_gravity(mass, radius, height):
    """Acceleration along the normal outside a uniform razor-thin disk."""
    if height == 0:
        raise ValueError("disk field is discontinuous across its surface")
    length = sqrt(radius**2 + height**2)
    # Rationalized form avoids cancellation far from the disk.
    magnitude = 2 * G * mass / (length * (length + abs(height)))
    return -magnitude if height > 0 else magnitude


def disk_axial_potential(mass, radius, height):
    return -2 * G * mass / (sqrt(radius**2 + height**2) + abs(height))


def loop_elements(center, normal, radius, segments):
    reference = (1.0, 0.0, 0.0) if abs(normal[0]) < 0.9 else (0.0, 1.0, 0.0)
    first = cross(normal, reference)
    first = scale(1 / norm(first), first)
    second = cross(normal, first)
    step = 2 * pi / segments
    elements = []
    for index in range(segments):
        angle = (index + 0.5) * step
        offset = add(scale(cos(angle), first), scale(sin(angle), second))
        tangent = add(scale(-sin(angle), first), scale(cos(angle), second))
        elements.append((add(center, scale(radius, offset)), scale(radius * step, tangent)))
    return elements


def loop_distance(center, normal, radius, location):
    offset = subtract(location, center)
    height = dot(offset, normal)
    radial = norm(subtract(offset, scale(height, normal)))
    return sqrt((radial - radius)**2 + height**2)


def loop_field(elements, ampere_turns, location):
    contributions = []
    for position, length in elements:
        displacement = subtract(location, position)
        radius = norm(displacement)
        if radius == 0:
            raise ValueError("measurement coincides with a filament element")
        contributions.append(scale(1 / radius**3, cross(length, displacement)))
    return scale(MU0 * ampere_turns / (4 * pi), vector_sum(contributions))


def axial_loop_field(radius, height, ampere_turns):
    return MU0 * ampere_turns * radius**2 / (2 * (radius**2 + height**2)**1.5)


def electric_field(charge, source, location):
    displacement = subtract(location, source)
    radius = norm(displacement)
    if radius == 0:
        raise ValueError("measurement coincides with a point charge")
    return scale(charge / (4 * pi * EPS0 * radius**3), displacement)


def lorentz_force(charge, velocity, electric, magnetic):
    return scale(charge, add(electric, cross(velocity, magnetic)))


def magnetic_energy_density(field):
    return dot(field, field) / (2 * MU0)


def kinetic_energy(mass, speed):
    return 0.5 * mass * speed**2


def radiation_pressure(power_per_area, reflectance=0):
    """Normal incidence with an opaque surface and reflectance in [0, 1]."""
    return power_per_area * (1 + reflectance) / C
