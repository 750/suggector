from abc import ABC
from abc import abstractmethod
from suggector.suggest import Suggest
from suggector.suggest.browser import Browser

import dataclasses

@dataclasses.dataclass
class SuggestEndpoint:
    suggest_converter: str
    suggest_url_template: str
    search_url_template: str
    suggest_headers: dict[str, str] = None


class BaseConverter(ABC):
    @classmethod
    def get_browsers(cls) -> tuple[Browser]:
        raise NotImplementedError()

    @classmethod
    def get_default_suggest_endpoint(cls) -> SuggestEndpoint:
        raise NotImplementedError()

    @classmethod
    def get_converter_name(cls):
        """
        Converter name to use in config
        """
        return cls.__name__

    @abstractmethod
    def load(self, raw_suggest: str) -> Suggest:
        """
        Class method to parse suggest
        """
        raise NotImplementedError()

    @abstractmethod
    def dump(self, suggest: Suggest):
        """
        Class method"""
        raise NotImplementedError()
