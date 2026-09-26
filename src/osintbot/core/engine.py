from osintbot.core.models import (
    Investigation,
    SourceExecution,
    SourceStatus,
)
from osintbot.core.source import OSINTSource

class InvestigationEngine:
    """cords OSINT sources for an investigation"""
    def __init__(self, sources: list[OSINTSource]) -> None:
        self.sources = sources

    def investigate(
            self,
            investigation: Investigation,
    ) -> Investigation:
        """run all compatible sources against all targets"""
        for target in investigation.targets:
            for source in self.sources:

                if not source.supports(target):
                    investigation.add_execution(
                        SourceExecution(
                            source=source.name,
                            status=SourceStatus.SKIPPED,
                        )
                    )
                    continue

                try:
                    findings = source.search(target)

                    for finding in findings:
                        investigation.add_finding(finding)

                    investigation.add_execution(
                        SourceExecution(
                            source=source.name,
                            status=SourceStatus.COMPLETED,
                            findings=findings,
                        )
                    )

                except Exception as error:
                    investigation.add_execution(
                        SourceExecution(
                            source=source.name,
                            status=SourceStatus.FAILED,
                            error=str(error),
                        )
                    )

        return investigation