import html
from suggector.suggest import Browser

def prepare_opensearch_xml(
        name: str,
        host: str,
        port: int,
        browser: Browser,
        ):
    return f"""<?xml version="1.0"?>
    <OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/" xmlns:moz="http://www.mozilla.org/2006/browser/search/">
        <ShortName>{html.escape(name)}</ShortName>
        <Description>{html.escape(name)}</Description>
    <Url type="text/html" method="get"
         template="http://{host}:{port}/search?term={{searchTerms}}" />
    <Url type="application/x-suggestions+json" method="get"
         template="http://{host}:{port}/suggest?term={{searchTerms}}&amp;browser={browser}" />
    </OpenSearchDescription>
    """

def prepare_opensearch_xml_link(
        search_engine_name: str,
        browser: Browser,
        ):

    return f"""<link
                rel="search"
                href="/{browser}/opensearch.xml"
                title="{html.escape(search_engine_name)}"
                type="application/opensearchdescription+xml"
               >
    """