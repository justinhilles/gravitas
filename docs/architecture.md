# Architecture

The CLI is the linear entry point. It loads experiment JSON, validates it against the component registry and dispatches to simulation, optimization or analytical benchmarking. SQLite stores a complete copy of each executed definition and its results. Markdown export reads the database, including the recorded model list, software versions, seeds and numerical checks.

| Module | Responsibility |
| --- | --- |
| components and schema | Supported geometry, model IDs, versioned data contract, units and bounds |
| physics | Pure SI calculations |
| simulation | Model dispatch, field assembly, convergence gates, controls and metrics |
| benchmarks | Packaged reference inputs and analytical checks |
| search | Uniform sampling, candidate validation, rejection records and Pareto ranking |
| storage and report | Transactional run persistence and Markdown export |

## Decisions

- Use the Python standard library for this release. The installed uv build backend can package the code offline, and the tested calculations and SQLite workflow require no runtime dependencies. Reconsider numerical libraries when parameter grids or independent solvers justify them.
- Use a single-process CLI and SQLite. Store each run atomically with its experiment definition, an output status and result, preserving rejected candidates in optimization runs.
- Validate strict SI quantities at the input boundary. Reject unknown fields and unsupported model versions. When validated physics behavior changes, version the model and preserve interpretability of existing run records.
- Score accepted configurations on Pareto fronts using declared metric directions. The current metrics cover acceleration, acceleration variation, local field energy and sample force. Experimental uncertainty, measurability and information gain need observable-specific evidence before they can be ranked.
- Package the runnable benchmark JSON with the Python module. The public experiment format and repo tests live beside the source tree.

## Modeling limits

Coils are ideal thin, coincident turns within each ring. Coil rest mass is split uniformly between the two rings. Time-varying currents are quasistatic snapshots with no electric induction, eddy currents, thermal effects or backreaction. Sample force uses a scalar susceptibility and the local gradient of squared magnetic field. Bismuth in the benchmark is treated as an isotropic effective sample. Single-crystal susceptibility is direction dependent. [Primary susceptibility measurements](https://doi.org/10.1103/PhysRev.36.319)

Field energy is a midpoint estimate in a 1 mm cube centered on each measurement. The corresponding mass equivalent is a unit conversion. Reported gravity derives solely from component rest masses. The disk model is a uniform, razor-thin disk evaluated on its axis. Vertical measurement pairs estimate acceleration variation across the modeled region. Changing the disk profile, thickness or off-axis geometry requires a new validated model.

Fixed sources and test samples represent imposed boundary conditions. Energy and momentum exchange with source supports and current supplies are outside the modeled system. Coulomb and Lorentz force, kinetic energy, and radiation pressure calculations are available as baseline functions. The schema exposes static point charges. Optical propagation, induction and coupled mechanical evolution require additional models.
