from flask import Request
from enum import StrEnum
import html

from werkzeug.routing import BaseConverter as RoutingBaseConverter

class BrowserNotSupportedException(Exception):
    pass

class Browser:

    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    YABRO = "yabro"

    @staticmethod
    def from_request(request: Request) -> 'Browser':
        user_agent = request.headers.get("User-agent")

        if "YaBrowser" in user_agent:
            return Browser.YABRO
        if "Firefox" in user_agent:
            return Browser.FIREFOX
        if "Chrome" in user_agent:
            return Browser.CHROMIUM

        raise BrowserNotSupportedException(f"Unknown browser with user agent: {user_agent}")


class BrowserConverter(RoutingBaseConverter):
    def to_python(self, value):
        return Browser(value)
