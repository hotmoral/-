from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin

from model import M0, M1, M2, Morphology, Vec2


@dataclass(frozen=True)
class Vec3:
    """P1 v0.2 body-local point: +X forward, +Y dorsal/up, +Z anatomical left."""

    x: float
    y: float
    z: float

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vec3":
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    __rmul__ = __mul__


@dataclass(frozen=True)
class MorphologyV2:
    base: Morphology
    thorax_width_scale: float = 1.0
    pelvis_width_scale: float = 1.0
    stance_width_scale: float = 1.0

    @property
    def id(self) -> str:
        return self.base.id

    def validate(self) -> None:
        self.base.validate()
        for name, value in (
            ("thorax_width_scale", self.thorax_width_scale),
            ("pelvis_width_scale", self.pelvis_width_scale),
            ("stance_width_scale", self.stance_width_scale),
        ):
            if value <= 0.0:
                raise ValueError(f"invalid {name}={value}")


M0_V2 = MorphologyV2(M0)
M1_V2 = MorphologyV2(
    M1,
    thorax_width_scale=0.90,
    pelvis_width_scale=0.92,
    stance_width_scale=0.88,
)
M2_V2 = MorphologyV2(
    M2,
    thorax_width_scale=1.10,
    pelvis_width_scale=1.12,
    stance_width_scale=1.08,
)


def blend_morphology_v2(a: MorphologyV2, b: MorphologyV2, t: float, id: str) -> MorphologyV2:
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must be [0,1]")
    return MorphologyV2(
        Morphology.blend(a.base, b.base, t, id),
        thorax_width_scale=a.thorax_width_scale * (1.0 - t) + b.thorax_width_scale * t,
        pelvis_width_scale=a.pelvis_width_scale * (1.0 - t) + b.pelvis_width_scale * t,
        stance_width_scale=a.stance_width_scale * (1.0 - t) + b.stance_width_scale * t,
    )


def project_b3(
    point: Vec3,
    body_root_s: Vec2,
    scale_dp_per_bu: float,
    yaw_rad: float,
    tangent_s: Vec2 = Vec2(1.0, 0.0),
    normal_s: Vec2 = Vec2(0.0, -1.0),
) -> Vec2:
    """Orthographic 2.5D reference projection from P1 schema v0.2."""

    screen_t = point.x * cos(yaw_rad) + point.z * sin(yaw_rad)
    screen_n = point.y
    return Vec2(
        body_root_s.x + scale_dp_per_bu * (screen_t * tangent_s.x + screen_n * normal_s.x),
        body_root_s.y + scale_dp_per_bu * (screen_t * tangent_s.y + screen_n * normal_s.y),
    )


def yaw_label(yaw_rad: float) -> str:
    tau = 2.0 * pi
    yaw = yaw_rad % tau
    quarter = pi / 4.0
    if yaw < quarter or yaw >= tau - quarter:
        return "PROFILE_POS"
    if yaw < 3.0 * quarter:
        return "FRONT_INTERMEDIATE"
    if yaw < 5.0 * quarter:
        return "PROFILE_NEG"
    if yaw < 7.0 * quarter:
        return "BACK_INTERMEDIATE"
    return "PROFILE_POS"
