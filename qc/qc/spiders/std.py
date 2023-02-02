import scrapy
import json


usdot_range = range(1, 10)


def clean_null_terms(d):
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = clean_null_terms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None:
            clean[k] = v
    return clean


class QCSpider(scrapy.Spider):
    name = "std"

    def start_requests(self):
        for usdot in usdot_range:
            url = f'https://mobile.fmcsa.dot.gov/qc/services/carriers/{usdot}?webKey=365277e5b51ede9f3e9da6530d43a0a033609ab1'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        result = json.loads(response.body)

        try:
            carrier = clean_null_terms(result['content']['carrier'])
            yield carrier
        except TypeError:
            print("RNF")
