from abc import ABC, abstractmethod
from typing import List, TextIO

from .typings.invoice_types import Invoice


class BaseLedesParser(ABC):
    @abstractmethod
    def parse(self, reader: TextIO) -> List[Invoice]:
        pass
