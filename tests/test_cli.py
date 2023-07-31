import json
import os
from unittest import TestCase, mock

import requests_cache
import responses

from restcountries_cli.cli import RestCountriesCli
from restcountries_cli.exceptions import APIException, NotValidEndpoint
from restcountries_cli.factories import CountryFactory
from restcountries_cli.models import Country


class RestCountriesCliTestCase(TestCase):
    def setUp(self) -> None:
        self.cli = RestCountriesCli()

    def test_cached_session(self):
        test_data_list = [
            [True, requests_cache.CachedSession],
            [False, requests_cache.OriginalSession],
        ]
        for test_data in test_data_list:
            with self.subTest(test_data=test_data):
                cached_session, expected_session = test_data
                cli = RestCountriesCli(cached_session=cached_session)
                self.assertIsInstance(cli.session, expected_session)

    def test_parse_country(self):
        with open("tests/example_country.json") as example_country_json_file:
            example_country_json = json.load(example_country_json_file)[0]
            self.assertIsInstance(self.cli.parse_country(example_country_json), Country)

    def test_clean_cache_file_called_on_destroy(self):
        complete_cache_name = f"{self.cli.cache_name}.sqlite"
        with mock.patch.object(RestCountriesCli, "clean_cache_file") as mock_clean_cache_file:
            del self.cli

        self.assertEqual(mock_clean_cache_file.call_count, 1)
        os.remove(complete_cache_name)  # We must clean the file manually

    def test_clean_cache_file(self):
        complete_cache_name = f"{self.cli.cache_name}.sqlite"
        self.assertTrue(os.path.exists(complete_cache_name))
        self.cli.clean_cache_file()
        self.assertFalse(os.path.exists(complete_cache_name))

    def test_refresh_cached_session(self):
        test_data_list = [
            [False, True],
            [True, False],
        ]
        for test_data in test_data_list:
            with self.subTest(test_data=test_data):
                cached_session, expected_same_session_value = test_data
                cli = RestCountriesCli(cached_session=cached_session)
                original_session = cli.session
                cli.refresh_cached_session()
                self.assertEqual(cli.session is original_session, expected_same_session_value)

    def test_all_failed(self):
        test_data_list = [
            [404, NotValidEndpoint, f"url {self.cli.url}/{self.cli.all_endpoint} is not valid"],
            [500, APIException, f"url {self.cli.url}/{self.cli.all_endpoint} is experienced an internal " f"error"],
            [
                418,
                APIException,
                f"url {self.cli.url}/{self.cli.all_endpoint} is experienced an error "
                f"with code: '418' and body: '{{}}'",
            ],
        ]
        for test_data in test_data_list:
            with self.subTest(test_data=test_data):
                status, expected_exception_to_use, expected_message = test_data
                with responses.RequestsMock() as mock_responses, self.assertRaises(
                    expected_exception_to_use
                ) as expected_exception:
                    mock_responses.add(
                        method=responses.GET,
                        url=f"{self.cli.url}/{self.cli.all_endpoint}",
                        body="{}",
                        status=status,
                        content_type="application/json",
                    )
                    self.cli.all()
                self.assertEqual(str(expected_exception.exception), expected_message)

    def test_all_ok(self):
        with open("tests/example_all.json") as example_all_file, responses.RequestsMock() as mock_responses:
            example_all = json.load(example_all_file)
            mock_responses.add(
                method=responses.GET,
                url=f"{self.cli.url}/{self.cli.all_endpoint}",
                body=json.dumps(example_all),
                status=200,
                content_type="application/json",
            )
            self.cli.all()
            self.assertEqual(len(self.cli.countries), 250)

    def test_country_name_cached_and_force_parameters(self):
        cached_country: Country = CountryFactory()
        self.cli.countries.append(cached_country)
        test_data_list = [
            [False, 0],
            [True, 1],
        ]
        for test_data in test_data_list:
            with self.subTest(test_data=test_data), mock.patch.object(
                self.cli.session, "get"
            ) as mock_get, mock.patch.object(self.cli, "parse_country") as mock_parse_country:
                force_query, mock_get_call_count = test_data
                mocked_response = mock.MagicMock()
                mocked_response.status_code = 200
                mock_get.return_value = mocked_response
                mock_parse_country.return_value = cached_country
                country = self.cli.country_name(country_name=cached_country.name.common, force_query=force_query)
                self.assertEqual(mock_get.call_count, mock_get_call_count)
                self.assertEqual(country, cached_country)

    def test_country_name_failed(self):
        test_data_list = [
            [404, NotValidEndpoint, f"url {self.cli.url}/{self.cli.name_endpoint} is not valid"],
            [500, APIException, f"url {self.cli.url}/{self.cli.name_endpoint} is experienced an internal " f"error"],
            [418, APIException, f"url {self.cli.url}/{self.cli.name_endpoint} returned unexpected code " f"'418'"],
        ]
        for test_data in test_data_list:
            with self.subTest(test_data=test_data):
                status, expected_exception_to_use, expected_message = test_data
                with responses.RequestsMock() as mock_responses, self.assertRaises(
                    expected_exception_to_use
                ) as expected_exception:
                    mock_responses.add(
                        method=responses.GET,
                        url=f"{self.cli.url}/{self.cli.name_endpoint}/Test",
                        body="{}",
                        status=status,
                        content_type="application/json",
                    )
                    self.cli.country_name(country_name="Test")
                self.assertEqual(str(expected_exception.exception), expected_message)

    def test_country_name_ok(self):
        with open(
            "tests/example_country.json"
        ) as example_country_name_file, responses.RequestsMock() as mock_responses:
            example_country_name = json.load(example_country_name_file)
            mock_responses.add(
                method=responses.GET,
                url=f"{self.cli.url}/{self.cli.name_endpoint}/Spain",
                body=json.dumps(example_country_name),
                status=200,
                content_type="application/json",
            )
            country = self.cli.country_name(country_name="Spain")
            self.assertEqual(country.name.common, "Spain")
