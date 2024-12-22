import dataclasses
import json
import requests

from suggector.converters import BaseConverter
from suggector.converters import DEFAULT_CONVERTERS
from suggector.injectors import DebugInjector
from suggector.converters import SuggestEndpoint
from suggector.converters.google_chrome_converter import GoogleChromeConverter
from suggector.injectors.base_injector import BaseInjector
from suggector.suggest.browser import Browser
from suggector.suggest.models import Suggest
import urllib.parse


class Suggector:
    def __init__(
            self,
            name: str,
            host: str,
            port: int,
    ):
        self.name = name
        self.host = host
        self.port = port

        self._converter_by_name: dict[str, BaseConverter] = {}
        self._dump_converter_by_browser: dict[Browser, BaseConverter] = {}

        self.suggest_endpoint: SuggestEndpoint = None
        self._injectors: list[BaseInjector] = []

        self.register_converters([i() for i in DEFAULT_CONVERTERS])
        self.register_injectors([DebugInjector(f"http://{self.host}:{self.port}")])

    def to_dict(self):
        return {
            "name": self.name,
            "host": self.host,
            "port": self.port,
            "suggest_endpoint": dataclasses.asdict(self.suggest_endpoint) if self.suggest_endpoint is not None else None,
            "_converter_by_name": list(self._converter_by_name.keys()),
            "_injectors": [i.get_injector_name() for i in self._injectors],
        }

    def register_converters(self, converters: list[BaseConverter]):
        for converter in converters:
            name = converter.get_converter_name()
            assert name not in self._converter_by_name, "same name converters found"
            self._converter_by_name[name] = converter

            for browser in converter.get_browsers():
                self._dump_converter_by_browser[browser] = converter

    def register_injectors(self, injectors: list[BaseInjector]):
        self._injectors.extend(injectors)

    def setup_endpoint(self, suggest_endpoint):
        if isinstance(suggest_endpoint, str):
            self.suggest_endpoint = self._converter_by_name[suggest_endpoint].get_default_suggest_endpoint()
        else:
            assert isinstance(suggest_endpoint, SuggestEndpoint)
            self.suggest_endpoint = suggest_endpoint

    def get_raw_suggest(self, query) -> str:
        suggest_url = self.suggest_endpoint.suggest_url_template.format(query=query)
        suggest_headers = self.suggest_endpoint.suggest_headers
        raw_response = requests.get(
            suggest_url,
            headers=suggest_headers,
            # verify='/Users/jarvis-hmac/Downloads/charles-proxy-ssl-proxying-certificate.pem'
        ).text

        return raw_response

    def _render_image_urls(self, suggest: Suggest):
        for item in suggest.items:
            image = item.image_url
            if image and len(image) == 1:
                print(f"FIX {image}")
                item.image_url = f"http://{self.host}:{self.port}/icon/{urllib.parse.quote(image)}.svg"
                # item.image_url = "https://www.svgrepo.com/show/528888/cat.svg"

    def process(self, query: str, browser: Browser):
        raw_suggest = self.get_raw_suggest(query)

        converter = self._converter_by_name[self.suggest_endpoint.suggest_converter]

        suggest = converter.load(raw_suggest)

        for injector in self._injectors:
            did_inject = injector.inject(suggest)

            print(f"{injector.get_injector_name()}: {did_inject}")

        self._render_image_urls(suggest)

        dump_converter = self._dump_converter_by_browser[browser]

        result = dump_converter.dump(suggest)

        # print(json.dumps(result))
        print(json.dumps(GoogleChromeConverter.decode_recursive(result)))

        return result
