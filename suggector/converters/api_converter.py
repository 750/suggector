
import base64
import dataclasses
import json

from suggector.converters import BaseConverter
from suggector.converters import SuggestEndpoint
from suggector.suggest import Suggest
from suggector.suggest import SuggestItem
from suggector.suggest.browser import Browser


class ApiConverter(BaseConverter):
    @classmethod
    def get_default_suggest_endpoint(cls):
        raise KeyError()

    @classmethod
    def get_browsers(cls) -> tuple[Browser]:
        return (
            Browser.API,
        )

    def load(self, raw_suggest):
        return super().load(raw_suggest)

    def dump(self, suggest: Suggest):
        return [dataclasses.asdict(i) for i in suggest.items]
