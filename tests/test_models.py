from osintbot.core.models import (
    Evidence,
    Findings,
    Target,
    TargetType,
    Investigation,
    Confidence,
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

def test_investigation_can_contain_targets():
    investigation = Investigation(
        name = "Test investigation",
    )

    target = Target(
        value = "example123",
        target_type = TargetType.USERNAME,
    )

    investigation.add_target(target)

    assert investigation.name == "Test investigation"
    assert len(investigation.targets) == 1
    assert investigation.targets[0] == target

def test_finding_has_confidence():
    target = Target(
        value = "example123",
        target_type = TargetType.USERNAME,
    )

    findings = Findings(
        target = target,
        title = "possible profile",
        description = "A matching public profile observed",
        confidence = Confidence.MEDIUM,
    )

    assert findings.confidence == Confidence.MEDIUM