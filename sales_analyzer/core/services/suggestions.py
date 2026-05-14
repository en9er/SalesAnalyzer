from abc import ABC, abstractmethod
from typing import List

class ISuggestionsService(ABC):
    @abstractmethod
    def get_suggestions(*args, **kwargs) -> List[str]:
        raise NotImplementedError
