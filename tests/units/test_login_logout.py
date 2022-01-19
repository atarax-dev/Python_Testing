import unittest
from tests.units.test_base import BasicTests


class TestLoginLogout(BasicTests):
    def test_route_email_ok(self):
        response = self.login("john@simplylift.co")
        self.assertEqual(response.status_code, 200)

    def test_route_email_nok(self):
        response = self.login("atarax@test.com")
        self.assertRaises(IndexError)
        self.assertTrue(b'Email not found' in response.data)

    def test_logout(self):
        self.login("john@simplylift.co")
        response = self.app.get("/logout", follow_redirects=False)
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
