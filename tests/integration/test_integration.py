import unittest
from unittest.mock import patch, Mock

from tests.functionals.test_purchase import fake_competitions
from tests.units.test_base import BasicTests
from server import load_clubs, load_competitions


class TestUserScenario(BasicTests):

    @patch('server.competitions', fake_competitions)
    def test_scenario(self):
        clubs = load_clubs()
        self.assertTrue(len(clubs) == 3)
        competitions = load_competitions()
        self.assertTrue(len(competitions) == 2)
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.login("kate@shelifts.co.uk")
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/book/TestMonkey%20Classic/She%20Lifts", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        purchase_response = self.app.post(
            "/purchasePlaces", data=dict(competition="TestMonkey Classic", club="She Lifts", places=2), follow_redirects=True
        )

        self.assertEqual(purchase_response.status_code, 200)
        self.assertTrue(b"Great-booking complete!" in purchase_response.data)
        self.assertTrue(b"Points available: 8" in purchase_response.data)
        self.assertTrue(b"Number of Places: 1" in purchase_response.data)
        response = self.app.get("/logout", follow_redirects=False)
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
