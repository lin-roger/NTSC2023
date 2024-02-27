from abc import ABC, abstractmethod
from typing import overload, List, Union
from ..tool._Para import Para


class SummaryStrategy(ABC):
    @overload
    @abstractmethod
    def summary(input: str) -> str:
        ...

    @overload
    @abstractmethod
    def summary(input: List[Para]) -> List[Para]:
        ...

    @abstractmethod
    def summary(input: Union[str, List[Para]]) -> Union[str, List[Para]]:
        pass



