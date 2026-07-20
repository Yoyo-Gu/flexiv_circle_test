"""Robot control interface design for future Flexiv RDK integration.

This module is stage-5 scaffolding only. It is safe to import in WSL because it
does not import ``flexivrdk`` at module import time and does not connect to a
real robot unless ``FlexivRobotController.connect()`` is called explicitly.

The local trajectory code currently generates points shaped as ``[x, y, z]``.
When connected to a real robot, those points will be expanded to full TCP poses:
``[x, y, z, q_w, q_x, q_y, q_z]`` by reusing the current TCP orientation.
"""

from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Any, Sequence

import numpy as np


Pose7 = list[float]


@dataclass(frozen=True)
class RobotConnectionConfig:
    """Connection settings for a Flexiv robot.

    Flexiv RDK Python examples connect by robot serial number, not by robot IP.
    Network/IP setup is still required on the lab computer before this can work.
    """

    robot_sn: str
    command_frequency_hz: int = 20
    operational_timeout_s: float = 120.0

    def __post_init__(self) -> None:
        if not self.robot_sn:
            raise ValueError("robot_sn cannot be empty")
        if not 1 <= self.command_frequency_hz <= 100:
            raise ValueError("command_frequency_hz must be in [1, 100]")
        if self.operational_timeout_s <= 0:
            raise ValueError("operational_timeout_s must be greater than 0")


class FlexivRobotController:
    """Small wrapper around the Flexiv RDK control steps used by this project.

    Current stage:
        The class defines the API and the future RDK call order.

    Future real-robot stage:
        1. connect()
        2. clear_fault_if_any()
        3. enable()
        4. read_current_tcp_pose()
        5. send_cartesian_trajectory(points)
        6. stop()
    """

    def __init__(self, config: RobotConnectionConfig) -> None:
        self.config = config
        self._rdk: Any | None = None
        self._robot: Any | None = None
        self._single_arm_groups: dict[Any, Any] = {}

    @property
    def connected(self) -> bool:
        """Whether a real Flexiv RDK robot object has been created."""

        return self._robot is not None

    def connect(self) -> None:
        """Create the real RDK robot object.

        This method is intentionally not called automatically. On a personal WSL
        machine it should normally be left unused. Run it only on the lab
        computer after network setup, First Time Setup, and RDK installation.
        """

        if self.connected:
            return

        import flexivrdk  # type: ignore[import-not-found]

        self._rdk = flexivrdk
        self._robot = flexivrdk.Robot(self.config.robot_sn)

    def clear_fault_if_any(self) -> None:
        """Check robot fault state and clear it if possible."""

        robot = self._require_robot()
        if robot.fault():
            if not robot.ClearFault():
                raise RuntimeError("Flexiv robot fault cannot be cleared")

    def enable(self) -> None:
        """Servo on the robot and wait until it becomes operational."""

        robot = self._require_robot()
        robot.ServoOn()

        deadline = time.monotonic() + self.config.operational_timeout_s
        while not robot.operational():
            if time.monotonic() > deadline:
                raise TimeoutError("Timed out waiting for robot to become operational")
            time.sleep(1.0)

    def prepare_for_cartesian_motion(self) -> None:
        """Switch to non-real-time Cartesian pure motion control mode."""

        rdk = self._require_rdk()
        robot = self._require_robot()
        self._single_arm_groups = dict(robot.info().single_arm_groups)
        if not self._single_arm_groups:
            raise RuntimeError("No single-arm joint group found on the connected robot")

        robot.SwitchMode(rdk.Mode.NRT_CARTESIAN_MOTION_FORCE)
        for group in self._single_arm_groups:
            robot.SetForceControlAxis(group, [False, False, False, False, False, False])

    def read_states(self) -> dict[Any, Any]:
        """Return robot states keyed by joint group."""

        return self._require_robot().states()

    def read_current_tcp_pose(self, group: Any | None = None) -> Pose7:
        """Read current TCP pose for one single-arm group.

        The returned pose format follows Flexiv RDK examples:
        ``[x, y, z, q_w, q_x, q_y, q_z]`` in meters and quaternion orientation.
        """

        if not self._single_arm_groups:
            self.prepare_for_cartesian_motion()

        selected_group = group if group is not None else next(iter(self._single_arm_groups))
        states_by_group = self.read_states()
        if selected_group not in states_by_group:
            raise RuntimeError("Selected joint group has no robot state")

        return list(states_by_group[selected_group].tcp_pose)

    def send_cartesian_trajectory(
        self,
        points_xyz: np.ndarray | Sequence[Sequence[float]],
        *,
        group: Any | None = None,
        reference_pose: Sequence[float] | None = None,
    ) -> None:
        """Send local ``[x, y, z]`` points as TCP pose commands.

        Position comes from ``points_xyz``. Orientation is copied from
        ``reference_pose`` or, if omitted, from the current TCP pose.
        """

        rdk = self._require_rdk()
        robot = self._require_robot()
        points = _normalize_points_xyz(points_xyz)

        if not self._single_arm_groups:
            self.prepare_for_cartesian_motion()

        selected_group = group if group is not None else next(iter(self._single_arm_groups))
        base_pose = (
            list(reference_pose)
            if reference_pose is not None
            else self.read_current_tcp_pose(selected_group)
        )
        if len(base_pose) != 7:
            raise ValueError("reference_pose must have length 7")

        period = 1.0 / self.config.command_frequency_hz
        for point in points:
            if robot.fault():
                raise RuntimeError("Fault occurred while sending Cartesian trajectory")

            target_pose = base_pose.copy()
            target_pose[0:3] = point.tolist()
            robot.SendCartesianMotionForce(
                {selected_group: rdk.NrtCartesianCmd(target_pose)}
            )
            time.sleep(period)

    def stop(self) -> None:
        """Stop robot motion and put the robot into IDLE mode."""

        if self._robot is not None:
            self._robot.Stop()

    def _require_rdk(self) -> Any:
        if self._rdk is None:
            raise RuntimeError("Flexiv RDK is not loaded. Call connect() first.")
        return self._rdk

    def _require_robot(self) -> Any:
        if self._robot is None:
            raise RuntimeError("Robot is not connected. Call connect() first.")
        return self._robot


