from osintbot.core.engine import InvestigationEngine
from osintbot.core.models import (
    Confidence,
    Findings,
    Investigation,
    Target,
    TargetType,
)
from osintbot.core.source import OSINTSource

class FakeUsernameSource(OSINTSource):

    @property
    def name(self) -> str:
        return "fake user source"

    def supports(self, target: Target) -> bool:
        return target.target_type == TargetType.USERNAME

    def search(self, target: Target) -> list[Findings]:
        return [
            Findings(
                target=target,
                title="fake user found",
                description=f"Found user: {target.value}",
                confidence=Confidence.MEDIUM,
            )
        ]

class FakeEmailSource(OSINTSource):
    @property
    def name(self) -> str:
        return "fake email source"
    def supports(self, target: Target) -> bool:
        return target.target_type == TargetType.EMAIL
    def search(self, target: Target) -> list[Findings]:
        return [
            Findings(
                target=target,
                title="test email found",
                description=f"Found email: {target.value}",
                confidence=Confidence.MEDIUM,
            )
        ]

def test_engine_runs_compatible_sources():
    username_source = FakeUsernameSource()
    email_source = FakeEmailSource()

    engine = InvestigationEngine(
        sources=[
            username_source,
            email_source,
        ]
    )
    investigation = Investigation(
        name="test investigation",
    )

    username = Target(
        value="example123",
        target_type=TargetType.USERNAME,
    )

    investigation.add_target(username)

    result = engine.investigate(investigation)

    assert len(result.findings) == 1
    assert result.findings[0].title == "fake user found"

def test_engine_skips_incompatible_sources():
    email_source = FakeEmailSource()

    engine = InvestigationEngine(
        sources=[email_source],
    )
    investigation = Investigation(
        name="test investigation",
    )
    username = Target(
        value="example123",
        target_type=TargetType.USERNAME,
    )

    investigation.add_target(username)
    result = engine.investigate(investigation)

    assert len(result.findings) == 0