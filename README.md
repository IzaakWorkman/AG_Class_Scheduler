# SLA Activity Scheduler: Genetic Algorithm

CS 461 Program 2. A genetic algorithm that builds an activity schedule for the
Seminar Learning Association (SLA). Each of the 11 activities is assigned a room,
a time slot and a facilitator. Schedules are scored with the Appendix A fitness
rubric and improved over generations.

## How It Works

- A schedule is an 11 × 3 NumPy integer array: one row per activity, holding
  `[room, time, facilitator]` as index numbers. A population is N × 11 × 3
  (default N = 252).
- Generation 0 is random. Each generation keeps the best half as parents, pairs
  them by softmax probability and builds two children per pair with crossover.
  Only the children are mutated, each room, time and facilitator separately at
  the mutation rate. The next population is the best half plus the children.
- A run lasts at least 100 generations. After that it stops once average fitness
  improves by less than 1% from one generation to the next.
- All facts (rooms, activities, facilitators) are in `data/sla_catalog.json`. All
  point values and thresholds are in `data/scoring.json`.

## Requirements

- Python 3.14.8
- The packages in `requirements.txt`: numpy, scipy, matplotlib, plotext
- Tkinter for the GUI (included with the standard Python installers)

## Setup

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running

### Command Line

```bash
python cli.py --seed 42
```

Each generation prints one line: generation, best, average and worst fitness,
improvement % and mutation rate. At the end the program prints the best schedule
and a chart of best, average and worst fitness over the generations.

| Flag | Values | Default |
| --- | --- | --- |
| `--pop` | Population size: at least 250 and a multiple of 4 | 252 |
| `--seed` | Any integer | Random (printed and saved) |
| `--mutation` | Mutation rate, greater than 0 and at most 1 | 0.01 |
| `--temperature` | Softmax temperature, greater than 0 | 1.0 |
| `--pairing` | `softmax`, `tournament`, `random` | `softmax` |
| `--crossover` | `single_point`, `uniform` | `single_point` |
| `--max-gen` | Generation cap, at least 100 | 1000 |
| `--auto-halve` | Halve the mutation rate instead of stopping | Off |
| `--show` | `first6`, `all` | `first6` |
| `--sort` | `time`, `activity` | `time` |
| `--group` | `none`, `building`, `facilitator` | `none` |
| `--rules` | Optional rules, comma-separated: `scaling`, `timepref`, `equipment` | None |

### Mutation Rate Sweep

Runs the GA for every rate and seed, then writes `mutation_sweep.csv` and a chart:

```bash
python cli.py sweep --rates 0.01,0.005,0.0025 --seeds 1,2,3,4,5
```

### GUI

```bash
python -m gui.app
```

The window has controls for run settings, mutation rate and optional rules, and
live tabs for fitness, the schedule, constraint violations, course load and
room utilization.

## Output

Every run writes to its own folder, `output/run_<YYYYMMDD-HHMMSS>_seed<seed>/`:

| File | Contents |
| --- | --- |
| `best_schedule.txt` | Best fitness, seed, settings, stop reason, the best schedule and its violation counts |
| `fitness_history.csv` | One row per generation: best, average, worst, improvement %, mutation rate and violation counts |
| `run.log` | A timestamped line per generation with the best fitness and schedule |

To repeat a run exactly, use the seed from its folder name.

## Project Layout

```
data/
  sla_catalog.json    rooms, times, facilitators and activities (facts only)
  scoring.json        every point value and threshold
sla_ga/
  types.py            shared type aliases and constants
  catalog.py          Catalog: loads and checks sla_catalog.json
  scoring.py          Scoring: loads and checks scoring.json
  config.py           GAConfig: every run setting
  schedule.py         random populations and a readable view of a schedule
  fitness.py          FitnessEvaluator: the Appendix A rules
  optional_rules.py   room-size scaling, time preferences, equipment
  operators.py        pairing, crossover and mutation
  engine.py           GAEngine: the generation loop
  report.py           Reporter: output files and schedule text
  experiments.py      mutation rate sweep
gui/
  app.py              Tkinter window
  charts.py           Matplotlib chart functions
cli.py                command-line entry point
```

## Changing the Fitness Function

To try different point values, copy `data/scoring.json`, change the numbers and
point `GAConfig.scoring_path` at the copy. The rule logic stays in `fitness.py`.