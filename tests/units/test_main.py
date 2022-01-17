import unittest
from tests.units.test_base import BasicTests
from server import load_clubs, load_competitions, is_competition_date_wrong
import json


class TestMain(BasicTests):
    def test_main_page(self):
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 500)

    def test_loads_club(self):
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

    def test_load_competitions(self):
        competitions = load_competitions()
        self.assertTrue(len(competitions) == 3)

        comp1 = "Spring Festival"
        comp2 = "Fall Classic"
        comp3 = "Test Classic"
        comp4 = "Fake Classic"

        self.assertTrue(comp1 in [comp["name"] for comp in competitions])
        self.assertTrue(comp2 in [comp["name"] for comp in competitions])
        self.assertTrue(comp3 in [comp["name"] for comp in competitions])
        self.assertFalse(comp4 in [comp["name"] for comp in competitions])

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
        self.assertTrue(b'Email not found' in response.data)

    def test_book(self):
        response = self.app.get("/book/Test%20Classic/She%20Lifts", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_book_with_wrong_path(self):
        response = self.app.get("/book/Fake%20Classic/She%20Lifts", follow_redirects=True)
        self.assertRaises(IndexError)
        self.assertTrue(b'Something went wrong-please try again' in response.data)

    def test_purchase(self):
        response = self.app.post(
            "/purchasePlaces", data=dict(competition="Test Classic", club="She Lifts", places=2), follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_validate_competition_date(self):
        date = '2020-03-27 10:00:00'
        self.assertTrue(is_competition_date_wrong(date))



if __name__ == "__main__":
    unittest.main()
