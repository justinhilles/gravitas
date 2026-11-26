# Gravitas repository instructions

Read PLAN.md for the charter. The current milestone is a local Python simulation and search tool. Keep experimental physics separate from the established models, and leave speculative models disabled by default.

Use SI at model boundaries and retain model versions, seeds, input configurations, failed checks and results. Treat numerical anomalies as items to investigate. Validate changes against independent formulas or numerical convergence. Keep gravitational, magnetic, electrical, mechanical and optical observables separate. Never adjust a validated model to make a desired outcome score higher.

The CLI in src/gravitas/cli.py drives run validation, simulation, optimization, persistence and reporting. See docs/architecture.md and docs/validation-strategy.md before changing a model. Use Python 3.12 or newer and run `uv run python -m unittest discover -s tests -v` and `uv run gravitas benchmark` before committing scientific changes.

Record scientific outcomes in research/journal.md and architecture decisions in docs/architecture.md. Keep repository operations local unless the owner explicitly requests publication.
