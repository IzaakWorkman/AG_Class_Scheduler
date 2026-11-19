"""Tkinter GUI (optional, +5). Run from the repo root with: python -m gui.app

The engine runs on a background thread and puts each GenerationStats on a queue;
the window reads the queue on a timer, so it never freezes.
"""

import tkinter as tk
from queue import Queue

from sla_ga.engine import GAEngine, GenerationStats
from sla_ga.report import Reporter


class App:
    """The main window: control panels on one side, result tabs on the other."""

    def __init__(self, root: tk.Tk) -> None:
        """Store the root window, build the controls and tabs, start poll_queue."""
        self._root: tk.Tk
        self._engine: GAEngine | None
        self._stats_queue: Queue[GenerationStats]
        self._reporter: Reporter | None
        raise NotImplementedError

    def build_controls(self) -> None:
        """Panels with title-case labels:
        Run Settings (Population Size, Random Seed, Max Generations, Pairing Method,
            Crossover Method, Softmax Temperature)
        Mutation (Mutation Rate, Halve Rate, Auto Halve, Mutation Rate Tracker)
        Optional Rules (Room Size Scaling, Time Preferences, Equipment Requirements)
        Run Controls (Start, Pause / Resume, Step One Generation, Stop, Reset)"""
        raise NotImplementedError

    def build_tabs(self) -> None:
        """Tabs: Fitness Over Generations, Fitness Matrix, Schedule, Constraint Violations,
        Course Load, Room Utilization; plus the status bar (Generation, Best Fitness,
        Improvement, Stop Reason)."""
        raise NotImplementedError

    def validate_inputs(self) -> bool:
        """Highlight bad fields and keep Start disabled until all pass:
        Population Size >= 250 and a multiple of 4, 0 < Mutation Rate <= 1,
        Softmax Temperature > 0, Max Generations >= 100. Returns True if all pass."""
        raise NotImplementedError

    def start_run(self) -> None:
        """Build the GAEngine and its Reporter (Shared Definitions 6), add a listener that
        puts each GenerationStats on the queue, and run the engine on a background thread.
        When the run ends, call write_best and close."""
        raise NotImplementedError

    def poll_queue(self) -> None:
        """Every ~100 ms: take new stats from the queue and update labels, tables and charts
        (charts redraw at most every 200 ms)."""
        raise NotImplementedError


def main() -> None:
    """Open the window and run the Tkinter event loop."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
