import math
import unittest

from gravitas.physics import (
    C, G, MU0, axial_loop_field, disk_axial_gravity, disk_axial_potential,
    electric_field, kinetic_energy, loop_elements, loop_field, lorentz_force,
    magnetic_energy_density, point_gravity, radiation_pressure, ring_axial_gravity,
    vector_sum,
)


class PhysicsTests(unittest.TestCase):
    def test_point_gravity_and_inverse_square(self):
        first, potential = point_gravity(8, (0, 0, 0), (2, 0, 0))
        second, _ = point_gravity(8, (0, 0, 0), (4, 0, 0))
        self.assertEqual(first, (-2 * G, 0, 0))
        self.assertEqual(potential, -4 * G)
        self.assertEqual(first[0] / second[0], 4)

    def test_gravity_superposition(self):
        left, _ = point_gravity(10, (-2, 0, 0), (0, 0, 0))
        right, _ = point_gravity(10, (2, 0, 0), (0, 0, 0))
        self.assertEqual(vector_sum([left, right]), (0, 0, 0))

    def test_ring_gravity_against_distributed_points(self):
        radius, height, mass = 2, 3, 10
        elements = loop_elements((0, 0, 0), (0, 0, 1), radius, 64)
        values = [point_gravity(mass / len(elements), position, (0, 0, height))[0]
                  for position, _ in elements]
        self.assertTrue(math.isclose(vector_sum(values)[2],
                                     ring_axial_gravity(mass, radius, height), rel_tol=1e-13))

    def test_disk_gravity_against_midpoint_ring_sum(self):
        mass, radius, height, segments = 1000, 2, 1, 4000
        segment = radius / segments
        values = []
        for index in range(segments):
            r = segment * (index + 0.5)
            ring_mass = mass * 2 * r * segment / radius**2
            values.append(ring_axial_gravity(ring_mass, r, height))
        self.assertTrue(math.isclose(math.fsum(values), disk_axial_gravity(mass, radius, height),
                                     rel_tol=1e-7))
        self.assertEqual(disk_axial_gravity(mass, radius, -height), -disk_axial_gravity(mass, radius, height))

    def test_disk_far_field_and_potential_derivative(self):
        self.assertTrue(math.isclose(disk_axial_gravity(900, 2, 1e8), -G * 900 / 1e16,
                                     rel_tol=1e-12))
        h, step = 0.9, 1e-5
        derivative = (disk_axial_potential(900, 2, h + step)
                      - disk_axial_potential(900, 2, h - step)) / (2 * step)
        self.assertTrue(math.isclose(-derivative, disk_axial_gravity(900, 2, h),
                                     rel_tol=1e-9))

    def test_magnetic_superposition_and_axial_formula(self):
        z_loop = loop_elements((0, 0, 0), (0, 0, 1), 2, 32)
        x_loop = loop_elements((0, 0, 0), (1, 0, 0), 2, 32)
        location = (0, 0, 0)
        z_field = loop_field(z_loop, 10, location)
        x_field = loop_field(x_loop, 5, location)
        self.assertTrue(math.isclose(z_field[2], axial_loop_field(2, 0, 10), rel_tol=1e-12))
        combined = vector_sum([z_field, x_field])
        self.assertTrue(math.isclose(combined[0], axial_loop_field(2, 0, 5), rel_tol=1e-12))
        self.assertEqual(combined[1], 0)
        self.assertEqual(combined[2], z_field[2])

    def test_electric_and_lorentz_force(self):
        field = electric_field(2e-9, (0, 0, 0), (1, 0, 0))
        self.assertGreater(field[0], 0)
        self.assertEqual(lorentz_force(2, (1, 0, 0), (1, 0, 0), (0, 0, 3)), (2, -6, 0))

    def test_energy_and_pressure(self):
        self.assertEqual(kinetic_energy(2, 3), 9)
        self.assertTrue(math.isclose(magnetic_energy_density((0, 0, MU0)), MU0 / 2))
        self.assertEqual(radiation_pressure(C, 1), 2)


if __name__ == "__main__":
    unittest.main()
