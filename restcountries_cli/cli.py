import os.path
import uuid

import requests_cache

from restcountries_cli.exceptions import APIException, NotValidEndpoint
from restcountries_cli.models import Country


class RestCountriesCli:
    """
    Main client to obtain the values of the countries from restcountries
    """

    def __init__(
        self,
        base_url: str = "https://restcountries.com",
        version: str = "v3.1",
        cached_session: bool = True,
        cache_name: str | None = None,
    ):
        """
        Initialization of the cli. It will start the request session and set the main
        parameters to call the API.
        :param base_url: Url to call where the API is hosted.
        :param version: Version to use in the API call.
        :param cached_session: Bool that shows if the calls are cached or not.
        """
        # Base parameters for the client to work
        self.base_url = base_url
        self.version = version
        self.url = f"{base_url}/{version}"
        self.cached_session = cached_session
        self.cache_name = cache_name if cache_name else uuid.uuid4().hex

        # If the session is cached, it will only call the API once
        if self.cached_session:
            self.session = requests_cache.CachedSession(cache_name=self.cache_name)
        else:
            self.session = requests_cache.OriginalSession()  # type: ignore

        # Store the countries in the cli internally to avoid unnecessary calls
        self.countries: list[Country] = []

        # Endpoints to use
        self.all_endpoint = "all"
        self.name_endpoint = "name"

    @staticmethod
    def parse_country(country: dict) -> Country:
        """
        Country obtained from the API call. It is transformed into a dict from a json.
        :param country: The Country object using the model.
        :return:
        """

        # Correct some corner cases like Finland for open_street_maps
        open_street_maps = country.get("maps", {}).get("openStreetMaps")
        if "openstreetmap.org" in open_street_maps and "http" not in open_street_maps:
            open_street_maps = f"https://www.{open_street_maps}"

        return Country(
            name={
                "common": country.get("name", {}).get("common"),
                "official": country.get("name", {}).get("official"),
                "native_name": country.get("name", {}).get("nativeName", {}),
            },
            tld=country.get("tld"),
            cca2=country.get("cca2"),
            ccn3=country.get("ccn3"),
            cca3=country.get("cca3"),
            cioc=country.get("cioc"),
            independent=country.get("independent"),
            status=country.get("status"),
            un_member=country.get("unMember"),
            currencies=country.get("currencies", {}),
            idd=country.get("idd"),
            capital=country.get("capital"),
            alt_spellings=country.get("altSpellings"),
            region=country.get("region"),
            subregion=country.get("subregion"),
            languages=[{"code": code, "name": name} for code, name in country.get("languages", {}).items()],
            translations=country.get("translations", {}),
            latlng=country.get("latlng"),
            landlocked=country.get("landlocked"),
            borders=country.get("borders"),
            area=country.get("area"),
            demonyms=country.get("demonyms", {}),
            flag=country.get("flag"),
            maps={
                "google_maps": country.get("maps", {}).get("googleMaps"),
                "open_street_maps": open_street_maps,
            },
            population=country.get("population"),
            gini=country.get("gini"),
            fifa=country.get("fifa"),
            car=country.get("car"),
            timezones=country.get("timezones"),
            continents=country.get("continents"),
            flags=country.get("flags"),
            coat_of_arms=country.get("coatOfArms"),
            start_of_week=country.get("startOfWeek"),
            capital_info=country.get("capitalInfo"),
        )

    def __del__(self):
        """
        Make sure that when the cli is destroyed, the cached file is deleted if it exists
        :return:
        """
        self.clean_cache_file()

    def clean_cache_file(self):
        """
        Clean the cache by removing the cache file if it does exist.
        :return:
        """
        if os.path.exists(f"{self.cache_name}.sqlite"):
            os.remove(f"{self.cache_name}.sqlite")

    def refresh_cached_session(self):
        """
        Refresh the cached session if it was cached.

        If this is the case, it is also cleaning the old cache file.
        :return:
        """
        if self.cached_session:
            self.clean_cache_file()
            self.cache_name = uuid.uuid4().hex
            self.session = requests_cache.CachedSession(cache_name=self.cache_name)

    def all(self) -> list[Country]:
        """
        Get all the countries calling the endpoint "all" of the API.
        :return:
        """
        countries = []
        response = self.session.get(f"{self.url}/{self.all_endpoint}")

        match response.status_code:
            case 200:
                # If the response is ok, we parse all the countries
                for country in response.json():
                    country = self.parse_country(country=country)
                    countries.append(country)
            case 404:
                raise NotValidEndpoint(f"url {self.url}/{self.all_endpoint} is not valid")
            case 500:
                raise APIException(f"url {self.url}/{self.all_endpoint} is experienced an internal error")
            case _:
                raise APIException(
                    f"url {self.url}/{self.all_endpoint} is experienced an error with "
                    f"code: '{response.status_code}' and body: '{response.json()}'"
                )
        self.countries = countries
        return self.countries

    def country_name(self, country_name: str, full_name: bool = False, force_query: bool = False) -> Country:
        """
        Get a country based on the name, calling the endpoint "name" of the API.
        It can be just by name or using the full name.

        Using full name will search for exact values, it can be the common or official
        value. This will add the query-parameter "fullText"

        If the country is in the internal cli list, it will not make the call to the API.

        :param force_query:
        :param country_name:
        :param full_name:
        :return:
        """

        # first of all, check if the country is in the country internal cli list
        if (
            cached_country := [country for country in self.countries if (country_name.lower() in country.valid_names)]
        ) and not force_query:
            return cached_country[0]

        # Get the country and append it to the country list
        query = f"{self.url}/{self.name_endpoint}/{country_name}"
        if full_name:
            query += "/fullText=true"
        response = self.session.get(query)
        match response.status_code:
            case 200:
                # If the response is ok, we parse all the countries
                country = self.parse_country(country=response.json()[0])
                self.countries.append(country)
                return country
            case 404:
                raise NotValidEndpoint(f"url {self.url}/{self.name_endpoint} is not valid")
            case 500:
                raise APIException(f"url {self.url}/{self.name_endpoint} is experienced an internal " f"error")
            case _:
                raise APIException(
                    f"url {self.url}/{self.name_endpoint} returned unexpected code " f"'{response.status_code}'"
                )
