# Gravitas

Gravitas v0.1.0 runs reproducible computational physics experiments under established models. Its first benchmarks measure quasistatic field superposition in an orthogonal coil array and the Newtonian gravitational acceleration above a finite disk. See the [research charter](PLAN.md) for the full project scope.

## Run locally

Use Python 3.12 or newer and uv 0.13.1 or a compatible 0.13 release.

```powershell
uv sync
uv run gravitas benchmark
uv run gravitas validate src/gravitas/benchmarks/grv-0001.json
uv run gravitas run src/gravitas/benchmarks/grv-0001.json
uv run gravitas optimize src/gravitas/benchmarks/grv-0002.json --trials 32
uv run gravitas results
uv run gravitas report RUN_ID --output report.md
uv run python -m unittest discover -s tests -v
```

Use an ID printed by a run or by `results`. The default database is `data/gravitas.sqlite3` relative to the working directory. Put `--db PATH` before the subcommand to select a different database. Reports can be printed to the terminal or written to a new file with `--output`.

The installed program includes both benchmark definitions. Copy a benchmark JSON file to create a new experiment. The schema, supported units, and objective directions are described in the [experiment format](docs/experiment-format.md).

## Research scope

- [Architecture and model limits](docs/architecture.md)
- [Scientific principles](docs/scientific-principles.md)
- [Validation strategy](docs/validation-strategy.md)
- [Simulation scope and safety](docs/safety.md)
- [Research roadmap](docs/research-roadmap.md)
- [Research journal](research/journal.md)
