import unittest
from unittest.mock import patch

from tests.units.test_base import BasicTests
from server import load_clubs, load_competitions, is_competition_date_wrong


class TestMain(BasicTests):
    def test_main_page(self):
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 500)

    def test_load_clubs(self):
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
        self.assertTrue(len(competitions) == 2)

        comp1 = "Spring Festival"
        comp2 = "Fall Classic"
        comp3 = "Fake Classic"

        self.assertTrue(comp1 in [comp["name"] for comp in competitions])
        self.assertTrue(comp2 in [comp["name"] for comp in competitions])
        self.assertFalse(comp3 in [comp["name"] for comp in competitions])

    def test_validate_competition_date(self):
        date = '2020-03-27 10:00:00'
        self.assertTrue(is_competition_date_wrong(date))

    def test_list_clubs(self):
        response = self.app.get("/clubs", follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
