from osintbot.core.models import Findings, Investigation, Target
from osintbot.core.source import OSINTSource

class InvestigationEngine:
    """Cords OSINT sources for investigation"""

    def __init__(self, sources: list[OSINTSource]) -> None:
        self.sources = sources

    def investigate(
            self,
            investigation: Investigation,
    ) -> Investigation:
        """run compatible sources against investigation targets"""

        for target in investigation.targets:
            for source in self.sources:
                if not source.supports(target):
                    continue

                findings = source.search(target)

                for finding in findings:
                    investigation.add_finding(finding)

        return investigation
