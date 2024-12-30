### suggector

Inject your own items into browser suggest!

Until published to pip, install with:
```sh
pip install git+https://github.com/750/suggector
```

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

* think about a more general design
    * initial implementation:
        * there is a single search engine parser-dumper
        * there are any number of injectors each injecting one after another
        * problems arise:
            * how to combine search engines?
            * how to switch engine based on some condition?
            * how to determine sorting order dynamically?
    * proposed implementation:
        * no difference between a search engine and an injector: they are the same thing conceptually
            * naming: SuggestSource
        * new: `combiners` combine results from different sources
        * things to figure out:
            * such design allows for directed acyclic graphs - out of scope for now
            * async is simple: every source is launched asynchroniously, no need to work around search engine converter timings
            * not sure if parsers and formatters should be connected anymore
                * before: there is a single base class for both parsing and dumping
                * after: there are separate base classes for parsing and dumping, old converter inherits from both

* release a package on PyPI

* image handling
    * provide helpers to create images without writing full `data:something...` urls
    * chrome doesn't support svg in omnibox, here is a simple way to generate png with emoji: https://750.github.io/emoji2png

* cross-browser compatibility handling
    * firefox enables rich suggest depending on certain fields - we should automagically prefill these fields if the user forgot to do that
    * Firefox doesn't support urls in suggest - they are not even shown. We can return them in a form firefox doesn't recognise as urls and then redirect

* ~~render html and xml with flask's built-in engine instead of directly in code~~ fixed in https://github.com/750/suggector/issues/1

* injectors need to be able to inject independently of main suggector endpoint handling
    * e.g. some injectors can be run before or in parallel to fetching google's autosuggest

* move from requests to something asynchronious
    * injectors can fetch their own endpoints - http requests should not block each other

* provide simple ways to add suggest items
    * as of `0.1.0` adding an item means manually adding `SuggestItem` with its fields filled - that's bad because the user needs to understand something about those fields

* some way to reimplement native keyword search

* support offline usage
    * not sure if this is needed but local-only injectors should work offline

* make hello page user-friendly
    * chrome: suggector should have been added
    * firefox: right-click address bar -> add "Suggector" ({suggector_name})

* maybe backport to something older than 3.10
    * https://w3techs.com/technologies/history_details/pl-python/3
    * https://gist.github.com/yunruse/326481cd75800c3824f9b63206d350a3

* improve logging

* research llm autocomplete
    * https://news.ycombinator.com/item?id=37541093
    * https://huggingface.co/models?search=next+word
      * https://huggingface.co/allenai/t5-small-next-word-generator-qoogle
      * https://huggingface.co/allenai/t5-small-squad2-next-word-generator-squad