class DryRunRobotController:
    """Local-only controller used to verify code flow without a real robot."""

    def __init__(
        self,
        initial_tcp_pose: Sequence[float] = (0.3, 0.0, 0.4, 1.0, 0.0, 0.0, 0.0),
    ) -> None:
        if len(initial_tcp_pose) != 7:
            raise ValueError("initial_tcp_pose must have length 7")
        self._tcp_pose = list(initial_tcp_pose)
        self.sent_poses: list[Pose7] = []

    def connect(self) -> None:
        """Dry-run connect placeholder."""

    def clear_fault_if_any(self) -> None:
        """Dry-run fault clear placeholder."""

    def enable(self) -> None:
        """Dry-run enable placeholder."""

    def prepare_for_cartesian_motion(self) -> None:
        """Dry-run Cartesian mode placeholder."""

    def read_states(self) -> dict[str, Pose7]:
        """Return minimal fake state information for local inspection."""

        return {"dry_run": self.read_current_tcp_pose()}

    def read_current_tcp_pose(self, group: Any | None = None) -> Pose7:
        """Return the fake TCP pose."""

        return self._tcp_pose.copy()

    def send_cartesian_trajectory(
        self,
        points_xyz: np.ndarray | Sequence[Sequence[float]],
        *,
        group: Any | None = None,
        reference_pose: Sequence[float] | None = None,
    ) -> None:
        """Convert points into full TCP poses and store them locally."""

        points = _normalize_points_xyz(points_xyz)
        base_pose = (
            list(reference_pose)
            if reference_pose is not None
            else self.read_current_tcp_pose(group)
        )
        if len(base_pose) != 7:
            raise ValueError("reference_pose must have length 7")

        self.sent_poses.clear()
        for point in points:
            pose = base_pose.copy()
            pose[0:3] = point.tolist()
            self.sent_poses.append(pose)

        if self.sent_poses:
            self._tcp_pose = self.sent_poses[-1].copy()

    def stop(self) -> None:
        """Dry-run stop placeholder."""


def _normalize_points_xyz(
    points_xyz: np.ndarray | Sequence[Sequence[float]],
) -> np.ndarray:
    """Validate and return trajectory points as a floating ``(N, 3)`` array."""

    points = np.asarray(points_xyz, dtype=float)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points_xyz must have shape (N, 3)")
    if len(points) == 0:
        raise ValueError("points_xyz cannot be empty")
    if not np.isfinite(points).all():
        raise ValueError("points_xyz must contain only finite values")
    return points


def preview_send_trajectory(points_xyz: np.ndarray | Sequence[Sequence[float]]) -> list[Pose7]:
    """Run the future send flow locally and return generated TCP poses."""

    controller = DryRunRobotController()
    controller.connect()
    controller.clear_fault_if_any()
    controller.enable()
    controller.prepare_for_cartesian_motion()
    reference_pose = controller.read_current_tcp_pose()
    controller.send_cartesian_trajectory(points_xyz, reference_pose=reference_pose)
    controller.stop()
    return controller.sent_poses
