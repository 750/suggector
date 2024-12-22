from flask import Request
from enum import StrEnum
import html

from werkzeug.routing import BaseConverter as RoutingBaseConverter

class BrowserNotSupportedException(Exception):
    pass

class Browser(StrEnum):

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


TABLE_START = "<table>\n  <tbody>"
TABLE_FINISH = "  <tbody>\n<table>"

def list_to_table(l):
    parts = [
        TABLE_START
    ]
    for row in l:
        parts.append("    <tr>")
        for cell in row:
            parts.append(f"      <td>{str(cell)}</td>")
        parts.append("    </tr>")

    parts.append(TABLE_FINISH)

    return "\n".join(parts)

def pre(s):
    return f"<pre>{html.escape(str(s))}</pre>"

def code(s):
    return f"<code>{html.escape(str(s))}</code>"


STYLE = """table {
  border-collapse: collapse;
  border: 2px solid rgb(200,200,200);
}

td, th {
  border: 1px solid rgb(190,190,190);
  padding: 10px 20px;
}

th {
  background-color: rgb(235,235,235);
}

td {
}

tr:nth-child(even) td {
  background-color: rgb(250,250,250);
}

tr:nth-child(odd) td {
  background-color: rgb(245,245,245);
}

caption {
  padding: 10px;
}
"""
