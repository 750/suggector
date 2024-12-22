import dataclasses



@dataclasses.dataclass
class SuggestItem:
    # generic fields without any browser or search engine specifics
    text: str
    relevance: int = 1000
    suggest_type: str = "QUERY"
    visible_text: str = None
    description: str = None
    
    # NOTE: chrome doesn't support svg
    image_url: str = None
    
    image_background_color: str = None

    def set_image_with_char(self, char):
        self.image_url = self.char_to_icon(char)

    @staticmethod
    def char_to_icon(char: str):
        return f"data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.90em%22 font-size=%2290%22>{char}</text></svg>"

    @staticmethod
    def url_is_data_url(url: str) -> bool:
        return url.startswith("data:")

@dataclasses.dataclass
class Suggest:
    query: str
    items: list[SuggestItem]
