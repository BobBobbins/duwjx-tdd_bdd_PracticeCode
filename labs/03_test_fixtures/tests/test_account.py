"""
Test Cases TestAccountModel
"""
import json
from unittest import TestCase
from models import app, db
from models.account import AccountDB

ACCOUNT_DATA = []

class TestAccountModel(TestCase):  # the start of a test case
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):  # runs once before test case
        """ Connect and load data needed by tests """
        app.app_context().push()
        db.create_all()
        global ACCOUNT_DATA
        with open("tests/fixtures/account_data.json") as json_data:
            ACCOUNT_DATA = json.load(json_data) # deserialize into python data dict

    @classmethod
    def tearDownClass(cls):  # runs once after test case
        """Disconnect from database"""
        db.session.close()

    def setUp(self):  # runs before each test
        """Truncate the tables"""
        db.session.query(AccountDB).delete()
        db.session.commit()

    def tearDown(self):  # runs after each test
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_account(self):
        """Test creating an Account."""
        data = ACCOUNT_DATA[0]
        account_database = AccountDB(**data) # pass in data as kwargs
        account_database.create_account()
        self.assertEqual(len(AccountDB.all()), 1)

    def test_create_all_accounts(self):
        """ Test creating multiple Accounts """
        for data in ACCOUNT_DATA:
            account = AccountDB(**data)
            account.create_account()
        self.assertEqual(len(AccountDB.all()), len(ACCOUNT_DATA))