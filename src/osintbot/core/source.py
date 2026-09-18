from abc import ABC, abstractmethod
from osintbot.core.models import Findings, Target

class OSINTSource:
    """
    base interface for OSINT findings
    every source must accept a target and return list of findings
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """human readable name of the source"""
        raise NotImplementedError

    @abstractmethod
    def supports(self, target: Target) -> bool:
        """return true if the source can investigate the target"""
        raise NotImplementedError

    @abstractmethod
    def search(self, target: Target) -> list[Findings]:
        """investigate target and return findings"""
        raise NotImplementedError