"""Generate and plot local drawing trajectories.

This program is for local validation only by default. ``--dry-run-robot`` uses a
fake controller to exercise the future robot-control path without connecting to
the Flexiv robot or sending any real motion command.
"""

from __future__ import annotations

import argparse

from config import CIRCLE_CENTER, CIRCLE_POINTS, CIRCLE_RADIUS, DEFAULT_OUTPUT
from plot_trajectory import plot_xy_trajectory
from robot_control import DryRunRobotController
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
    parser.add_argument(
        "--dry-run-robot",
        action="store_true",
        help="Use a fake robot TCP as the trajectory center and preview sent TCP poses.",
    )
    parser.add_argument(
        "--fake-tcp",
        type=float,
        nargs=7,
        metavar=("X", "Y", "Z", "QW", "QX", "QY", "QZ"),
        default=(0.3, 0.0, 0.4, 1.0, 0.0, 0.0, 0.0),
        help="Fake current TCP pose for --dry-run-robot.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    controller = None
    reference_pose = None
    center = CIRCLE_CENTER

    if args.dry_run_robot:
        controller = DryRunRobotController(args.fake_tcp)
        controller.connect()
        controller.clear_fault_if_any()
        controller.enable()
        controller.prepare_for_cartesian_motion()
        reference_pose = controller.read_current_tcp_pose()
        center = tuple(reference_pose[:3])

    if args.shape == "circle":
        points = generate_circle(
            center=center,
            radius=args.radius,
            num_points=args.points,
        )
        title = "Circle TCP trajectory preview"
    else:
        raise ValueError(f"unsupported shape: {args.shape}")

    summary = summarize_points(points)
    sent_poses = []
    if controller is not None:
        controller.send_cartesian_trajectory(points, reference_pose=reference_pose)
        controller.stop()
        sent_poses = controller.sent_poses

    plot_xy_trajectory(points, title=title, output_path=args.output, show=args.show)

    print(f"shape: {args.shape}")
    print(f"dry run robot: {args.dry_run_robot}")
    print(f"point count: {len(points)}")
    print(f"center xyz / m: {center}")
    print(f"radius / m: {args.radius}")
    print(f"first point: {summary['first_point']}")
    print(f"last point: {summary['last_point']}")
    print(f"min xyz: {summary['min_xyz']}")
    print(f"max xyz: {summary['max_xyz']}")
    print(f"closed error / m: {summary['closed_error']:.12f}")
    print(f"saved plot: {args.output}")
    if sent_poses:
        print(f"fake current TCP pose: {reference_pose}")
        print(f"preview sent pose count: {len(sent_poses)}")
        print(f"preview first sent pose: {sent_poses[0]}")
        print(f"preview last sent pose: {sent_poses[-1]}")


if __name__ == "__main__":
    main()
