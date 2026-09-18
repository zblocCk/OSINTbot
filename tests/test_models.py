from osintbot.core.models import (
    Evidence,
    Findings,
    Target,
    TargetType,
)

def test_create_username_target():
    target = Target(
        value = "example123",
        target_type = TargetType.USERNAME,
    )

    assert target.value == "example123"
    assert target.target_type == TargetType.USERNAME

def test_create_findings():
    target = Target(
        value = "example123",
        target_type = TargetType.USERNAME,
    )

    evidence = Evidence(
        source = "TestSource",
        description = "Test profile found",
        url="https://example.com/example123",
    )

    findings = Findings(
        target = target,
        title = "Test findings",
        description = "A test findings",
        evidence = [evidence],
    )

    assert findings.target == target
    assert len(findings.evidence) == 1