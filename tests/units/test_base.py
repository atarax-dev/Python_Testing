import unittest
from server import app


class BasicTests(unittest.TestCase):
    """Classe parente permettant de mettre en place l'environnement de test 

    """
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = True
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    def login(self, email):
        return self.app.post(
            "/showSummary", data=dict(email=email), follow_redirects=True
        )


if __name__ == "__main__":
    unittest.main()
