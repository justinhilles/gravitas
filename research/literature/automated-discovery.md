# Automated experimental design

Quanta's overview describes using algorithms to search experimental designs that researchers might overlook. It motivates preserving interpretable designs and checking calculated performance against real experimental constraints. [Quanta overview](https://www.quantamagazine.org/ai-comes-up-with-bizarre-physics-experiments-but-they-work-20250721/)

PyTheus encodes quantum optical experiments in weighted graphs. Its search varies continuous optical properties and discrete structure, then reduces graph complexity while retaining the target behavior. Gravitas can borrow the representation and constraint strategy once it has validated component composition rules. [PyTheus paper](https://arxiv.org/abs/2210.09980)

Urania uses hybrid global and local optimization over interferometric configurations to identify candidate gravitational-wave detector layouts. Its objective concerns detector sensitivity and its results need additional engineering checks before deployment. This suggests a separate Gravitas objective for sensitivity to deviations from the baseline. [Urania paper](https://doi.org/10.1103/PhysRevX.15.021012)

AI Feynman uses physical structure, including symmetry and separability, to aid symbolic regression. A Gravitas extension could propose interpretable relations from data and test them against independent held-out predictions, dimensional constraints and controls. [AI Feynman paper](https://doi.org/10.1126/sciadv.aay2631)

Uniform seeded search is the first comparison baseline. Population-based evolutionary search and graph topology changes belong in later model comparisons, where compute budgets and independent validation can distinguish useful designs from artifacts.
