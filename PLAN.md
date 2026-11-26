# Project Gravitas — Research and Development Charter

## 1. Project initialization

Act as the lead software architect, computational physicist, and scientific research engineer for Project Gravitas.

Create a new local Git repository at:

`C:\Projects\gravitas`

Check whether the directory already exists before making changes. Preserve any existing files. Keep the repository private and local until instructed otherwise.

## 2. Project vision

Gravitas is an AI-driven computational physics research platform designed to discover unconventional physical phenomena through automated hypothesis generation, experiment design, numerical simulation, optimization, and scientific validation.

The long-term research objective is to investigate whether gravity can be artificially generated, amplified, reduced, or manipulated through controllable physical interactions.

The aspirational application is a switchable artificial gravity plate that could provide downward gravitational acceleration inside a spacecraft without requiring spacecraft rotation or continuous acceleration.

Do not assume this objective is physically achievable. Determining its feasibility is part of the research.

## 3. Research inspiration

The project is inspired by the following Quanta Magazine article:

**AI Comes Up With Bizarre Physics Experiments. But They Work.**

https://www.quantamagazine.org/ai-comes-up-with-bizarre-physics-experiments-but-they-work-20250721/

Review the article and its referenced research, particularly:

- AI-generated physics experiments.
- Automated scientific discovery.
- Unconventional experimental configurations.
- PyTheus and graph-based experiment representation.
- Evolutionary optimization.
- Symbolic regression.
- AI-assisted gravitational-wave detector optimization.

The central idea is to allow computational systems to discover experimental configurations that humans might not intuitively consider.

Do not restrict the discovery engine to experiments proposed by the project owner.

## 4. Previous research discussions

The following concepts have already been explored as potential research directions:

- Negative gravitational mass.
- Repulsive gravitational interactions.
- Hidden gravitational fields.
- Gravitational time dilation.
- Gravitomagnetism and frame dragging.
- Counterrotating masses.
- Perpendicular rotating magnetic rings.
- Rare-earth magnets.
- Electronically rotating electromagnetic fields.
- Three-axis electromagnetic field generation.
- Superconductors.
- Laser excitation of materials.
- Electron–hole pair generation.
- Particle–antiparticle production.
- Proton bombardment.
- Confined charged-particle plasma.
- Nuclear excitation.
- Gravitational effects of stored energy.
- Artificial gravity plates.

These are research topics, not established mechanisms for manipulating gravity.

No known combination of ordinary magnets, lasers, materials, or particle beams has demonstrated practical gravitational shielding, amplification, or repulsion.

## 5. Scientific principles

The system must adhere to the following principles:

1. Established physics is the baseline against which all results are evaluated.
2. Speculative physics must be explicitly identified and isolated from validated models.
3. Every hypothesis must produce a falsifiable prediction.
4. Every experiment must have measurable outcomes.
5. Conservation laws must be enforced wherever applicable.
6. Units and dimensional consistency must be validated.
7. Numerical anomalies must not be classified as discoveries without independent validation.
8. Negative results must be preserved.
9. Results must be reproducible using recorded parameters, software versions, and random seeds.
10. AI-generated claims must be supported by calculations, experimental evidence, or verifiable scientific references.
11. Safety constraints must not be bypassed by optimization algorithms.
12. The system must distinguish genuine gravitational effects from electromagnetic forces, radiation pressure, buoyancy, thermal effects, vibration, and mechanical acceleration.

The AI should be free to challenge assumptions but never free to manufacture evidence.

## 6. Research engine architecture

Implement a modular discovery engine with the following logical components.

### Hypothesis generator

Responsible for:

- Reviewing scientific literature.
- Identifying unexplored interactions.
- Proposing mathematical hypotheses.
- Generating falsifiable predictions.
- Identifying contradictions with existing experimental evidence.
- Assigning confidence and evidence classifications.

### Experiment designer

Responsible for:

- Selecting physical components.
- Generating experimental geometries.
- Defining material properties.
- Selecting field strengths, frequencies, and phases.
- Defining measurement locations.
- Generating experimental controls.
- Estimating feasibility, cost, and safety.

### Physics simulation engine

Responsible for calculating physical behavior using validated mathematical models.

