from osintbot.core.models import (
    Confidence,
    Findings,
    Target,
    TargetType,
)
from osintbot.core.source import OSINTSource

class FakeUserNameSource(OSINTSource):
    @property
    def name(self) -> str:
        return "Fake UserName source"

    def supports(self, target: Target) -> bool:
        return target.target_type == TargetType.USERNAME

    def search(self, target: Target) -> list[Findings]:
        return [
            Findings(
                target=target,
                title="Test username found",
                description=f"Found username {target.value}",
                confidence=Confidence.MEDIUM,
            )
        ]

def test_source_name():
    source = FakeUserNameSource()

    assert source.name == "Fake UserName source"

def test_source_supports_username():
    source = FakeUserNameSource()

    username = Target(
        value="example123",
        target_type=TargetType.USERNAME,
    )

    email =  Target(
        value="example@example.com",
        target_type=TargetType.EMAIL,
    )

    assert source.supports(username)
    assert not source.supports(email)

def test_source_returns_findings():
    source = FakeUserNameSource()

    target = Target(
        value="example123",
        target_type=TargetType.USERNAME,
    )

    findings = source.search(target)

    assert len(findings) == 1
    assert findings[0].target == target
    assert findings[0].confidence == Confidence.MEDIUM