import dns.resolver
from osintbot.core.models import (
    Confidence,
    Evidence,
    Finding,
    Target,
    TargetType,
)
from osintbot.core.source import OSINTSource

class DNSSource(OSINTSource):
    """DNS reconnaissance source. Scout, search domains, etc."""
    RECORD_TYPES = (
        "A",
        "AAAA",
        "MX",
        "NS",
        "TXT",
    )

    @property
    def name(self) -> str:
        return "DNS"

    def supports(self, target: Target) -> bool:
        return target.target_type == TargetType.DOMAIN

    def search(self, target: Target) -> list[Finding]:
        findings: list[Finding] = []

        resolver = dns.resolver.Resolver()

        for record_type in self.RECORD_TYPES:
            try:
                answers = resolver.resolve(
                    target.value,
                    record_type,
                )
            except (
                dns.resolver.NXDOMAIN,
                dns.resolver.NoAnswer,
            ):
                continue

            for answer in answers:
                value = answer.to_text()

                findings.append(
                    Finding(
                        target=target,
                        title=f"DNS {record_type} record",
                        description=(
                            f"{target.value} has a"
                            f"{record_type} record: {value}"
                        ),
                        confidence=Confidence.HIGH,
                        evidence=[
                            Evidence(
                                source=self.name,
                                description=f"DNS {record_type} lookup "
                                f"returned {value}"
                            ),
                        ],
                    )
                )
        return findings