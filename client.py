import json
import urllib
import urllib.request

class Client:
    calendar = {
        1: list(range(1, 32)),
        2: list(range(1, 29)),
        3: list(range(1, 32)),
        4: list(range(1, 30)),
        5: list(range(1, 32)),
        6: list(range(1, 31)),
        7: list(range(1, 32)),
        8: list(range(1, 32)),
        9: list(range(1, 31)),
        10: list(range(1, 32)),
        11: list(range(1, 31)),
        12: list(range(1, 32)),
    }

    def __init__(self):
        self.base_url       = 'https://covid19.mathdro.id/api'
        self.today_path     = '/daily'
        self.by_date_path   = '/daily/{m}-{d}-{y}'
        self.countries_path = '/countries'
        self.country_detail = '/countries/{country}/confirmed'

    def load_api(self, path):
        url = f'{self.base_url}{path}'

        try:
            resource = urllib.request.urlopen(url)
            content =  resource.read().decode(resource.headers.get_content_charset())
            return json.loads(content)
        except Exception:
            raise Exception("No API with parameters you give.")

    def get_countries(self):
        countries_list = self.load_api(self.countries_path)
        return list(countries_list.get('countries'))


    def get_country_detail(self, name):
        api_path = self.country_detail.format(country=name)
        country_detail = self.load_api(api_path)
        return country_detail

    def get_world_stats_by_date(self, day, month, year):
        if not month in self.calendar:
            raise Exception({'error': f"Month with number {month} doesnt exist."} )

        if not day in self.calendar[month]:
            raise Exception({'error': f"Day with number {day} doesnt exist."} )

        api_path = self.by_date_path.format(d=day, m=month, y=year)
        given_date_stats = self.load_api(api_path)
        return given_date_stats

    def get_country_stats_by_date(self, country, day, month, year):
        given_date_stats = list(self.get_world_stats_by_date(day, month, year))
        country_stats = list(filter(
            lambda country_stat: country_stat['countryRegion'] == country,
            given_date_stats
        ))

        if len(country_stats) == 0:
            raise Exception({'error': f"Statistics for {country} not found for given date."} )

        return country_stats


client = Client()