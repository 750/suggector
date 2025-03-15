from suggector.injectors.base_injector import BaseSearchInjector

class UrlSearchInjector(BaseSearchInjector):
    def get_redirect_url(self, query):
        if query.startswith(("http://", "https://")) and " " not in query:
            return query