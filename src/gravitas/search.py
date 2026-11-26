"""Reproducible uniform sampling and Pareto-front ranking."""

from copy import deepcopy
from random import Random

from .schema import METRICS, validate
from .simulation import simulation


def dominates(left, right, objectives):
    differences = [
        (left[key] - right[key]) * (1 if METRICS[key] == "maximize" else -1)
        for key in objectives
    ]
    return all(change >= 0 for change in differences) and any(
        change > 0 for change in differences
    )


def optimize(raw, trials):
    if not 1 <= trials <= 1000:
        raise ValueError("trials must be between 1 and 1000")
    spec = validate(raw)
    if not spec["adjustable"]:
        raise ValueError("experiment has no adjustable parameters")
    random = Random(spec["seed"])
    objectives = spec["objectives"]
    experiment = deepcopy(raw)
    components = {item["id"]: item for item in experiment["components"]}
    accepted, rejected = [], []
    for index in range(trials):
        choices = {}
        for component, parameter, low, high, integer in spec["adjustable"]:
            value = random.randint(low, high) if integer else random.uniform(low, high)
            components[component]["parameters"][parameter]["value"] = value
            choices.setdefault(component, {})[parameter] = value
        candidate = {"trial": index + 1, "parameters": choices}
        try:
            candidate["metrics"] = simulation(experiment)["metrics"]
        except ValueError as error:
            candidate["reason"] = str(error)
            rejected.append(candidate)
        else:
            accepted.append(candidate)
    counts = [0] * len(accepted)
    dominated = [[] for _ in accepted]
    for index, left in enumerate(accepted):
        for other_index in range(index + 1, len(accepted)):
            right = accepted[other_index]
            if dominates(left["metrics"], right["metrics"], objectives):
                dominated[index].append(other_index)
                counts[other_index] += 1
            elif dominates(right["metrics"], left["metrics"], objectives):
                dominated[other_index].append(index)
                counts[index] += 1
    front = [index for index, count in enumerate(counts) if count == 0]
    rank = 1
    while front:
        next_front = []
        for index in front:
            accepted[index]["rank"] = rank
            for other in dominated[index]:
                counts[other] -= 1
                if counts[other] == 0:
                    next_front.append(other)
        front = next_front
        rank += 1
    return {
        "algorithm": "seeded uniform sampling with Pareto ranks",
        "seed": spec["seed"],
        "objectives": {key: METRICS[key] for key in objectives},
        "accepted": sorted(accepted, key=lambda item: (item["rank"], item["trial"])),
        "rejected": rejected,
    }
