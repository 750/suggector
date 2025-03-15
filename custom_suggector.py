from suggector.flask_app import run
from suggector.injectors import TimestampInjector
from suggector.injectors import UrlSearchInjector

run(
    name="😎 Yagector",
    suggest_endpoint="YandexYabroConverter",
    injectors=[TimestampInjector()],
    search_injectors=[UrlSearchInjector()],
)