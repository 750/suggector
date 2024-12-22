from suggector.flask_app import run
from suggector.injectors import TimestampInjector

run(
    name="Yagector 😎",
    suggest_endpoint="YandexYabroConverter",
    injectors=[TimestampInjector()]
)