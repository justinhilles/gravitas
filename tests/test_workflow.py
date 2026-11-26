import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

from gravitas.benchmarks import BENCHMARKS, benchmark, definition
from gravitas.cli import main
from gravitas.schema import validate
from gravitas.search import optimize
from gravitas.storage import RunStore


class WorkflowTests(unittest.TestCase):
    def test_benchmarks(self):
        for identifier in BENCHMARKS:
            with self.subTest(identifier=identifier):
                _, result, passed = benchmark(identifier)
                self.assertTrue(passed, result["analytical_checks"])
                self.assertEqual(result["control"]["gravity_m_s2"], (0, 0, 0))

    def test_wrong_units_and_out_of_bounds_current(self):
        raw = definition("GRV-0001")
        wrong_units = deepcopy(raw)
        wrong_units["components"][0]["parameters"]["current"]["unit"] = "mA"
        with self.assertRaisesRegex(ValueError, "SI unit A"):
            validate(wrong_units)
        raw["parameters"][0]["max"]["value"] = 6
        with self.assertRaisesRegex(ValueError, "bounds"):
            validate(raw)

    def test_invalid_normal_and_off_axis_disk(self):
        raw = definition("GRV-0002")
        raw["components"][0]["normal"] = [0, 0, 2]
        with self.assertRaises(ValueError):
            validate(raw)
        raw = definition("GRV-0002")
        raw["measurements"][0]["position"]["value"][0] = 1
        with self.assertRaisesRegex(ValueError, "axial"):
            validate(raw)

    def test_stable_pareto_search(self):
        raw = definition("GRV-0002")
        before = deepcopy(raw)
        first = optimize(raw, 20)
        self.assertEqual(first, optimize(raw, 20))
        self.assertEqual(raw, before)
        self.assertEqual(len(first["accepted"]), 20)
        ranks = [item["rank"] for item in first["accepted"]]
        self.assertEqual(ranks, sorted(ranks))
        self.assertEqual(ranks[0], 1)
        self.assertGreater(ranks[-1], 1)

    def test_invalid_search_candidates_are_retained(self):
        raw = definition("GRV-0001")
        raw["measurements"][0]["position"]["value"] = [0.05, 0.1, 0]
        raw["parameters"] = [{"component": "x", "parameter": "radius",
                              "min": {"unit": "m", "value": 0.1},
                              "max": {"unit": "m", "value": 0.1}}]
        result = optimize(raw, 1)
        self.assertEqual(result["accepted"], [])
        self.assertIn("filament", result["rejected"][0]["reason"])

    def test_cli_and_sqlite_round_trip(self):
        directory = Path(tempfile.gettempdir()).resolve() / f"gravitas-test-{uuid4()}"
        directory.mkdir()
        self.addCleanup(shutil.rmtree, directory)
        database = directory / "test.sqlite3"
        args = ["--db", str(database)]
        experiment = directory / "disk.json"
        experiment.write_text(json.dumps(definition("GRV-0002")), encoding="utf-8")
        report = directory / "report.md"
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(main([*args, "validate", str(experiment)]), 0)
            self.assertEqual(main([*args, "run", str(experiment)]), 0)
            run = RunStore(database).results()[0]
            self.assertEqual(main([*args, "report", run["id"], "--output", str(report)]), 0)
            self.assertEqual(main([*args, "report", run["id"], "--output", str(report)]), 1)
            self.assertEqual(main([*args, "optimize", str(experiment), "--trials", "3"]), 0)
            self.assertEqual(main([*args, "results"]), 0)
        stored = RunStore(database).get(run["id"])
        self.assertEqual(stored["experiment"], definition("GRV-0002"))
        self.assertEqual(stored["runtime"]["gravitas"], "0.1.0")
        self.assertIn("Finite-disk", report.read_text(encoding="utf-8"))
        self.assertEqual(len(RunStore(database).results()), 2)


if __name__ == "__main__":
    unittest.main()
