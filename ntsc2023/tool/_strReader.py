from typing import List, Union

from ._Para import Para
from ._reader import Reder
from ..segment import _segStrategy

import re


class StrReader(Reder):
    def __init__(self, input: Union[str, List[str]], windosSize=3) -> None:
        """
        input: str, the path of the input file or list of transcript
        """
        super().__init__()
        self._indexList: List[int] = []
        self._startTimeList: List[str] = []
        self._endTimeList: List[str] = []
        self._contextList: List[str] = []
        self._windosSize: int = windosSize

        tmp = None
        if isinstance(input, list):
            tmp = input
        else:
            with open(input, "r", encoding="UTF-8") as f:
                tmp = f.readlines()

        count = 0
        for i in tmp:
            i = re.sub(re.compile(r"\[(.*?)\]"), "", i.strip())
            if len(i) != 0:
                if count == 0:
                    self._indexList.append(int(i))
                elif count == 1:
                    startTime, endTime = i.split("-->")
                    self._startTimeList.append(startTime.strip())
                    self._endTimeList.append(endTime.strip())
                elif count == 2:
                    self._contextList.append(i)
                else:
                    self._contextList[-1] += i
                count += 1
            else:
                count = 0

        self._newParaTagList: List[float] = [0.0] * (len(self._indexList) - 1)

    def __len__(self):
        return len(self._indexList)

    def __getitem__(self, i) -> dict:
        return {
            "index": self._indexList[i],
            "stratTime": self._startTimeList[i],
            "endTime": self._endTimeList[i],
            "context": self._contextList[i],
        }

    def __iter__(self):
        i = 1
        while i < len(self._indexList):
            yield [
                " ".join(self._contextList[i - self._windosSize : i]),
                " ".join(self._contextList[i : i + self._windosSize]),
            ]
            i += 1

    def segmentBy(self, alg: _segStrategy.SegStrategy):
        super().segmentBy(alg)
        for i, [s1, s2] in enumerate(self):
            self._newParaTagList[i] = alg.segment(s1, s2)

    def _getParaSegIdxList(self, var) -> List[int]:
        idxList = []
        for i, tag in enumerate(self._newParaTagList):
            # if tag:
            if not tag > var:
                idxList.append(i + 1)
        return idxList

    def getPara(self, var) -> List[Para]:
        super().getPara(var)
        idxList = self._getParaSegIdxList(var)
        paraList = []
        for i in range(len(idxList)):
            if i == 0:
                tmp = self[: idxList[i]]
            elif i == len(idxList) - 1:
                tmp = self[idxList[i] :]
            else:
                tmp = self[idxList[i] : idxList[i + 1]]

            paraList.append(
                Para(
                    index=tmp["index"][0],
                    stratTime=tmp["stratTime"][0],
                    endTime=tmp["endTime"][-1],
                    context=" ".join(tmp["context"]),
                )
            )
        return paraList
