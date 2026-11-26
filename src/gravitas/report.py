"""Markdown rendering for stored runs."""

import json


def markdown(run):
    experiment = run["experiment"]
    result = run["result"]
    lines = [
        f"# {run['experiment_id']} — {experiment['name']}", "",
        f"Run {run['id']} | {run['kind']} | {run['status']} | {run['created_at']}", "",
        "## Hypothesis and prediction", "", experiment["hypothesis"], "",
        experiment["prediction"], "",
    ]
    if "observations" in result:
        lines.extend([
            "## Measurements", "",
            "| Location | Time (s) | Gravity (m/s²) | Electric field (V/m) | "
            "Magnetic field (T) | Sample magnetic force (N) |",
            "| --- | ---: | --- | --- | --- | --- |",
        ])

        def vector(value):
            return "—" if value is None else "(" + ", ".join(f"{x:.6g}" for x in value) + ")"

        for row in result["observations"]:
            label = row["measurement"].replace("|", r"\|").replace("\n", " ")
            lines.append(
                f"| {label} | {row['time_s']:g} | {vector(row['gravity_m_s2'])} | "
                f"{vector(row['electric_v_m'])} | {vector(row['magnetic_t'])} | "
                f"{vector(row['magnetic_sample_force_n'])} |"
            )
        lines.extend(["", "The field energy mass equivalent is a local energy conversion.",
                      "The Newtonian calculation uses component rest masses.", ""])
        disk_rows = [(row["measurement"], disk)
                     for row in result["observations"][:len(experiment["measurements"])]
                     for disk in row["disk_targets"]]
        if disk_rows:
            lines.extend(["## Required disk mass", "",
                          "| Location | Disk | Height (m) | 0.01g (kg) | Lunar (kg) | "
                          "Martian (kg) | Earth (kg) |", "| --- | --- | ---: | ---: | "
                          "---: | ---: | ---: |"])
            for location, disk in disk_rows:
                targets = " | ".join(f"{goal['mass_kg']:.6g}"
                                     for goal in disk["required"].values())
                lines.append(f"| {location} | {disk['component']} | "
                             f"{disk['height_m']:.6g} | {targets} |")
            lines.append("")
    if "analytical_checks" in result:
        lines.extend(["## Analytical checks", ""])
        for check in result["analytical_checks"]:
            status = "pass" if check["passed"] else "fail"
            lines.append(f"- {check['name']} — {status} "
                         f"(computed {check['actual']:.6g}, expected {check['expected']:.6g})")
        lines.append("")
    if "accepted" in result:
        lines.extend([f"{len(result['accepted'])} accepted, {len(result['rejected'])} rejected.",
                      "Rank 1 is the first Pareto front.", ""])
    if "error" in result:
        lines.extend(["## Rejection", "", result["error"], ""])
    lines.extend(["## Reproducibility", ""])
    for key in ("runtime", "experiment", "result"):
        lines.extend([f"### {key.title()}", "", "~~~json",
                      json.dumps(run[key], indent=2, ensure_ascii=False), "~~~", ""])
    return "\n".join(lines)
