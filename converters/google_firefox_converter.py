import json
from converters import SuggestEndpoint
from suggest import Suggest
from converters import BaseConverter
from suggest import SuggestItem
from suggest.browser import Browser


class GoogleFirefoxConverter(BaseConverter):
    # https://searchfox.org/mozilla-central/source/browser/components/urlbar/UrlbarProviderSearchSuggestions.sys.mjs#51
    FIREFOX_FILTER_SUGGESTS_WITH_SYMBOLS = "/@:[."
    
    def get_default_suggest_endpoint(cls):
        return SuggestEndpoint(
            suggest_converter=cls.get_converter_name(),
            suggest_url_template="https://www.google.com/complete/search?client=firefox&channel=fen&q={query}",
            search_url_template="https://www.google.com/search?q={query}",
        )
        
    @classmethod
    def get_browsers(cls) -> list[Browser]:
        return (
            Browser.FIREFOX,
        )
    
    def load(self, raw_suggest) -> Suggest:
        raw_suggest = json.loads(raw_suggest)
        query = raw_suggest[0]
        texts = raw_suggest[1]
        descriptions = raw_suggest[2]
        
        items = [SuggestItem(i) for i in texts]
        
        for idx, i in enumerate(descriptions):
            items[idx].description = i
        
        suggest_meta = raw_suggest[3]
    
        if "google:suggestdetail" in suggest_meta:
            for idx, i in enumerate(suggest_meta["google:suggestdetail"]):
                description = i.get("a")
                color = i.get("dc")
                image_url = i.get("i")
                # params = i.get("q")
                visible_text = i.get("t")
                
                items[idx].description = description
                items[idx].image_background_color = color
                items[idx].image_url = image_url
                items[idx].visible_text = visible_text

        return Suggest(
            query=query,
            items=items,
        )
    
    @staticmethod
    def suggest_item_is_rich(item: SuggestItem):
        return any([
            item.description,
            item.image_url,
        ])
        
    def fix_firefox_links(self, suggest: Suggest):
        for i in suggest.items:
            if " " not in i.text and any([s in i.text for s in self.FIREFOX_FILTER_SUGGESTS_WITH_SYMBOLS]):
                i.text = f"{i.text} "
                # i.image_url = "🔗"
            else:
                i.text = i.text
            
    
    def dump(self, suggest: Suggest):
        self.fix_firefox_links(suggest)

        rich_data = []

        to_dump = [
            suggest.query,
            [i.text for i in suggest.items],
            [i.description or "" for i in suggest.items],
            {
                "google:suggestdetail": rich_data,
            }
        ]

        for i in suggest.items:
            if self.suggest_item_is_rich(i):
                rich_data.append({
                    "a": i.description,
                    "dc": i.image_background_color,
                    "i": i.image_url,
                    "q": "gs_ssp=1",
                    "t": i.visible_text,
                })
            else:
                rich_data.append({})

        return to_dump
