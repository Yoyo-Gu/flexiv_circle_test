"""Generate and plot local drawing trajectories.

This program is for local validation only. It does not connect to the Flexiv
robot and does not send any robot motion command.
"""

from __future__ import annotations

import argparse

from config import CIRCLE_CENTER, CIRCLE_POINTS, CIRCLE_RADIUS, DEFAULT_OUTPUT
from plot_trajectory import plot_xy_trajectory
from trajectory import generate_circle, summarize_points


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a local trajectory for robot drawing."
    )
    parser.add_argument(
        "--shape",
        choices=("circle",),
        default="circle",
        help="Trajectory shape to generate. Currently only circle is supported.",
    )
    parser.add_argument(
        "--radius",
        type=float,
        default=CIRCLE_RADIUS,
        help="Circle radius in meters.",
    )
    parser.add_argument(
        "--points",
        type=int,
        default=CIRCLE_POINTS,
        help="Number of generated points.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Path of the saved trajectory image.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show the matplotlib window in addition to saving the image.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.shape == "circle":
        points = generate_circle(
            center=CIRCLE_CENTER,
            radius=args.radius,
            num_points=args.points,
        )
        title = "Circle TCP trajectory preview"
    else:
        raise ValueError(f"unsupported shape: {args.shape}")

    summary = summarize_points(points)
    plot_xy_trajectory(points, title=title, output_path=args.output, show=args.show)

    print(f"shape: {args.shape}")
    print(f"point count: {len(points)}")
    print(f"center xyz / m: {CIRCLE_CENTER}")
    print(f"radius / m: {args.radius}")
    print(f"first point: {summary['first_point']}")
    print(f"last point: {summary['last_point']}")
    print(f"min xyz: {summary['min_xyz']}")
    print(f"max xyz: {summary['max_xyz']}")
    print(f"closed error / m: {summary['closed_error']:.12f}")
    print(f"saved plot: {args.output}")


if __name__ == "__main__":
    main()
