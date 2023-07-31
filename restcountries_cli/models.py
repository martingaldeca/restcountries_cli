from pydantic import BaseModel, HttpUrl


class CountryBaseName(BaseModel):
    """
    Helper pydantic model that has common fields for the native name and the country name
    """

    common: str
    official: str


class CountryName(CountryBaseName):
    """
    Model for the country name
    """

    native_name: dict[str, CountryBaseName]


class Currency(BaseModel):
    """
    Currency of a country
    """

    name: str
    symbol: str | None = ""  # Countries like Bosnia and Herzegovina has not symbol


class IDD(BaseModel):
    """
    International Direct Dialing of the country
    """

    root: str | None = None
    suffixes: list[str] | None = []


class Language(BaseModel):
    """
    Language of a country
    """

    code: str
    name: str


class Translation(BaseModel):
    """
    Model for a concrete translation of a country
    """

    official: str
    common: str


class Demonym(BaseModel):
    """
    Demonym in a language for the country
    """

    f: str
    m: str


class Maps(BaseModel):
    """
    URLs to the map addresses of the countries
    """

    google_maps: HttpUrl
    open_street_maps: HttpUrl


class Car(BaseModel):
    """
    Todo, WTF is this?
    """

    signs: list[str] | None = []  # Countries like Aruba have not signs
    side: str


class CountryImageBase(BaseModel):
    """
    Helper model for images
    """

    png: HttpUrl | None = None
    svg: HttpUrl | None = None


class Flag(CountryImageBase):
    """
    Flag of the country model
    """

    alt: str | None = None


class CoatOfArm(CountryImageBase):
    """
    Coat of arms information of the country
    """


class CapitalInfo(BaseModel):
    """
    Capital information about the country
    """

    latlng: list[float | None] = [None, None]

    @property
    def latitude(self) -> float | None:
        """
        Property to return only the latitude
        :return:
        """
        return self.latlng[0]

    @property
    def longitude(self) -> float | None:
        """
        Property to return only the longitude
        :return:
        """
        return self.latlng[1]


class Country(CapitalInfo):
    """
    Country model with all the information and validations with pydantic
    """

    name: CountryName
    tld: list[str] | None
    cca2: str
    ccn3: str | None
    cca3: str
    cioc: str | None
    independent: bool | None
    status: str
    un_member: bool
    currencies: dict[str, Currency]
    idd: IDD  # International Direct Dialing
    # A country can have multiple capitals or none as Antarctica
    capital: list[str] | None
    alt_spellings: list[str]
    region: str
    subregion: str | None  # Antarctica, for example, has not subregion
    languages: list[Language]
    translations: dict[str, Translation]
    landlocked: bool
    borders: list[str] | None
    area: float
    demonyms: dict[str, Demonym]
    flag: str
    maps: Maps
    population: int
    gini: dict[str, float] | None
    fifa: str | None
    car: Car
    timezones: list[str]
    continents: list[str]
    flags: Flag
    coat_of_arms: CoatOfArm | None
    start_of_week: str
    capital_info: CapitalInfo
    postal_code: dict[str, str] = {"format": "", "regex": ""}

    @property
    def valid_names(self) -> list:
        """
        Property that returns all the valid names of the countries in lowercase.
        These names are the common and the official name and the native common and official names for all the languages
        present in the native name dict.
        :return:
        """
        return (
            [
                self.name.common.lower(),
                self.name.official.lower(),
            ]
            + [base_name.common.lower() for base_name in self.name.native_name.values()]
            + [base_name.official.lower() for base_name in self.name.native_name.values()]
        )

    def __eq__(self, other: object) -> bool:
        """
        2 Countries will be the same if their cca2 are the same
        :param other:
        :return:
        """
        if not isinstance(other, Country):  # Avoid violate the Liskov substitution principle
            return NotImplemented
        return self.cca2 == other.cca2
