from suggector.injectors.base_injector import BaseInjector
from suggector.suggest.models import Suggest, SuggestItem
import datetime

class TimestampInjector(BaseInjector):
    def inject(self, suggest: Suggest):
        query = suggest.query.strip()

        dt = None
        if query.isdigit():
            ts_int = int(query)

            if 1_000_000_000 <= ts_int <= 2_000_000_000:
                dt = datetime.datetime.fromtimestamp(ts_int)
            elif 1_000_000_000_000 <= ts_int <= 2_000_000_000_000:
                dt = datetime.datetime.fromtimestamp(ts_int/1000)

        if dt is not None:
            dt_str = str(dt)

            item = SuggestItem(
                text=query,
                suggest_type="ENTITY",
                description=dt_str,
                visible_text=dt_str,
                image_background_color="#ffffff",
                image_url='⏰',
            )
            suggest.items.insert(0, item)
            return True