Initially support:

- Newtonian gravity.
- Gravitational potential.
- Gravitational acceleration.
- Magnetic fields.
- Electric fields.
- Lorentz forces.
- Classical mechanics.
- Energy calculations.
- Radiation pressure.

Later introduce:

- General relativity approximations.
- Gravitomagnetism.
- Electromagnetic stress-energy.
- Quantum materials.
- Plasma physics.
- Optical interactions.
- Quantum field theory models where appropriate.

Do not implement advanced physics using unvalidated placeholder equations.

### Optimization engine

Responsible for exploring experimental configurations using:

- Randomized parameter searches.
- Monte Carlo methods.
- Genetic algorithms.
- Evolutionary optimization.
- Bayesian optimization.
- Multi-objective optimization.
- Symbolic regression.
- Graph-based experiment generation.

The optimization engine should eventually be capable of changing experimental topology, not merely tuning predefined parameters.

### Scientific evaluator

Responsible for:

- Validating simulation outputs.
- Checking conservation laws.
- Detecting numerical instability.
- Comparing results against analytical solutions.
- Evaluating experimental measurability.
- Identifying alternative explanations.
- Estimating uncertainty.
- Rejecting invalid configurations.
- Ranking scientifically useful experiments.

### Research database

Persist:

- Hypotheses.
- Experiments.
- Component definitions.
- Simulation parameters.
- Simulation results.
- Optimization runs.
- Scientific references.
- Validation results.
- Failed experiments.
- Research findings.
- Reproducibility metadata.

### AI research agents

Eventually implement specialized agents for:

- Literature research.
- Hypothesis generation.
- Experiment design.
- Simulation execution.
- Mathematical verification.
- Scientific criticism.
- Safety review.
- Research documentation.

AI agents must not be permitted to modify validated physics equations simply to achieve a desired optimization result.

## 7. Physical component library

Design an extensible component registry.

| Category | Components |
|---|---|
| Geometry | Rings, disks, spheres, plates, cavities, cylinders |
| Electromagnetism | Permanent magnets, coils, electromagnets, electric fields |
| Materials | Copper, aluminum, graphite, bismuth, iron, tungsten, semiconductors |
| Optical | Lasers, photons, mirrors, lenses, optical cavities |
| Particles | Electrons, protons, neutrons, ions, positrons |
| Energy | Electrical, magnetic, thermal, kinetic, optical |
| Quantum | Superconductors, quasiparticles, quantum excitations |
| Measurement | Accelerometers, force sensors, magnetic sensors, interferometers |

Each component should have:

- Unique identifier.
- Component type.
- Physical properties.
- SI units.
- Geometry.
- Position and orientation.
- Configurable parameters.
- Supported simulation models.
- Valid operating ranges.
- Safety constraints.
- Scientific references where applicable.

Components that cannot yet be simulated accurately should remain unavailable to the optimizer.

## 8. Recommended technology stack

Use a Python-first architecture.

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| Numerical computation | NumPy, SciPy |
| Symbolic mathematics | SymPy |
| Data validation | Pydantic |
| Magnetic simulation | Magpylib |
| Optimization | SciPy initially; DEAP or Optuna later |
| Database | SQLite initially; PostgreSQL later |
| ORM | SQLAlchemy if needed |
| API | FastAPI, when needed |
| Visualization | Plotly, Matplotlib |
| Future dashboard | React, TypeScript, Three.js |
| Testing | Pytest |
| Linting and formatting | Ruff |
| Type checking | MyPy or Pyright |
| Dependency management | uv |
| Infrastructure | Docker Compose when needed |
| Version control | Git |

Avoid unnecessary infrastructure during the initial implementation.

Prioritize a working, scientifically validated simulation engine over dashboards, distributed services, or complex agent orchestration.

## 9. Repository structure

Create the following initial structure, adapting it where justified:

