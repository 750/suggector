### suggector

### How it works

User configures their browser to use Suggector as their suggestions provider (autocomplete provider).

When the user types some query into the browser's address bar (this is called omnibox on chrome), suggector does the following:
1. Sends that query to a search engine's autocomplete endpoint and gets the result
2. Decodes the result
3. Runs injectors - functions that do something with that result, e.g. add some other suggestions
4. Encodes the result for browser and returns it

Point #3 is the whole point of Suggector: it lets users modify their regular suggect however they wish. Some practical (as in "I'm using them every day") examples are:
* for a given ID suggest links to some service that uses that id
    * you type number `1172` - a link https://xkcd.com/1172/ is suggested
        * this use case can be very nice if you have a lot of internal services at work
* quickly show information
    * you type unix timestamp `1734879333` - text `Sun Dec 22 2024 17:55:33 GMT+0300` is suggested
    * you type hex color `#123898` - an image of that solid color is shown in omnibox
* you type some text with a url in it - that link is suggested (so that you don't have to select and copypaste it)

Some less practical examples are:
* Get suggestions from multiple search engines and then somehow combine them together. Not sure why but that can be done

### Not stable yet

Project version below 1.0.0 means that APIs are not yet stable

Stuff to figure out before 1.0.0:

* image handling - provide helpers to create images without writing full `data:something...` urls
    * would also mean that we can
    * chrome doesn't support svg images in omnibox, but there could be a way to simplify converting svg to png:
        * https://jsfiddle.net/e5m74Lka/ taken from here https://github.com/niklasvh/html2canvas/issues/3225

* cross-browser compatibility handling
    * firefox enables rich suggest depending on certain fields - we should automagically prefill these fields if the user forgot to do that
    * Firefox doesn't support urls in suggest - they are not even shown. We can return them in a form firefox doesn't recognise as urls and then redirect

* render html and xml with flask's built-in engine instead of directly in code

* injectors need to be able to inject independently of main suggector endpoint handling
    * e.g. some injectors can be run before or in parallel to fetching google's autosuggest

* move from requests to something asynchronious
    * injectors can fetch their own endpoints - http requests should not block each other

* provide simple ways to add suggest items
    * as of `0.1.0` adding an item means manually adding `SuggestItem` with its fields filled - that's bad because the user needs to understand something about those fields

* some way to reimplement native keyword search

* support offline usage
    * not sure if this is needed but local-only injectors should work offline
