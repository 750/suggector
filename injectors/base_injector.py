from abc import ABC
from abc import abstractmethod
from suggest.models import Suggest


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