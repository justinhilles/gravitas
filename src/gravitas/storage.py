"""SQLite persistence for successful, rejected and failed research runs."""

import json
import platform
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from . import __version__


class RunStore:
    def __init__(self, path):
        self.path = Path(path)

    def connect(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    experiment_id TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    status TEXT NOT NULL,
                    experiment TEXT NOT NULL,
                    result TEXT NOT NULL,
                    runtime TEXT NOT NULL
                )
            """)
        return connection

    def save(self, experiment, kind, status, result):
        run_id = str(uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        runtime = {"gravitas": __version__, "python": platform.python_version(),
                   "platform": platform.platform()}
        with closing(self.connect()) as connection, connection:
            connection.execute(
                "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (run_id, timestamp, experiment["id"], kind, status,
                 json.dumps(experiment, allow_nan=False),
                 json.dumps(result, allow_nan=False), json.dumps(runtime))
            )
        return run_id

    def results(self):
        with closing(self.connect()) as connection:
            return [dict(row) for row in connection.execute(
                "SELECT id, created_at, experiment_id, kind, status FROM runs "
                "ORDER BY created_at DESC, id"
            )]

    def get(self, run_id):
        with closing(self.connect()) as connection:
            row = connection.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
        if row is None:
            raise ValueError(f"unknown run ID {run_id}")
        result = dict(row)
        for key in ("experiment", "result", "runtime"):
            result[key] = json.loads(result[key])
        return result
