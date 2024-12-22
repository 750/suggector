from flask_app import run
from injectors.timestamp_injector import TimestampInjector

run(
    name="Yagector 😎",
    suggest_endpoint="YandexYabroConverter",
    injectors=[TimestampInjector()]
)