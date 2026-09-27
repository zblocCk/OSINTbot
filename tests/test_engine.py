from unittest.mock import MagicMock, patch
from osintbot.core.engine import InvestigationEngine
from osintbot.core.models import (
    Confidence,
    Finding,
    Investigation,
    SourceStatus,
    Target,
    TargetType,
)
from osintbot.core.source import OSINTSource
from osintbot.sources.dns.source import DNSSource
from dns.resolver import NoAnswer

class FakeUsernameSource(OSINTSource):

    @property
    def name(self) -> str:
        return "fake user source"

    def supports(self, target: Target) -> bool:
        return target.target_type == TargetType.USERNAME

    def search(self, target: Target) -> list[Finding]:
        return [
            Finding(
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
    def search(self, target: Target) -> list[Finding]:
        return [
            Finding(
                target=target,
                title="test email found",
                description=f"Found email: {target.value}",
                confidence=Confidence.MEDIUM,
            )
        ]

class FailingSource(OSINTSource):
    @property
    def name(self) -> str:
        return "Failing source"
    def supports(self, target: Target) -> bool:
        return True
    def search(self, target: Target) -> list[Finding]:
        raise RuntimeError("Test source failure")

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

def test_engine_records_completed_execution():
    source = FakeUsernameSource()

    engine = InvestigationEngine(
        sources=[source]
    )
    investigation = Investigation(
        name="test investigation",
    )
    target = Target(
        value="example123",
        target_type=TargetType.USERNAME,
    )
    investigation.add_target(target)
    result = engine.investigate(investigation)

    assert len(result.executions) == 1
    assert result.executions[0].source == "fake user source"
    assert result.executions[0].status == SourceStatus.COMPLETED

def test_engine_records_skipped_source():
    source = FakeEmailSource()
    engine = InvestigationEngine(
        sources=[source]
    )
    investigation = Investigation(
        name="test investigation",
    )
    target = Target(
        value="example123",
        target_type=TargetType.USERNAME,
    )
    investigation.add_target(target)
    result = engine.investigate(investigation)

    assert len(result.executions) == 1
    assert result.executions[0].status == SourceStatus.SKIPPED

def test_engine_records_source_failure():
    source = FailingSource()
    engine = InvestigationEngine(
        sources=[source]
    )
    investigation = Investigation(
        name="test investigation",
    )
    target = Target(
        value="example123",
        target_type=TargetType.USERNAME,
    )
    investigation.add_target(target)
    result = engine.investigate(investigation)

    assert len(result.executions) == 1
    assert result.executions[0].status == SourceStatus.FAILED
    assert result.executions[0].error == "Test source failure"

@patch("osintbot.sources.dns.source.dns.resolver.Resolver")
def test_engine_runs_dns_source(mock_resolver):
    resolver = mock_resolver.return_value

    a_answer = MagicMock()
    a_answer.to_text.return_value = "93.184.216.34"

    def fake_resolve(domain, record_type):
        if record_type == "A":
            return [a_answer]
        raise NoAnswer()
    resolver.resolve.side_effect = fake_resolve

    engine = InvestigationEngine(
        sources=[DNSSource()]
    )
    investigation = Investigation(
        name="DNS integration test",
    )
    target = Target(
        value="example.com",
        target_type=TargetType.DOMAIN,
    )
    investigation.add_target(target)
    result = engine.investigate(investigation)

    assert len(result.findings) == 1
    assert result.findings[0].title == "DNS A record"

    assert len(result.executions) == 1
    assert result.executions[0].source == "DNS"
    assert result.executions[0].status == SourceStatus.COMPLETED