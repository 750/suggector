from flask import Flask, Response, request, redirect
import json

from .converters.base_converter import BaseConverter
from suggector.injectors.base_injector import BaseInjector
from suggector.Suggector import Suggector
from suggector.converters import SuggestEndpoint
from suggector.suggest import BrowserConverter
from suggector.suggest import Browser
from suggector.suggest import BrowserNotSupportedException
from suggector.suggest.browser import STYLE, list_to_table, pre, code
from suggector.templates import prepare_opensearch_xml, prepare_opensearch_xml_link
import urllib.parse

class SuggectorFlask(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.suggector: Suggector = None

app = SuggectorFlask(__name__, )
app.url_map.converters['browser'] = BrowserConverter


@app.route("/")
def index():
    try:
        unknown_browser = False
        browser = Browser.from_request(request)
    except BrowserNotSupportedException:
        unknown_browser = True
        browser = Browser.CHROMIUM

    xml_link = prepare_opensearch_xml_link(
        app.suggector.name,
        browser
    )

    table = [
        ("Browser", code(browser) + (f" - falling back to {code(browser)} because your browser couldn't be recognised ❌" if unknown_browser else "")),
        ("User agent", pre(request.headers.get("User-agent"))),
    ]

    table.extend([(
        pre(k),
        pre(v if isinstance(v, str) else json.dumps(v, indent=2, ensure_ascii=False))
    ) for k, v in app.suggector.to_dict().items()])

    html_str = f"<style>{STYLE}</style>"+xml_link+"\n"+list_to_table(table)

    return Response(html_str, mimetype='text/html')

@app.route("/icon/<char>.svg")
def char_as_icon(char):
    char = char[0]
    icon = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".90em" font-size="90">{char}</text></svg>'

    return Response(icon, mimetype='image/svg+xml')

@app.route("/<browser:browser>/opensearch.xml")
def opensearch_xml(browser):
    xml = prepare_opensearch_xml(
        name=app.suggector.name,
        host=app.suggector.host,
        port=app.suggector.port,
        browser=browser,
    )
    return Response(xml, mimetype='text/xml')

@app.route("/suggest")
def suggest():
    term = request.args['term']
    browser = request.args['browser']

    result = app.suggector.process(query=term, browser=browser)

    return result

@app.route("/search")
def search():
    term = request.args['term'].strip()

    if term.startswith(("http://", "https://")) and " " not in term:
        return redirect(term)

    url = app.suggector.suggest_endpoint.search_url_template.format(query=urllib.parse.quote_plus(term))

    return redirect(url)


def run(
        name: str = "Suggector",
        converters: list[BaseConverter] = None,
        injectors: list[BaseInjector] = None,
        suggest_endpoint: str|SuggestEndpoint = "GoogleChromeConverter",
        host: str = "127.0.0.1",
        port: int = 9099,
):
    """
    `name`
    What name will be displayed for your suggector in browser. Probably not very important

    `converters`
    Used to supply additional converters for endpoints not supported by suggector.
    Usually not needed at all since most search engines follow very similar specs

    `injectors`
    This is the whole point of Suggector!
    Injectors are callables which somehow modify suggestions.

    `suggest_endpoint`
    Defines what endpoint to ask for suggestions and how to parse them.
    Built-in parser's provide their own default endpoints - simply provide parser's class name to avoid configuration

    `host`, `port`
    Defines Suggector network location.
    Most people would only need to change them if some other software is already using default location
    """
    app.suggector = Suggector(
        name=name,
        host=host,
        port=port,
    )
    app.suggector.setup_endpoint(suggest_endpoint)

    if converters:
        app.suggector.register_converters(converters)

    if injectors:
        app.suggector.register_injectors(injectors)

    app.run(host=host, port=port)
