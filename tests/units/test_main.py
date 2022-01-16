import unittest
from tests.units.test_base import BasicTests
from server import load_clubs, load_competitions
import json


class TestMain(BasicTests):
    def test_main_page(self):
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 500)

    def test_email_loads_club(self):
        clubs = load_clubs()
        self.assertTrue(len(clubs) == 3)

        email1 = "john@simplylift.co"
        email2 = "admin@irontemple.com"
        email3 = "kate@shelifts.co.uk"
        email4 = "michel@google.com"

        self.assertTrue(email1 in [club["email"] for club in clubs])
        self.assertTrue(email2 in [club["email"] for club in clubs])
        self.assertTrue(email3 in [club["email"] for club in clubs])
        self.assertFalse(email4 in [club["email"] for club in clubs])

    def test_loads_club_alt(self):
        clubs = json.loads(
            '[{"name":"Simply Lift","email":"atarax@simplylift.co","points":"250"}]'
        )
        self.assertTrue(len(clubs) == 1)
        email1 = "atarax@simplylift.co"
        self.assertTrue(email1 in [club["email"] for club in clubs])

    def test_route_email_ok(self):
        response = self.login("john@simplylift.co")
        self.assertEqual(response.status_code, 200)

    def test_route_email_nok(self):
        response = self.login("atarax@test.com")
        self.assertRaises(IndexError)

    def test_book(self):
        response = self.app.get("/book/Test%20Classic/She%20Lifts", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_purchase(self):

        response = self.app.post(
            "/purchasePlaces", data=dict(competition="Test Classic", club="She Lifts", places=2), follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
