import random

from factory import Factory, Faker, LazyAttribute, SubFactory, fuzzy
from pydantic import HttpUrl

from restcountries_cli import constants, models


class CountryNameFactory(Factory):
    """
    Main sub factory for the country name
    """

    common: str = fuzzy.FuzzyText()
    official: str = fuzzy.FuzzyText()
    native_name: dict = LazyAttribute(
        lambda country_name: {
            "en": {
                "common": country_name.common,
                "official": country_name.official,
            }
        }
    )

    class Meta:
        model = models.CountryName


class CurrencyFactory(Factory):
    """
    Main sub factory for the currency
    """

    name: str = fuzzy.FuzzyText()
    symbol: str = "€"

    class Meta:
        model = models.Currency


class IDDFactory(Factory):
    """
    Main sub factory for the IDD
    """

    root: str = fuzzy.FuzzyText()
    suffixes: list[str] = []

    class Meta:
        model = models.IDD


class LanguageFactory(Factory):
    """
    Main sub factory for the language
    """

    code: str = fuzzy.FuzzyText(length=3)
    name: str = fuzzy.FuzzyText()

    class Meta:
        model = models.Language


class TranslationFactory(Factory):
    """
    Main sub factory for the translation
    """

    official: str = fuzzy.FuzzyText()
    common: str = fuzzy.FuzzyText()

    class Meta:
        model = models.Translation


class DemonymFactory(Factory):
    """
    Main sub factory for the demonym
    """

    f: str = fuzzy.FuzzyText()
    m: str = fuzzy.FuzzyText()

    class Meta:
        model = models.Demonym


class MapsFactory(Factory):
    """
    Main sub factory for the map's info
    """

    google_maps: HttpUrl = Faker("url")
    open_street_maps: HttpUrl = Faker("url")

    class Meta:
        model = models.Maps


class CarFactory(Factory):
    """
    Main sub factory for the car
    """

    signs: list[str] = LazyAttribute(lambda _: [fuzzy.FuzzyText().fuzz() for _ in range(0, random.randint(0, 3))])
    side: str = fuzzy.FuzzyText()

    class Meta:
        model = models.Car


class FlagFactory(Factory):
    """
    Main sub factory for the flag
    """

    png: HttpUrl = Faker("url")
    svg: HttpUrl = Faker("url")
    alt: str = fuzzy.FuzzyText()

    class Meta:
        model = models.Flag


class CoatOfArmFactory(Factory):
    """
    Main sub factory for the coat of arm
    """

    png: HttpUrl = Faker("url")
    svg: HttpUrl = Faker("url")

    class Meta:
        model = models.CoatOfArm


class CapitalInfoFactory(Factory):
    """
    Main sub factory for the capital
    """

    latlng: list[float] = LazyAttribute(lambda _: [random.randint(-180, 180), random.randint(-180, 180)])

    class Meta:
        model = models.CapitalInfo


class CountryFactory(Factory):
    """
    Main country factory to use in tests
    """

    name: models.CountryName = SubFactory(CountryNameFactory)
    tld: list[str] = LazyAttribute(lambda country: [f".{country.cca2.lower()}"])
    cca2: str = fuzzy.FuzzyText(length=2)
    ccn3: str = LazyAttribute(lambda _: str(random.randint(1, 999)))
    cca3: str = fuzzy.FuzzyText(length=3)
    cioc: str = fuzzy.FuzzyText(length=3)
    independent: bool = Faker("boolean")
    status: str = fuzzy.FuzzyChoice(constants.VALID_COUNTRIES_STATUSES)
    un_member: bool = Faker("boolean")
    currencies: dict[str, models.Currency] = LazyAttribute(
        lambda _: {
            fuzzy.FuzzyText(length=3).fuzz().upper(): CurrencyFactory.build() for _ in range(random.randint(1, 3))
        }
    )
    idd: models.IDD = SubFactory(IDDFactory)
    capital: list[str] = LazyAttribute(lambda _: [fuzzy.FuzzyText().fuzz()])
    alt_spellings: list[str] = LazyAttribute(lambda _: [fuzzy.FuzzyText().fuzz()])
    region: str = fuzzy.FuzzyChoice(constants.VALID_REGIONS)
    subregion: str = fuzzy.FuzzyChoice(constants.VALID_SUBREGIONS)
    languages: list[models.Language] = LazyAttribute(lambda _: [LanguageFactory() for _ in range(random.randint(1, 3))])
    translations: dict[str, models.Translation] = LazyAttribute(
        lambda _: {
            fuzzy.FuzzyText(length=3).fuzz().upper(): TranslationFactory.build() for _ in range(random.randint(1, 3))
        }
    )
    latlng: list[float] = LazyAttribute(lambda _: [random.randint(-180, 180), random.randint(-180, 180)])
    landlocked: bool = Faker("boolean")
    borders: list[str] = LazyAttribute(
        lambda _: [fuzzy.FuzzyText(length=3).fuzz().upper() for _ in range(random.randint(1, 3))]
    )
    area: float = fuzzy.FuzzyFloat(low=0)
    demonyms: dict[str, models.Demonym] = LazyAttribute(
        lambda _: {
            fuzzy.FuzzyText(length=3).fuzz().lower(): DemonymFactory.build() for _ in range(random.randint(1, 3))
        }
    )
    flag: str = fuzzy.FuzzyText(length=1)
    maps: models.Maps = SubFactory(MapsFactory)
    population: int = fuzzy.FuzzyInteger(low=0)
    gini: dict[str, float] = LazyAttribute(
        lambda _: {
            str(fuzzy.FuzzyInteger(low=0).fuzz()): fuzzy.FuzzyFloat(low=0).fuzz() for _ in range(random.randint(1, 3))
        }
    )
    fifa: str = fuzzy.FuzzyText()
    car: models.Car = SubFactory(CarFactory)
    timezones: list[str] = LazyAttribute(
        lambda _: [fuzzy.FuzzyText(length=3).fuzz().upper() for _ in range(random.randint(1, 3))]
    )
    continents: list[str] = LazyAttribute(lambda _: random.choices(constants.VALID_CONTINENTS, k=random.randint(1, 3)))
    flags: models.Flag = SubFactory(FlagFactory)
    coat_of_arms: models.CoatOfArm = SubFactory(CoatOfArmFactory)

    start_of_week: str = fuzzy.FuzzyChoice(choices=constants.VALID_START_OF_THE_WEEK)
    capital_info: models.CapitalInfo = SubFactory(CapitalInfoFactory)
    postal_code: dict[str, str] = LazyAttribute(
        lambda _: {
            "format": fuzzy.FuzzyText().fuzz(),
            "regex": fuzzy.FuzzyText().fuzz(),
        }
    )

    class Meta:
        model = models.Country
