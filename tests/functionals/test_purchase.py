import unittest
from tests.units.test_base import BasicTests


class TestPurchase(BasicTests):
    def test_purchase_ok(self):
        response = self.app.post(
            "/purchasePlaces", data=dict(competition="Test Classic", club="She Lifts", places=2), follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Great-booking complete!" in response.data)
        self.assertTrue(b"Points available: 10" in response.data)
        self.assertTrue(b"Number of Places: 7798" in response.data)

    def test_purchase_on_past_competitions(self):
        response = self.app.post(
            "/purchasePlaces", data=dict(competition="Fall Classic", club="She Lifts", places=2), follow_redirects=True
        )
        self.assertTrue(b"Past competition, please select another one" in response.data)

    def test_purchase_more_than_available_places(self):
        response = self.app.post(
            "/purchasePlaces", data=dict(competition="TestMonkey Classic", club="She Lifts", places=4),
            follow_redirects=True
        )
        self.assertTrue(b"Not enough places to book" in response.data)

    def test_purchase_with_negative_places(self):
        response = self.app.post(
            "/purchasePlaces", data=dict(competition="TestMonkey Classic", club="She Lifts", places=-2),
            follow_redirects=True
        )
        self.assertTrue(b"Please use positive numbers" in response.data)

    def test_purchase_more_than_12_places(self):
        response = self.app.post(
            "/purchasePlaces", data=dict(competition="Test Classic", club="She Lifts", places=13),
            follow_redirects=True
        )
        self.assertTrue(b"Please book 12 places or less" in response.data)


if __name__ == "__main__":
    unittest.main()
