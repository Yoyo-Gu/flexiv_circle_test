"""Pure trajectory generation functions.

This module does not import or call Flexiv RDK. It only generates points that
can be plotted locally and later converted into robot commands.
"""

from __future__ import annotations

import numpy as np


def generate_circle(
    center: tuple[float, float, float],
    radius: float,
    num_points: int,
) -> np.ndarray:
    """Generate a closed circle trajectory in the x-y plane.

    Args:
        center: Circle center as ``(x, y, z)`` in meters.
        radius: Circle radius in meters.
        num_points: Number of points along the circle, including the final
            repeated point that closes the trajectory.

    Returns:
        A ``(num_points, 3)`` array. Each row is ``[x, y, z]``.
    """
    if radius <= 0:
        raise ValueError("radius must be greater than 0")
    if num_points < 4:
        raise ValueError("num_points must be at least 4")

    center_x, center_y, center_z = center
    theta = np.linspace(0.0, 2.0 * np.pi, num_points)

    x = center_x + radius * np.cos(theta)
    y = center_y + radius * np.sin(theta)
    z = np.full_like(theta, center_z)

    return np.column_stack((x, y, z))


def summarize_points(points: np.ndarray) -> dict[str, np.ndarray | float]:
    """Return basic checks for a generated trajectory."""
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points must have shape (N, 3)")

    first_point = points[0]
    last_point = points[-1]
    closed_error = float(np.linalg.norm(first_point - last_point))

    return {
        "first_point": first_point,
        "last_point": last_point,
        "min_xyz": points.min(axis=0),
        "max_xyz": points.max(axis=0),
        "closed_error": closed_error,
    }
