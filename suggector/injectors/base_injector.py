from abc import ABC
from abc import abstractmethod
from suggector.suggest.models import Suggest


class BaseInjector(ABC):
    @classmethod
    def get_injector_name(cls):
        """
        Injector name to use in config
        """
        return cls.__name__

    @abstractmethod
    def inject(self, suggest: Suggest) -> bool:
        """
        This method should modify suggest.items
        Return True if injector actually injected something
        """

        raise NotImplementedError()

class BaseSearchInjector(ABC):
    @abstractmethod
    def get_redirect_url(self, query: str) -> str:
        raise NotImplementedError()
