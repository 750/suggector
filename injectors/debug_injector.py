from injectors.base_injector import BaseInjector
from suggest.models import Suggest, SuggestItem

class DebugInjector(BaseInjector):
    def __init__(
            self,
            url: str,
            substring_trigger: str = "kekea"
    ):
        self.url = url
        self.substring_trigger = substring_trigger

    def inject(self, suggest: Suggest):
        query = suggest.query.strip()

        if self.substring_trigger in query:

            item = SuggestItem(
                text=self.url,
                suggest_type="ENTITY",
                description="Suggector home page",
                visible_text="Suggector home page",
                image_url="❓"
            )
            suggest.items.insert(0, item)
            return True