import json
from converters import SuggestEndpoint
from suggest import Suggest
from converters import BaseConverter
from suggest import SuggestItem
from suggest.browser import Browser


class YandexYabroConverter(BaseConverter):
    def get_default_suggest_endpoint(cls):
        return SuggestEndpoint(
            suggest_converter=cls.get_converter_name(),
            suggest_url_template="https://yandex.ru/suggest/suggest-browser?part={query}&brandID=yandex&rich=1&srv=browser_desktop&rich_nav=1",
            search_url_template="https://yandex.ru/search/?text={query}",
        )
        
    @classmethod
    def get_browsers(cls) -> list[Browser]:
        return ()

    def load(self, raw_suggest) -> Suggest:
        raw_suggest = json.loads(raw_suggest)
        query = raw_suggest[0]
        texts = raw_suggest[1]
        descriptions = raw_suggest[2]
        
        items = [SuggestItem(i, relevance=1000-idx) for idx,i in enumerate(texts)]
        
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
    
    def dump(self, suggest):
        raise NotImplementedError("No reason to implement: regular Chrome dump is supported")
