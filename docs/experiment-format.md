# Experiment format v1

The authoritative schema is the strict parser in [schema.py](../src/gravitas/schema.py). The [coil experiment](../src/gravitas/benchmarks/grv-0001.json) and the [disk experiment](../src/gravitas/benchmarks/grv-0002.json) are complete examples. Unknown keys and duplicate JSON object keys are rejected.

| Field | Contract |
| --- | --- |
| schema_version | Integer 1 |
| id, name, description | Nonempty strings |
| hypothesis, prediction | Nonempty strings describing a falsifiable claim and outcome |
| evidence | `established` |
| components | One to sixteen supported sources, with unique IDs, SI positions, typed properties and an orientation where needed |
| measurements | One to sixteen unique IDs with SI positions |
| environment | Vacuum and one to sixteen nonnegative times in seconds |
| controls | Array containing `sources_off` |
| parameters | Up to sixteen distinct component and parameter pairs, each with inclusive min and max quantities |
| objectives | One or more distinct metrics from the table below |
| validation | Relative tolerance from 1e-12 through 0.01 |
| safety | `simulation_only` true and `max_current` in amperes |
| seed | Unsigned 64-bit integer |
| models | Unique model IDs matching the actual source capabilities |
| sample | Optional scalar material, volume in m^3 and mass in kg |

A quantity is an object with `value` and `unit`. A position has a three-element value and unit `m`. Orientation is a dimensionless unit-vector array. A coil pair uses its center and axis normal. A disk uses its center and plane normal.

| Type | Model IDs | Parameter units |
| --- | --- | --- |
| point_mass | newtonian-v1 | mass kg |
| disk | newtonian-v1 | mass kg, radius m |
| coil_pair | newtonian-v1, biot-savart-v1 | mass kg, radius m, current A, turns 1 (integer), frequency Hz, phase rad |
| point_charge | coulomb-v1 | charge C |

The [component registry](../src/gravitas/components.py) specifies parameter bounds, including supported effective sample materials. Model-domain checks enforce axial disk observations and exclude near-singular points. Adjusted inputs are revalidated before simulation.

| Objective | Direction | Aggregate |
| --- | --- | --- |
| gravity_m_s2 | Maximize | Maximum magnitude of gravitational acceleration |
| gravity_gradient_s2 | Minimize | Maximum pairwise acceleration-vector change divided by measurement separation |
| magnetic_force_n | Minimize | Maximum sample magnetic force magnitude |
| magnetic_energy_j | Minimize | Maximum estimated magnetic energy in the 1 mm local measurement cube |

The search ranks candidates across the declared objectives. Narrowing a domain or trading off objectives requires changing the documented experiment input. Rejected candidates retain their sampled values and the reason for rejection.
