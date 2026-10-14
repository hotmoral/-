from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import hypot, isfinite
from typing import Dict, List


@dataclass(frozen=True)
class Vec2:
    x: float
    y: float

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vec2":
        return Vec2(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__

    def length(self) -> float:
        return hypot(self.x, self.y)

    def finite(self) -> bool:
        return isfinite(self.x) and isfinite(self.y)


@dataclass(frozen=True)
class Rect:
    left: float
    top: float
    right: float
    bottom: float

    @property
    def width(self) -> float:
        return max(0.0, self.right - self.left)

    @property
    def height(self) -> float:
        return max(0.0, self.bottom - self.top)

    @property
    def area(self) -> float:
        return self.width * self.height

    def expand(self, pad: float) -> "Rect":
        return Rect(self.left - pad, self.top - pad, self.right + pad, self.bottom + pad)

    def union(self, other: "Rect") -> "Rect":
        return Rect(
            min(self.left, other.left),
            min(self.top, other.top),
            max(self.right, other.right),
            max(self.bottom, other.bottom),
        )

    def contains(self, other: "Rect", eps: float = 1e-9) -> bool:
        return (
            self.left <= other.left + eps
            and self.top <= other.top + eps
            and self.right + eps >= other.right
            and self.bottom + eps >= other.bottom
        )


def rect_from_points(points: List[Vec2], pad: float = 0.0) -> Rect:
    if not points:
        raise ValueError("points required")
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    return Rect(min(xs)-pad, min(ys)-pad, max(xs)+pad, max(ys)+pad)


class Phase(str, Enum):
    CONTACT = "CONTACT"
    SWING = "SWING"
    FREE = "FREE"


class ContactKind(str, Enum):
    PAW_POINT = "PAW_POINT"
    BODY_PATCH = "BODY_PATCH"


@dataclass(frozen=True)
class ContactSite:
    id: str
    kind: ContactKind
    owner: str
    phase: Phase
    load_bearing: bool
    point: Vec2
    tangent_extent_dp: float = 0.0
    support_geometry_id: str = "GROUND"
    target_point: Vec2 | None = None


@dataclass(frozen=True)
class Morphology:
    id: str
    head_scale: float = 1.0
    trunk_length: float = 1.0
    trunk_depth: float = 1.0
    forequarter_scale: float = 1.0
    pelvis_scale: float = 1.0
    fore_limb_length: float = 1.0
    hind_limb_length: float = 1.0
    paw_scale: float = 1.0
    ear_scale: float = 1.0
    tail_length: float = 1.0
    tail_thickness: float = 1.0

    def validate(self) -> None:
        for key, value in self.__dict__.items():
            if key == "id":
                continue
            if not isfinite(value) or value <= 0:
                raise ValueError(f"invalid morphology {key}={value}")

    @staticmethod
    def blend(a: "Morphology", b: "Morphology", t: float, id: str) -> "Morphology":
        if not 0.0 <= t <= 1.0:
            raise ValueError("t must be [0,1]")
        values = {}
        for key, av in a.__dict__.items():
            if key == "id":
                continue
            values[key] = av * (1.0 - t) + getattr(b, key) * t
        return Morphology(id=id, **values)


M0 = Morphology(id="M0_NEUTRAL_V01")
M1 = Morphology(
    id="M1_KITTEN_STRESS_V01",
    head_scale=1.22,
    trunk_length=0.82,
    trunk_depth=0.94,
    forequarter_scale=0.90,
    pelvis_scale=0.90,
    fore_limb_length=0.82,
    hind_limb_length=0.84,
    paw_scale=1.08,
    ear_scale=1.10,
    tail_length=0.84,
    tail_thickness=0.90,
)
M2 = Morphology(
    id="M2_ADULT_STRESS_V01",
    head_scale=0.94,
    trunk_length=1.14,
    trunk_depth=1.06,
    forequarter_scale=1.06,
    pelvis_scale=1.08,
    fore_limb_length=1.12,
    hind_limb_length=1.14,
    paw_scale=1.00,
    ear_scale=0.98,
    tail_length=1.12,
    tail_thickness=1.05,
)

MANDATORY_ANCHORS = (
    "BODY_ROOT",
    "FOREQUARTER_REF",
    "PELVIS_REF",
    "HEAD_ROOT",
    "TAIL_ROOT",
    "FORE_PAW_L",
    "FORE_PAW_R",
    "HIND_PAW_L",
    "HIND_PAW_R",
)


@dataclass
class BodyPoseState:
    candidate: str
    morphology_id: str
    case_id: str
    t: float
    size_dp: float
    anchors: Dict[str, Vec2]
    contacts: List[ContactSite]
    support_set: List[str]
    visual_bounds: Rect
    body_bounds: Rect
    window_bounds: Rect
    shapes: List[dict] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def validate(self) -> List[str]:
        errors: List[str] = []
        for name in MANDATORY_ANCHORS:
            if name not in self.anchors:
                errors.append(f"missing_anchor:{name}")
            elif not self.anchors[name].finite():
                errors.append(f"nonfinite_anchor:{name}")
        if not self.window_bounds.contains(self.visual_bounds):
            errors.append("window_not_contain_visual")
        contact_map = {contact.id: contact for contact in self.contacts}
        for support_id in self.support_set:
            contact = contact_map.get(support_id)
            if contact is None:
                errors.append(f"support_missing_contact:{support_id}")
            elif contact.phase != Phase.CONTACT or not contact.load_bearing:
                errors.append(f"invalid_support_member:{support_id}")
        if not self.support_set:
            errors.append("zero_support")
        for contact in self.contacts:
            if not contact.point.finite():
                errors.append(f"nonfinite_contact:{contact.id}")
        return errors
