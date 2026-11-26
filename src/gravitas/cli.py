"""Command-line entry points for experiments and benchmark runs."""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from . import __version__
from .benchmarks import BENCHMARKS, benchmark, definition
from .report import markdown
from .schema import load
from .search import optimize
from .simulation import simulation
from .storage import RunStore


def parser():
    root = argparse.ArgumentParser(prog="gravitas")
    root.add_argument("--version", action="version", version=__version__)
    root.add_argument("--db", default="data/gravitas.sqlite3", help="SQLite database path")
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("validate", "run", "optimize"):
        command = commands.add_parser(name)
        command.add_argument("experiment", type=Path)
        if name == "optimize":
            command.add_argument("--trials", type=int, default=16)
    commands.add_parser("results")
    report = commands.add_parser("report")
    report.add_argument("run_id")
    report.add_argument("--output", type=Path)
    benchmarks = commands.add_parser("benchmark")
    benchmarks.add_argument("id", nargs="?", choices=BENCHMARKS)
    return root


def main(argv=None):
    arguments = parser().parse_args(argv)
    command = arguments.command
    store = RunStore(arguments.db)
    try:
        if command == "results":
            print(json.dumps(store.results(), indent=2))
            return 0
        if command == "report":
            content = markdown(store.get(arguments.run_id))
            if arguments.output:
                with arguments.output.open("x", encoding="utf-8") as output:
                    output.write(content)
            else:
                print(content)
            return 0
        if command == "benchmark":
            failed = False
            for identifier in (arguments.id,) if arguments.id else BENCHMARKS:
                try:
                    raw, result, passed = benchmark(identifier)
                except ValueError as error:
                    raw, result, passed = definition(identifier), {"error": str(error)}, False
                    print(f"gravitas: {identifier}: {error}", file=sys.stderr)
                status = "passed" if passed else "failed"
                run_id = store.save(raw, command, status, result)
                print(f"{identifier} {status} {run_id}")
                failed |= not passed
            return int(failed)
        raw = load(arguments.experiment)
        if command == "validate":
            print(f"{raw['id']} schema and model domains validated")
            return 0
        try:
            result = simulation(raw) if command == "run" else optimize(raw, arguments.trials)
        except ValueError as error:
            run_id = store.save(raw, command, "rejected", {"error": str(error)})
            print(f"gravitas: {error} (run {run_id})", file=sys.stderr)
            return 1
        status = "rejected" if command == "optimize" and not result["accepted"] else "passed"
        run_id = store.save(raw, command, status, result)
        print(f"{raw['id']} {status} {run_id}")
        return int(status != "passed")
    except (OSError, sqlite3.Error, ValueError) as error:
        print(f"gravitas: {error}", file=sys.stderr)
        return 1
