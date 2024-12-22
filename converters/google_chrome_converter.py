import base64
import dataclasses
import json

import blackboxprotobuf
from converters import BaseConverter
from converters import SuggestEndpoint
from suggest import Suggest
from suggest import SuggestItem
from suggest.browser import Browser

@dataclasses.dataclass
class EntityInfo:
    PROTOBUF_SCHEMA = {
        # https://source.chromium.org/chromium/chromium/src/+/main:third_party/omnibox_proto/entity_info.proto;l=38;drc=8ff4f09f8bbc04e69f0f20144a2005eb4c1eed53?q=gs_ssp&ss=chromium%2Fchromium%2Fsrc
        "1": {
            "name": "entity_id",
            "type": "string",
        },
        "2": {
            "name": "description",
            "type": "string",
        },
        "6": {
            "name": "image",
            "type": "string",
        },
        "7": {
            "name": "text",
            "type": "string",
        },
        "9": {
            "name": "color",
            "type": "string",
        },
        "10": {
            "name": "params",
            "type": "string",
        },
        "14": {
            "name": "category",
            "type": "int",
        },
        "17": {
            "name": "site_url",
            "type": "string",
        },
    }
    
    entity_id: str|None = None
    description: str|None = None
    image: str|None = None
    text: str|None = None
    category: int|None = None
    color: str = None
    action: int = None
    params: str = None
    site_url: str = None
    
    def is_empty(self):
        return all([
            not self.description,
            not self.image,
            not self.text,
            not self.color,
            not self.action,
            not self.site_url,
        ])
    
    @staticmethod
    def from_pb_b64(entity_info_pb_b64) -> 'EntityInfo':
        entity_info_pb = base64.b64decode(entity_info_pb_b64)
        entity_info_str, _ = blackboxprotobuf.protobuf_to_json(entity_info_pb, EntityInfo.PROTOBUF_SCHEMA)
        entity_info = json.loads(entity_info_str)
        
        entity_id = entity_info.get("entity_id")  # probably google's internal id for entity
        description = entity_info.get("description")  # this is rendered on chrome
        image = entity_info.get("image")  # supports data:image/... urls
        text = entity_info.get("text")  # actual suggestion text to be searched - only visible when item is selected
        category = entity_info.get("category")
        color = entity_info.get("color")  # chrome uses this instead of image if it can't be loaded
        params = entity_info.get("params")  # somehow lack of this parameter can make entity autofill search field - not desired
        site_url = entity_info.get("site_url")  # not used, probably google's internal stuff
        
        return EntityInfo(
            color=color,
            params=params,
            site_url=site_url,
            entity_id=entity_id,
            description=description,
            image=image,
            text=text,
            category=category,
        )
        
    def to_pb_64(self) -> str:
        d = {k: v for k, v in dataclasses.asdict(self).items() if v}
        return base64.b64encode(blackboxprotobuf.encode_message(d, self.PROTOBUF_SCHEMA)).decode()


class GoogleChromeConverter(BaseConverter):
    @classmethod
    def get_default_suggest_endpoint(cls):
        return SuggestEndpoint(
            suggest_converter=cls.get_converter_name(),
            suggest_url_template="https://www.google.com/complete/search?client=chrome-omni&gs_ri=chrome-ext-ansg&q={query}",
            search_url_template="https://www.google.com/search?q={query}",
            suggest_headers={
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0"
            },
        )

    @classmethod
    def get_browsers(cls) -> tuple[Browser]:
        return (
            Browser.CHROMIUM,
            Browser.YABRO,
        )
    
    @staticmethod
    def decode_recursive(d):
        if isinstance(d, list):
            return [GoogleChromeConverter.decode_recursive(i) for i in d]
        elif isinstance(d, dict):
            return {k: (dataclasses.asdict(EntityInfo.from_pb_b64(v)) if k == "google:entityinfo" else GoogleChromeConverter.decode_recursive(v)) for k, v in d.items()}
        else:
            return d
    
    def load(self, raw_suggest: str):
        raw_suggest = json.loads(raw_suggest)
        query = raw_suggest[0]
        texts = raw_suggest[1]
        descriptions = raw_suggest[2]
        
        items = [SuggestItem(i) for i in texts]
        
        for idx, i in enumerate(descriptions):
            items[idx].description = i
        
        suggest_meta = raw_suggest[4]
    
        if "google:suggestdetail" in suggest_meta:
            for idx, i in enumerate(suggest_meta["google:suggestdetail"]):
                if "google:entityinfo" in i:
                    entity_info = EntityInfo.from_pb_b64(i["google:entityinfo"])
                    
                    items[idx].visible_text = entity_info.text
                    items[idx].description = entity_info.description
                    items[idx].image_url = entity_info.image
                    items[idx].image_background_color = entity_info.color

        if "google:suggesttype" in suggest_meta:
            for idx, i in enumerate(suggest_meta["google:suggesttype"]):
                items[idx].suggest_type = i

        if "google:suggestrelevance" in suggest_meta:
            for idx, i in enumerate(suggest_meta["google:suggestrelevance"]):
                items[idx].relevance = i

        return Suggest(
            query=query,
            items=items,
        )
    
    def dump(self, suggest: Suggest):
        entity_infos = []
        
        to_dump = [
            suggest.query,
            [i.text for i in suggest.items],
            [i.description or "" for i in suggest.items],
            [],
            {
                "google:suggestrelevance": [i.relevance for i in suggest.items],
                # "google:suggestsubtypes": [i.suggestsubtypes for i in suggest.items],
                "google:suggesttype": [i.suggest_type for i in suggest.items],
                "google:suggestdetail": entity_infos,
                "google:verbatimrelevance": 1187,
            }
        ]

        for i in suggest.items:
            entity_info = EntityInfo(
                entity_id="1",
                description=i.description,
                image=i.image_url,
                text=i.visible_text,
                color=i.image_background_color or "#000000",
                params="gs_ssp=1",
            )
            
            # print(dataclasses.asdict(entity_info))
            # print(entity_info.is_empty())
            
            if entity_info.is_empty():
                entity_infos.append({})
            else:
                entity_infos.append({"google:entityinfo": entity_info.to_pb_64()})
        
        return to_dump
