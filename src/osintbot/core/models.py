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

class Confidence(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

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
    confidence: Confidence = Confidence.LOW
    evidence: list[Evidence] = field(default_factory=list)
    observed_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

@dataclass
class Investigation:
    name: str
    targets: list[Target] = field(default_factory=list)
    findings: list[Findings] = field(default_factory=list)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def add_target(self, target: list[Target]) -> None:
        self.targets.append(target)

    def add_finding(self, finding: Findings) -> None:
        self.findings.append(finding)