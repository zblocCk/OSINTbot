from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

class TargetType(Enum):
    USERNAME = "username"
    EMAIL = "email"
    PHONE = "phone"
    DOMAIN = "domain"
    IP = "ip"
    URL = "url"
    IMAGE = "image"

@dataclass
class Target:
    value: str
    target_type: TargetType

@dataclass
class Evidence:
    source: str
    description: str
    url: str | None = None
    observed_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

@dataclass
class Findings:
    target: Target
    title: str
    description: str
    evidence: list[Evidence] = field(default_factory=list)