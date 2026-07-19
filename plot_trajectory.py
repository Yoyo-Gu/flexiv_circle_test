"""Plot local trajectories before connecting to a robot."""

from __future__ import annotations

import os
from pathlib import Path

_MPL_CONFIG_DIR = Path(__file__).resolve().parent / ".matplotlib-cache"
_MPL_CONFIG_DIR.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_MPL_CONFIG_DIR))

import matplotlib.pyplot as plt
import numpy as np


def plot_xy_trajectory(
    points: np.ndarray,
    title: str,
    output_path: str | Path | None = None,
    show: bool = False,
) -> None:
    """Plot the x-y projection of a trajectory."""
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points must have shape (N, 3)")

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(points[:, 0], points[:, 1], marker=".", markersize=3, linewidth=1.5)
    ax.scatter(points[0, 0], points[0, 1], color="green", label="start", zorder=3)
    ax.scatter(points[-1, 0], points[-1, 1], color="red", label="end", zorder=3)

    ax.set_title(title)
    ax.set_xlabel("x / m")
    ax.set_ylabel("y / m")
    ax.axis("equal")
    ax.grid(True)
    ax.legend()

    if output_path is not None:
        fig.savefig(output_path, dpi=150, bbox_inches="tight")

    if show:
        backend = plt.get_backend().lower()
        interactive_backends = ("qt", "tk", "gtk", "wx", "macosx", "nbagg", "ipympl")
        if any(name in backend for name in interactive_backends):
            plt.show()
        else:
            print(
                f"[info] matplotlib backend '{plt.get_backend()}' is non-interactive; "
                "skipping window display."
            )

    plt.close(fig)