```text
gravitas/
├── README.md
├── AGENTS.md
├── pyproject.toml
├── .gitignore
├── docs/
│   ├── architecture.md
│   ├── scientific-principles.md
│   ├── research-roadmap.md
│   ├── validation-strategy.md
│   └── safety.md
├── src/
│   └── gravitas/
│       ├── agents/
│       ├── components/
│       ├── physics/
│       │   ├── gravity/
│       │   ├── electromagnetism/
│       │   ├── mechanics/
│       │   ├── relativity/
│       │   └── quantum/
│       ├── experiments/
│       ├── optimization/
│       ├── evaluation/
│       ├── validation/
│       ├── storage/
│       └── cli/
├── experiments/
│   ├── benchmarks/
│   └── generated/
├── research/
│   ├── literature/
│   ├── hypotheses/
│   ├── findings/
│   └── negative-results/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── physics/
├── notebooks/
└── data/
```

## 10. Experiment definition format

Create a versioned JSON experiment schema.

An experiment should define:

- Experiment ID.
- Name and description.
- Research hypothesis.
- Evidence classification.
- Physical components.
- Component positions and orientations.
- Environmental conditions.
- Simulation models.
- Adjustable parameters.
- Parameter bounds.
- Measurement locations.
- Control configurations.
- Optimization objectives.
- Validation requirements.
- Safety constraints.
- Random seed.
- Model versions.

Use SI units internally.

Validate every experiment before execution.

## 11. First benchmark experiment: GRV-0001

### Three-axis electromagnetic field interaction

The original experimental concept consists of:

- Three perpendicular electromagnetic axes.
- Ideally, three orthogonal Helmholtz coil pairs.
- A shared central experimental region.
- Independently controlled electrical currents.
- Adjustable magnetic field strength, frequency, phase, and direction.
- A removable material sample.
- Optional laser illumination.

The simulation should investigate:

- Three-dimensional magnetic field distribution.
- Magnetic field superposition.
- Rotating magnetic fields.
- Field gradients.
- Magnetic forces on test samples.
- Magnetic energy density.
- Newtonian gravity from component masses.
- Approximate mass equivalent of stored field energy, clearly distinguished from a complete relativistic gravity calculation.

Initially evaluate materials such as graphite, bismuth, copper, aluminum, and silicon where validated material models are available.

The expected result is that conventional electromagnetic effects dominate and gravitational effects are negligible.

This is an intentional validation benchmark. A substantial unexpected gravitational prediction should trigger investigation of numerical errors and model assumptions before being treated as a scientific result.

Do not build physical hardware during the initial software milestone.

## 12. Second benchmark experiment: GRV-0002

### Artificial gravity plate

Model a finite disk of ordinary positive mass.

Calculate:

- Gravitational acceleration at different heights.
- Required mass for a target acceleration.
- Gravitational gradients across a human-sized region.
- Energy-equivalent mass requirements.
- Effects of plate radius and mass distribution.

Compare target accelerations of:

- 0.01g.
- Lunar gravity.
- Martian gravity.
- Earth gravity.

Use this benchmark to establish the scale of the artificial gravity problem and provide a reference for future hypotheses.

## 13. Experiment scoring

Implement a multi-objective scoring framework.

Evaluate:

| Objective | Priority |
|---|---|
| Physical validity | Mandatory |
| Safety | Mandatory |
| Reproducibility | Mandatory |
| Gravitational acceleration | Critical |
| Experimental measurability | High |
| Scientific information gained | High |
| Energy requirements | High |
| Uncertainty | High |
| Experimental feasibility | Medium |
| Novelty | Medium |
| Construction cost | Medium |

Do not combine all physical effects into a single force value and label it gravity.

Report gravitational, electromagnetic, mechanical, optical, and other modeled forces separately.

Distinguish optimization for practical artificial gravity from optimization for detecting small deviations from established physics.

An experiment that conclusively rejects a hypothesis may be scientifically valuable even if it produces no novel physical effect.

## 14. Speculative physics framework

Eventually support experimental extensions to established physics.

Each speculative model must document:

- Mathematical equations.
- Underlying assumptions.
- Free parameters.
- Dimensional consistency.
- Conservation-law implications.
- Compatibility with existing observations.
- Known experimental constraints.
- Falsifiable predictions.
- Proposed distinguishing experiments.

A speculative model producing artificial gravity in a simulation does not constitute evidence that the model describes reality.

Keep speculative models disabled by default.

## 15. Development roadmap

### Phase 1 — Scientific foundation

