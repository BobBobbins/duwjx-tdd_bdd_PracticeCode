"""
Test Cases for Mocking Lab
"""
import json
from unittest import TestCase
from unittest.mock import patch, Mock
from requests import Response
from models import IMDb

IMDB_DATA = {}


class TestIMDbDatabase(TestCase):
    """Tests Cases for IMDb Database"""

    @classmethod
    def setUpClass(cls):
        """Load imdb responses needed by tests"""
        global IMDB_DATA
        with open("tests/fixtures/imdb_responses.json") as json_data:
            IMDB_DATA = json.load(json_data)

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    # You always want to patch the function that is within the namespace that you are
    # testing. This is why you need to fully qualify IMDb.search_titles as
    # test_imdb.IMDb.search_titles
    # Patch where the object is used
    # https://www.youtube.com/watch?v=ww1UsGZV8fQ&t=1062s
    @patch("tests.test_imdb.IMDb.search_titles", spec=True)
    def test_search_by_title(self, search_titles_mock):
        """Test searching by title"""
        search_titles_mock.return_value = IMDB_DATA["GOOD_SEARCH"]
        imdb = IMDb("k_12345678")
        results = imdb.search_titles("Bambi")
        self.assertIsNotNone(results)
        self.assertIsNone(results["errorMessage"])
        self.assertIsNotNone(results["results"])
        self.assertEqual(results["results"][0]["id"], "tt1375666")

    # the models package has a module imdb.py which uses the requests.get method
    # so we patch "models.imdb.requests.get" NOT "requests.get"
    @patch("models.imdb.requests.get", spec=True)
    def test_search_with_no_results(self, get_mock):
        """Test searching with no results"""
        get_mock.return_value = Mock(status_code=404)
        imdb = IMDb("k_12345678")
        results = imdb.search_titles("Bambi")
        self.assertEqual(results, {})

    def test_search_with_no_results_context(self):
        """Test searching with no results context patch"""
        imdb = IMDb("k_12345678")
        with patch("models.imdb.requests.get", spec=True) as get_mock:
            get_mock.return_value = Mock(status_code=404)
            results = imdb.search_titles("Bambi")
        self.assertEqual(results, {})

    @patch("models.imdb.requests.get", spec=True)
    def test_search_by_title_failed(self, get_mock):
        """Test searching by title failed"""
        # setup mock Response object returned by get
        response_mock = Mock(spec=Response, status_code=200)
        # mock the json() method of response_mock
        response_mock.json = Mock(return_value=IMDB_DATA["INVALID_API"])
        # now use this response mock object as return val of get method
        get_mock.return_value = response_mock
        imdb = IMDb("bad-key")
        # Now results should contain our IMDB_DATA["INVALID_API"] dict
        results = imdb.search_titles("Bambi")
        self.assertIsNotNone(results)
        self.assertEqual(results["errorMessage"], "Invalid API Key")

    @patch("models.imdb.requests.get", spec=True)
    def test_movie_reviews(self, get_mock):
        """Test movie Reviews"""
        # setup mock Response object returned by get
        response_mock = Mock(spec=Response, status_code=200)
        # mock the json() method of response_mock should return python dict
        response_mock.json = Mock(return_value=IMDB_DATA["GOOD_REVIEW"])
        # now use this response mock object as return val of get method
        get_mock.return_value = response_mock
        imdb = IMDb("k_12345678")
        results = imdb.movie_reviews("tt1375666")
        self.assertIsNotNone(results)
        self.assertEqual(results["title"], "Bambi")
        self.assertEqual(results["items"][0]["username"], "mickey")
        self.assertEqual(results["items"][0]["rate"], "5")
        self.assertEqual(results["items"][0]["content"], "This movie will make you cry")

    @patch("models.imdb.requests.get", spec=True)
    def test_movie_ratings(self, get_mock):
        """Test movie Ratings"""
        # setup mock Response object returned by get
        response_mock = Mock(spec=Response, status_code=200)
        # mock the json() method of response_mock should return python dict
        response_mock.json = Mock(return_value=IMDB_DATA["GOOD_RATING"])
        # now use this response mock object as return val of get method
        get_mock.return_value = response_mock
        imdb = IMDb("k_12345678")
        results = imdb.movie_ratings("tt1375666")
        self.assertIsNotNone(results)
        self.assertEqual(results["title"], "Bambi")
        self.assertEqual(results["filmAffinity"], 3)
        self.assertEqual(results["rottenTomatoes"], 5)
