import unittest
from unittest.mock import patch
from tests.units.test_base import BasicTests

fake_competitions = [
    {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25"
    },
    {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13"
    },
    {
        "name": "Test Classic",
        "date": "2025-10-22 13:30:00",
        "numberOfPlaces": "7800"
    },
    {
        "name": "TestMonkey Classic",
        "date": "2025-09-22 13:30:00",
        "numberOfPlaces": "3"
    }
]

fake_clubs = [
    {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "72"
    },
    {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    },
    {"name": "She Lifts",
     "email": "kate@shelifts.co.uk",
     "points": "45"
     }
]


class TestPurchase(BasicTests):
    @patch('server.competitions', fake_competitions)
    def test_purchase_ok(self):
        response = self.app.post(
            "/purchasePlaces", data=dict(competition="Test Classic", club="She Lifts", places=2), follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Great-booking complete!" in response.data)
        self.assertTrue(b"Points available: 6" in response.data)
        self.assertTrue(b"Number of Places: 7798" in response.data)

    def test_purchase_on_past_competitions(self):
        response = self.app.post(
            "/purchasePlaces", data=dict(competition="Fall Classic", club="She Lifts", places=2), follow_redirects=True
        )
        self.assertTrue(b"Past competition, please select another one" in response.data)

    @patch('server.competitions', fake_competitions)
    def test_purchase_more_than_available_places(self):
        response = self.app.post(
            "/purchasePlaces", data=dict(competition="TestMonkey Classic", club="She Lifts", places=4),
            follow_redirects=True
        )
        self.assertTrue(b"Not enough places or points to book" in response.data)

    @patch('server.competitions', fake_competitions)
    def test_purchase_with_not_enough_points(self):
        response = self.app.post(
            "/purchasePlaces", data=dict(competition="TestMonkey Classic", club="Iron Temple", places=8),
            follow_redirects=True
        )
        self.assertTrue(b"Not enough places or points to book" in response.data)

    @patch('server.competitions', fake_competitions)
    def test_purchase_with_negative_places(self):
        response = self.app.post(
            "/purchasePlaces", data=dict(competition="TestMonkey Classic", club="She Lifts", places=-2),
            follow_redirects=True
        )
        self.assertTrue(b"Please use positive numbers" in response.data)

    @patch('server.competitions', fake_competitions)
    @patch('server.clubs', fake_clubs)
    def test_purchase_more_than_12_places(self):
        response = self.app.post(
            "/purchasePlaces", data=dict(competition="Test Classic", club="Simply Lift", places=13),
            follow_redirects=True
        )
        self.assertTrue(b"Please book 12 places or less" in response.data)


if __name__ == "__main__":
    unittest.main()
