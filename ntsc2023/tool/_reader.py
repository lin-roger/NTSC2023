from abc import ABC, abstractmethod
from typing import List
from ._Para import Para
from ..segment import _segStrategy


class Reder(ABC):
    @abstractmethod
    def segmentBy(self, alg: _segStrategy.SegStrategy):
        """
        segment the context by the given algorithm
        """
        pass

    @abstractmethod
    def getPara(self, var: float) -> List[Para]:
        """
        get the paragraph segmentation
        """
        pass
