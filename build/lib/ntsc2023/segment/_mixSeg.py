from . import _nspSeg, _segStrategy, _simSeg
from typing import Union


class MixSeg(_segStrategy.SegStrategy):
    def __init__(self):
        super().__init__()
        self.nspSeg = _nspSeg.NSPSeg()
        self.simSeg = _simSeg.SimSeg()

    def segment(self, s1, s2, var=None) -> Union[float, bool]:
        super().segment(s1, s2, var)
        value = self.nspSeg.segment(s1, s2) + self.simSeg.segment(s1, s2)
        if var is not None:
            return value > var * 2
        else:
            return value
