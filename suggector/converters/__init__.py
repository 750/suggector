from .base_converter import SuggestEndpoint
from .base_converter import BaseConverter

from .google_chrome_converter import GoogleChromeConverter
from .google_firefox_converter import GoogleFirefoxConverter
from .yandex_yabro_converter import YandexYabroConverter
from .api_converter import ApiConverter

DEFAULT_CONVERTERS = (
    GoogleChromeConverter,
    GoogleFirefoxConverter,
    YandexYabroConverter,
    ApiConverter,
)
