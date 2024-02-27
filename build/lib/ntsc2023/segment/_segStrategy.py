from abc import ABC, abstractmethod
from typing import overload, Union


class SegStrategy(ABC):
    @overload
    @abstractmethod
    def segment(self, s1, s2, var) -> bool:
        """
        s1: 左側字串
        s2: 右側字串
        var: 可選，分割閥值

        return: bool, not need segment
        """
        ...

    @overload
    @abstractmethod
    def segment(self, s1, s2) -> float:
        """
        s1: 左側字串
        s2: 右側字串

        return: float, high is not need segment
        """
        ...

    @abstractmethod
    def segment(self, s1, s2, var=None) -> Union[float, bool]:
        pass