- Initialize repository.
- Establish Python environment.
- Define experiment and component schemas.
- Implement Newtonian gravity.
- Implement basic electromagnetic models.
- Implement analytical validation tests.
- Implement CLI.
- Persist experiment results.
- Complete initial benchmarks.

### Phase 2 — Automated discovery

- Randomized configuration generation.
- Reproducible parameter searches.
- Multi-objective scoring.
- Evolutionary optimization.
- Experiment ranking.
- Automated result visualization.

### Phase 3 — AI-assisted research

- Literature research pipeline.
- Structured hypothesis generation.
- AI experiment design.
- Independent scientific review agent.
- Automated experiment documentation.
- Citation verification.

### Phase 4 — Advanced physics

- Relativistic approximations.
- Electromagnetic stress-energy.
- Advanced material models.
- Plasma simulation.
- Optical interactions.
- Graph-based experiment topology optimization.

Introduce each model only after validation against established results.

### Phase 5 — Physical experimentation

- Identify safe, measurable experiments.
- Establish experimental controls.
- Estimate equipment requirements.
- Develop data acquisition systems.
- Compare measurements against predictions.
- Investigate statistically significant discrepancies.
- Seek independent replication.

High-energy particle beams, powerful lasers, high-speed magnetic rotors, and hazardous electrical systems are outside the scope of garage experimentation.

## 16. Initial implementation requirements

The first working release should support:

1. Loading a validated experiment from JSON.
2. Executing a Newtonian gravity simulation.
3. Calculating basic magnetic fields.
4. Generating randomized configurations.
5. Executing a reproducible parameter search.
6. Evaluating configurations against scientific objectives.
7. Persisting results.
8. Comparing results against analytical benchmarks.
9. Exporting a human-readable research report.
10. Running automated tests.

Provide CLI commands conceptually equivalent to:

```text
gravitas validate <experiment>
gravitas run <experiment>
gravitas optimize <experiment>
gravitas results
gravitas report <run-id>
gravitas benchmark
```

Do not implement commands that merely return fabricated or placeholder scientific results.

## 17. Testing requirements

Include tests covering:

- Newton's law of gravitation.
- Inverse-square behavior.
- Gravitational field superposition.
- Symmetric mass distributions.
- Circular ring gravity.
- Finite disk gravity.
- Magnetic field superposition.
- Lorentz force calculations.
- Unit validation.
- Energy calculations.
- Reproducible random searches.
- Invalid experiment rejection.
- Result persistence.
- Numerical tolerances.

Document assumptions, expected analytical values, and acceptable numerical error.

## 18. Research documentation

Maintain a permanent research journal containing:

- Research questions.
- Hypotheses.
- Literature references.
- Experimental configurations.
- Simulation results.
- Failed approaches.
- Scientific limitations.
- Open questions.
- Proposed next steps.

Record architectural decisions separately.

Create AGENTS.md so future AI coding agents understand the project's mission, scientific standards, architecture, and development conventions without requiring the original conversation.

## 19. Immediate execution instructions

Begin by:

1. Inspecting the local development environment.
2. Checking Python, Git, and uv availability.
3. Creating the repository safely.
4. Writing the research charter and architecture documentation.
5. Creating the initial Python package.
6. Implementing the experiment schema.
7. Implementing validated Newtonian gravity calculations.
8. Implementing basic magnetic field calculations.
9. Creating the first benchmark experiments.
10. Implementing a reproducible randomized search.
11. Running automated tests.
12. Creating the initial Git commit.
13. Reporting completed work, limitations, and recommended next steps.

Make reasonable architectural decisions independently and document them.

Do not attempt to implement every research phase immediately.

The immediate objective is a small, working, scientifically trustworthy version 0.1.0.

## 20. Definition of success

The initial project is successful when it can autonomously generate, simulate, validate, rank, and document simple physical experiments under established physics.

Long-term success is not defined exclusively by discovering artificial gravity.

Discovering unexpected physical configurations, improving experimental sensitivity, rejecting unsupported hypotheses, and identifying useful research directions are all valuable outcomes.

The guiding principle of Project Gravitas is:

**Explore without prejudice. Validate without compromise.**
