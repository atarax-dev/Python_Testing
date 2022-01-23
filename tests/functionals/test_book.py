import unittest
from unittest.mock import patch

from tests.functionals.test_purchase import fake_competitions
from tests.units.test_base import BasicTests


@patch('server.competitions', fake_competitions)
class TestBook(BasicTests):
    """Classe de tests sur l'affichage de l'écran de réservation

    """
    def test_book(self):
        response = self.app.get("/book/Test%20Classic/She%20Lifts", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'How many places?' in response.data)

    def test_book_with_wrong_path(self):
        response = self.app.get("/book/Fake%20Classic/She%20Lifts", follow_redirects=True)
        self.assertRaises(IndexError)
        self.assertTrue(b'Something went wrong-please try again' in response.data)


if __name__ == "__main__":
    unittest.main()
