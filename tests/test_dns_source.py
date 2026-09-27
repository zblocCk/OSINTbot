from unittest.mock import MagicMock, patch
from dns.resolver import NoAnswer
from osintbot.core.models import Target, TargetType
from osintbot.sources.dns.source import DNSSource

def test_dns_source_supports_domains():
    source = DNSSource()

    domain = Target(
        value="example.com",
        target_type=TargetType.DOMAIN,
    )
    email = Target(
        value="user@example.com",
        target_type=TargetType.EMAIL,
    )

    assert source.supports(domain)
    assert not source.supports(email)

@patch("osintbot.sources.dns.source.dns.resolver.Resolver")
def test_dns_source_returns_records(mock_resolver):
    resolver = mock_resolver.return_value

    a_answer = MagicMock()
    a_answer.to_text.return_value = "93.184.216.34"

    mx_answer = MagicMock()
    mx_answer.to_text.return_value = "10 mail.example.com"

    def fake_resolve(domain, record_type):
        if record_type == "A":
            return [a_answer]

        if record_type == "MX":
            return [mx_answer]

        raise NoAnswer()
    resolver.resolve.side_effect = fake_resolve
    source = DNSSource()
    target = Target(
        value="example.com",
        target_type=TargetType.DOMAIN,
    )
    findings = source.search(target)

    assert len(findings) == 2
    assert findings[0].title == "DNS A record"
    assert findings[0].confidence.value == "high"
    assert findings[1].title == "DNS MX record"
