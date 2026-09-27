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

class SourceStatus(Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

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
class Finding:
    target: Target
    title: str
    description: str
    confidence: Confidence = Confidence.LOW
    evidence: list[Evidence] = field(default_factory=list)
    observed_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

@dataclass
class SourceExecution:
    source: str
    status: SourceStatus
    findings: list[Finding] = field(default_factory=list)
    error: str | None = None

@dataclass
class Investigation:
    name: str
    targets: list[Target] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    executions: list[SourceExecution] = field(default_factory=list)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def add_target(self, target: list[Target]) -> None:
        self.targets.append(target)

    def add_finding(self, finding: Finding) -> None:
        self.findings.append(finding)

    def add_execution(self, execution: SourceExecution) -> None:
        self.executions.append(execution)